"""Seed guide: github. Edit only this file when reconciling this provider."""
from __future__ import annotations

from ._common import *  # noqa: F401,F403
from ._common import D, REVIEW_NOTES, V, U, st, bl, src
from ..models import ApprovalWait, EffortEstimate, Guide

# ============================================================================ GitHub
GUIDE = Guide(
    id="github", slug="github", provider_name="GitHub", category="Developer tools",
    tagline="Self-serve in minutes; the real catch is organization OAuth-app restrictions.",
    website="https://github.com", generated_by="seed", verified_on=D, overall_confidence="high",
    difficulty="easy",
    difficulty_explanation=(
        "Registering an OAuth App or GitHub App is a settings form with no GitHub review described in the registration docs. "
        "What slows teams down is organization policy: OAuth App access restrictions are on by default for new organizations, "
        "so an org owner may have to approve your app before it can see org data."
    ),
    effort=EffortEstimate(short_label="~0.5–1.5 h hands-on (estimate)", min_hours=0.5, max_hours=1.5,
                          rationale="Form registration plus the authorize/callback code. Assumes you have built an OAuth flow before and the target org does not restrict OAuth apps."),
    approval_wait=ApprovalWait(
        short_label="No review described", status="none_documented",
        summary=("The registration docs we read describe no GitHub review of your app; it is created immediately from a settings form. "
                 "Organizations can restrict OAuth apps and an owner may need to approve yours, but no turnaround time is stated in the docs."),
        source_ids=["S7"]),
    prerequisites=[
        V("A GitHub account that will own the OAuth App: a personal account, or an organization you have administrative access to.", "S1", quote="under your personal account or under any organization you have administrative access to."),
        V("Decide between an OAuth App and a GitHub App first: GitHub Apps are not subject to organization application policies; OAuth Apps need an org owner's authorization when a policy is active.", "S6", quote="GitHub Apps aren't subject to organization application policies."),
        V("Up to 10 callback URLs can be entered (the registration form asks for a callback URL; 'at least one' is our reading of the form, not a quoted rule).", "S1", quote="You can enter up to 10 callback URLs."),
    ],
    steps=[
        st(1, "Choose OAuth App or GitHub App", "GitHub Apps request fine-grained permissions and are not subject to org application policies. OAuth Apps use scopes and share the authorizing user's access. Pick before registering; the settings paths differ.", "developer", "verified", "S6"),
        st(2, "Open the registration form", "Profile menu → Settings → Developer settings → OAuth apps → New OAuth App. (GitHub Apps: Developer settings → GitHub Apps → New GitHub App.) Create it under a personal account or an organization where you are an admin.", "developer", "verified", "S1", "S4"),
        st(3, "Fill in app details and callback URL(s)", "Enter an application name, homepage URL, optional description and the authorization callback URL. Use 'Add callback URL' for more (maximum 10).", "developer", "verified", "S1"),
        st(4, "Decide on token expiry and device flow", "'Expire user access tokens' is on by default; uncheck it only if your code cannot use refresh tokens. Enable Device Flow only for headless or CLI apps.", "both", "verified", "S1", "S2"),
        st(5, "Register the application", "Click Register application, then keep the client ID and client secret in server-side environment variables, never in frontend code or git.", "developer", "unverified", "S1"),
        st(6, "Send users to the authorize endpoint", "Redirect to https://github.com/login/oauth/authorize with client_id and a random state. redirect_uri is optional (if left out GitHub redirects to the first registered callback URL). PKCE (code_challenge and code_challenge_method) is recommended rather than required, and the method must be S256; plain is not supported.", "agent", "verified", "S2", quote="Must be `S256` - the `plain` code challenge method is not supported."),
        st(7, "Handle the callback and exchange the code", "GitHub redirects back with code and state. Abort if state does not match. Exchange the code at https://github.com/login/oauth/access_token before it expires (10 minutes).", "agent", "verified", "S2", quote="The temporary code will expire after 10 minutes."),
        st(8, "Test with your own account, then an org", "Authorize with your own account first, then with an account in an org that has OAuth App access restrictions to see the owner-approval path. The docs we read give no dedicated test procedure.", "both", "unverified", "S2", "S7"),
    ],
    callback_requirements=[
        V("Up to 10 callback URLs per app.", "S1", "S4", quote="You can enter up to 10 callback URLs."),
        V("By default the redirect_uri you send must exactly match a registered callback URL. Wildcard matching can be enabled per URL: the host (excluding subdomains) and port must exactly match, and the path must be a subdirectory of the callback URL, so any subdomain of the registered host matches. The docs recommend disabling wildcard matching if you do not need it.", "S2", "S5", quote="If your app does not need wildcard matching, we recommend that you disable it."),
        V("Apps (the same sentence appears on both the GitHub App callback page and the OAuth authorizing page) that had a single callback URL enabled before August 3, 2026 have wildcard matching enabled for that callback URL.", "S5", "S2", quote="Apps that had a single callback URL enabled prior to August 3, 2026 have wildcard matching enabled for that callback URL."),
        V("For native applications the optional redirect_uri can be a loopback URL whose port need not match the registered callback URL; the docs say to use the loopback literal 127.0.0.1 or IPv6 ::1 rather than localhost. The loopback example uses plain http.", "S2"),
        U("HTTPS is not stated as a requirement on the pages we read (examples use https).", "S2"),
    ],
    scopes=[
        V("repo: full access to public and private repositories, plus the ability to manage org-owned resources such as projects, invitations, team memberships and webhooks.", "S3", quote="including projects, invitations, team memberships and webhooks."),
        V("read:user (profile), user:email (email addresses), read:org (read-only access to organization membership, organization projects and team membership), workflow (add and update GitHub Actions workflow files).", "S3", quote="Grants the ability to add and update GitHub Actions workflow files."),
        V("Users can edit the scopes you request, so your app may receive less access than requested; check the X-OAuth-Scopes response header to see which scopes your token has. The scopes page also suggests considering a GitHub App instead of an OAuth App.", "S3", quote="However, users can edit their scopes, effectively granting your application less access than you originally requested."),
        V("GitHub Apps use permissions instead of scopes: each is set to Read-only, Read & write or No access; the webhook events available depend on the permissions selected.", "S4", quote="The permissions that you selected in the previous step determine what webhook events are available."),
    ],
    testing=[
        V("Device flow is intended for headless or CLI apps; the non-web flow using personal access tokens is described as for limited situations such as testing.", "S2", quote="Non-web authentication is available for limited situations like testing."),
        U("Authorize with your own account, then revoke the app from your GitHub settings to repeat the consent screen.", "S2"),
    ],
    publishing=[
        V("OAuth App access restrictions are enabled by default for new organizations. Members can request owner approval and owners are notified; when a policy is active only an owner can authorize installation of an OAuth App.", "S7", "S6", quote="When you create a new organization, OAuth app access restrictions are enabled by default."),
        V("GitHub Apps are not subject to organization application policies; an owner grants repository access instead.", "S6", quote="A GitHub App only has access to the repositories an organization owner has granted."),
    ],
    blockers=[
        bl("Organization blocks your OAuth App", "With app access restrictions on, an unapproved OAuth App cannot access org resources.", "Ask an org owner to approve it, or switch to a GitHub App, which these policies do not apply to. No approval turnaround is stated in the docs.", "verified", "S7", "S6"),
        bl("Expiring user tokens", "With expiry on, access tokens last 8 hours and refresh tokens 6 months without use. Enabling expiry does not expire existing tokens. A bad_refresh_token error means restarting the authorization flow.", "Implement refresh handling before launch, or deliberately opt out.", "verified", "S2"),
        bl("Short-lived authorization codes", "The OAuth authorization code expires after 10 minutes; device codes after 900 seconds.", "Exchange the code immediately in the callback handler.", "verified", "S2"),
        bl("App limits", "Up to 100 OAuth Apps per owner and up to 10 callback URLs.", None, "verified", "S1"),
        bl("Token and rate limits", "Ten tokens are issued per user/application/scope combination. OAuth apps are separately limited to 2,000 access token requests per hour, and a distinct limit applies if an app signs a user in ten times within one hour.", "Reuse and refresh tokens rather than minting new ones on every request; see the rate-limit page for the re-authorization consequence.", "verified", "S2", "S8"),
    ],
    agent_can_do=[
        "Write the authorize redirect and callback handler with state and PKCE.",
        "Add refresh-token handling and environment-variable configuration for client ID and secret.",
        "Draft the request message to an organization owner asking for OAuth App approval.",
        "Write a smoke-test script for the token exchange.",
    ],
    developer_must_do=[
        "Sign in and create the app under the owning account or organization (needs a human session and admin rights for orgs).",
        "Decide OAuth App vs GitHub App and whether to expire user tokens.",
        "Store the client secret securely and rotate it if it leaks.",
        "Get an org owner to approve the app if the org restricts OAuth Apps.",
    ],
    sources=[
        src(1, "Creating an OAuth app", "https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app"),
        src(2, "Authorizing OAuth apps", "https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps", note="A search result suggested /using-oauth-apps/authorizing-oauth-apps as a canonical path, but on 2026-10-29 that URL returned a different page without the code-expiry text; the building-oauth-apps path above is the one that contains the quoted statements."),
        src(3, "Scopes for OAuth apps", "https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps"),
        src(4, "Registering a GitHub App", "https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/registering-a-github-app"),
        src(5, "About the user authorization callback URL", "https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/about-the-user-authorization-callback-url"),
        src(6, "Differences between GitHub Apps and OAuth apps", "https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/differences-between-github-apps-and-oauth-apps"),
        src(7, "About OAuth app access restrictions", "https://docs.github.com/en/organizations/managing-oauth-access-to-your-organizations-data/about-oauth-app-access-restrictions"),
        src(8, "Rate limits for OAuth apps", "https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/rate-limits-for-oauth-apps"),
    ],
    unknowns=[
        "Whether GitHub requires HTTPS for callback URLs (not stated on the pages read).",
        "Any GitHub review or verification for publishing apps, and GitHub Marketplace listing requirements (not read).",
        "How long an organization owner typically takes to approve an OAuth App (not stated).",
        "A dedicated testing procedure for either app type (none found).",
        "Whether the OAuth client secret should be stored server-side only: the creating and authorizing pages give no secret-storage guidance (step 5 is good practice, not a quoted GitHub statement).",
        "Whether OAuth App tokens share the user's 5,000 requests/hour REST limit: not stated on the OAuth rate-limits page, and the REST rate-limit page was not fetched.",
        "Whether revoking an authorization makes GitHub show the consent screen again (the docs say users can review and revoke authorizations, not that this repeats consent).",
        "Whether a GitHub App may be registered under an organization you only administer: the OAuth page says 'administrative access', the GitHub App page reportedly says 'organization you own' (not re-fetched).",
    ],
    review_notes=REVIEW_NOTES + [
        "Reconciled against a second verification pass on 2026-10-29: 26 claims confirmed, 2 corrected, 4 left unverified.",
    ],
)
