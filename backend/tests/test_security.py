import pytest

from app.security import InputError, UnsafeURLError, parse_query, slugify, validate_public_url


def public(host):
    from ipaddress import ip_address
    return [ip_address("93.184.216.34")]


@pytest.mark.parametrize("url", [
    "http://localhost/x", "http://127.0.0.1/", "http://10.0.0.5/", "http://192.168.1.1/",
    "http://172.16.0.1/", "http://169.254.169.254/latest/meta-data/", "http://metadata.google.internal/",
    "http://[::1]/", "http://2130706433/", "http://0x7f.0.0.1/", "http://100.100.100.200/",
    "ftp://example.com/", "file:///etc/passwd", "https://user:pw@example.com/", "https://example.com:8443/",
    "http://intranet.local/", "http://foo/", "https://[::ffff:127.0.0.1]/",
])
def test_blocks_unsafe_urls(url):
    with pytest.raises(UnsafeURLError):
        validate_public_url(url, resolver=public)


def test_blocks_host_resolving_to_private():
    from ipaddress import ip_address
    with pytest.raises(UnsafeURLError):
        validate_public_url("https://evil.example.com/", resolver=lambda h: [ip_address("10.1.2.3")])


def test_allows_public_url_and_strips_fragment():
    assert validate_public_url("https://Docs.Example.com/a?b=1#frag", resolver=public) == "https://docs.example.com/a?b=1"


def test_parse_name_and_url():
    n = parse_query("Acme CRM")
    assert (n.kind, n.name, n.url) == ("name", "Acme CRM", None)
    u = parse_query("acme.com/docs", resolver=public)
    assert u.kind == "url" and u.domain == "acme.com" and u.name == "Acme" and u.url.startswith("https://")


@pytest.mark.parametrize("bad", ["", " ", "a", "x" * 201, "name\x00bad", "<script>alert(1)</script>"])
def test_rejects_bad_input(bad):
    with pytest.raises(InputError):
        parse_query(bad)


def test_unsafe_url_in_query_rejected():
    with pytest.raises(UnsafeURLError):
        parse_query("http://169.254.169.254/", resolver=public)


def test_slugify():
    assert slugify("Google Calendar!") == "google-calendar"
    assert slugify("!!!") == "app"
