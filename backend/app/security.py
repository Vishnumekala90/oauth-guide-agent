"""Input validation and SSRF protection.

`validate_public_url` is used for the user-submitted URL, for every search result before it is
fetched, and again for every redirect hop. It blocks non-http(s) schemes, credentials in the URL,
non-standard ports, localhost / internal hostnames, and any host that resolves to a private,
loopback, link-local, reserved, multicast or cloud-metadata address.

Known limit (documented in the README): DNS is resolved here and again by the HTTP client, so a
hostile DNS server could in theory rebind between the two lookups. Egress filtering at the network
layer is the production answer.
"""
from __future__ import annotations

import ipaddress
import re
import socket
from dataclasses import dataclass
from urllib.parse import urlsplit, urlunsplit

ALLOWED_PORTS = {None, 80, 443}
BLOCKED_HOSTNAMES = {
    "localhost",
    "metadata",
    "metadata.google.internal",
    "instance-data",
    "kubernetes.default",
}
BLOCKED_SUFFIXES = (".localhost", ".local", ".internal", ".intranet", ".lan", ".home", ".corp", ".localdomain")
# Always blocked even if some resolver reports them as "global".
EXTRA_BLOCKED_NETS = [
    ipaddress.ip_network("169.254.0.0/16"),  # link-local incl. AWS/GCP/Azure metadata 169.254.169.254
    ipaddress.ip_network("100.64.0.0/10"),  # carrier-grade NAT (Alibaba metadata 100.100.100.200)
    ipaddress.ip_network("192.0.0.0/24"),
    ipaddress.ip_network("198.18.0.0/15"),
    ipaddress.ip_network("fd00:ec2::/32"),  # AWS IPv6 metadata
    ipaddress.ip_network("fe80::/10"),
]

APP_NAME_RE = re.compile(r"^[\w .&+'’\-/()@:]{2,100}$", re.UNICODE)
MAX_URL_LEN = 2000


class InputError(ValueError):
    """User-correctable input problem. Message is safe to show."""


class UnsafeURLError(InputError):
    """URL rejected by SSRF policy. Message is safe to show."""


@dataclass(frozen=True)
class ParsedQuery:
    kind: str  # "url" | "name"
    raw: str
    name: str  # best-effort app name
    url: str | None  # normalised https URL when kind == "url"
    domain: str | None


def _is_blocked_ip(ip: ipaddress._BaseAddress) -> bool:
    if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped:
        ip = ip.ipv4_mapped
    if (
        ip.is_private
        or ip.is_loopback
        or ip.is_link_local
        or ip.is_multicast
        or ip.is_reserved
        or ip.is_unspecified
        or not ip.is_global
    ):
        return True
    return any(ip in net for net in EXTRA_BLOCKED_NETS if net.version == ip.version)


def _resolve(host: str) -> list[ipaddress._BaseAddress]:
    try:
        infos = socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise UnsafeURLError(f"Could not resolve host '{host}'.") from exc
    ips = []
    for info in infos:
        addr = info[4][0].split("%")[0]
        ips.append(ipaddress.ip_address(addr))
    if not ips:
        raise UnsafeURLError(f"Could not resolve host '{host}'.")
    return ips


def validate_public_url(url: str, *, resolver=_resolve) -> str:
    """Return a normalised URL or raise UnsafeURLError. `resolver` is injectable for tests."""
    if not isinstance(url, str) or not url or len(url) > MAX_URL_LEN:
        raise UnsafeURLError("URL is empty or too long.")
    if any(ord(c) < 32 or c in "\\" for c in url):
        raise UnsafeURLError("URL contains invalid characters.")
    try:
        parts = urlsplit(url)
        port = parts.port
    except ValueError as exc:
        raise UnsafeURLError("URL is malformed.") from exc
    if parts.scheme.lower() not in ("http", "https"):
        raise UnsafeURLError("Only http and https URLs are allowed.")
    if parts.username or parts.password:
        raise UnsafeURLError("URLs with embedded credentials are not allowed.")
    host = (parts.hostname or "").strip(".").lower()
    if not host:
        raise UnsafeURLError("URL has no host.")
    if port not in ALLOWED_PORTS:
        raise UnsafeURLError("Only standard web ports (80/443) are allowed.")
    if host in BLOCKED_HOSTNAMES or host.endswith(BLOCKED_SUFFIXES):
        raise UnsafeURLError("Internal hostnames are not allowed.")

    # Literal IPs (including decimal/hex/octal forms that inet_aton accepts) are checked directly.
    literal: ipaddress._BaseAddress | None = None
    try:
        literal = ipaddress.ip_address(host)
    except ValueError:
        try:
            literal = ipaddress.ip_address(socket.inet_aton(host))
        except OSError:
            literal = None
    if literal is not None:
        if _is_blocked_ip(literal):
            raise UnsafeURLError("Private, loopback and metadata addresses are not allowed.")
    else:
        if "." not in host:
            raise UnsafeURLError("Host must be a public domain name.")
        for ip in resolver(host):
            if _is_blocked_ip(ip):
                raise UnsafeURLError("Host resolves to a private or internal address.")

    clean = urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path or "/", parts.query, ""))
    return clean


def parse_query(raw: str, *, resolver=_resolve) -> ParsedQuery:
    """Classify user input as a URL/domain or an app name and validate it."""
    q = (raw or "").strip()
    if len(q) < 2:
        raise InputError("Enter an app name or website.")
    if len(q) > 200:
        raise InputError("Input is too long (200 characters max).")
    if any(ord(c) < 32 for c in q):
        raise InputError("Input contains control characters.")

    looks_like_url = bool(re.match(r"^[a-z][a-z0-9+.-]*://", q, re.I)) or (
        " " not in q and "." in q and re.match(r"^[\w.-]+\.[a-z]{2,}(/.*)?$", q, re.I) is not None
    )
    if looks_like_url:
        candidate = q if "://" in q else f"https://{q}"
        safe = validate_public_url(candidate, resolver=resolver)
        host = urlsplit(safe).hostname or ""
        return ParsedQuery(kind="url", raw=q, name=_name_from_host(host), url=safe, domain=host)

    if not APP_NAME_RE.match(q):
        raise InputError("App names may contain letters, numbers, spaces and basic punctuation only.")
    return ParsedQuery(kind="name", raw=q, name=q, url=None, domain=None)


_GENERIC_LABELS = {"www", "app", "apps", "developer", "developers", "dev", "docs", "api", "api2", "my", "web", "login"}
_SECOND_LEVEL = {"co", "com", "org", "net", "gov", "ac"}


def registrable_label(host: str) -> str:
    labels = [l for l in host.lower().split(".") if l]
    if len(labels) >= 3 and labels[-2] in _SECOND_LEVEL:
        return labels[-3]
    if len(labels) >= 2:
        return labels[-2]
    return labels[0] if labels else ""


def _name_from_host(host: str) -> str:
    label = registrable_label(host)
    return label.replace("-", " ").title() if label else host


def slugify(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return (s or "app")[:30]


def no_dns_resolver(host: str) -> list:
    """Resolver for deployments behind an egress proxy: skip local DNS (literal-IP and hostname rules still run)."""
    return []


def quick_key(raw: str) -> str | None:
    """Cheap, network-free reduction of user input to a lowercase alnum key (used to match curated guides)."""
    q = (raw or "").strip().lower()
    q = re.sub(r"^[a-z][a-z0-9+.-]*://", "", q).split("/")[0].removeprefix("www.")
    if not q or len(q) > 100:
        return None
    return re.sub(r"[^a-z0-9]", "", q) or None
