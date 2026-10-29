"""Seed guide: notion. Edit only this file when reconciling this provider."""
from __future__ import annotations

from ._common import *  # noqa: F401,F403
from ._common import D, REVIEW_NOTES, V, U, st, bl, src
from ..models import ApprovalWait, EffortEstimate, Guide

# ============================================================================= Notion
GUIDE = Guide(
    id="notion", slug="notion", provider_name="Notion", category="Productivity",
    tagline="Create a public connection in minutes; the portal's Authorization URL field populates only after you submit the connection for review.",
    website="https://developers.notion.com", generated_by="seed", verified_on=D, overall_confidence="medium",
    difficulty="moderate",
    difficulty_explanation=(
        "Notion calls these public connections. Setup is a form in the developer portal, but the docs say the Authorization URL field populates after the connection is submitted for review, "
        "and no timeline or criteria for that step were found on the pages read. Installation scope (any workspace or selected workspaces) cannot be changed after creation, so choose before you create it."
    ),
    effort=EffortEstimate(short_label="~1–3 h hands-on (estimate)", min_hours=1, max_hours=3,
                          rationale="Portal form, capability selection and the OAuth code exchange with Basic auth. Marketplace listing content is extra."),
    approval_wait=ApprovalWait(
        short_label="5–10 business days (Marketplace listing)", status="documented", min_days=5, max_days=10,
        summary=("For a Marketplace listing, Notion says to expect to hear back within 5–10 business days by email. It is not stated whether the same timeline applies to the connection review that unlocks the Authorization URL."),
        source_ids=["S3"], quote="expect to hear back from our team within 5-10 business days via email"),
    prerequisites=[
        V("Access to the Notion Developer portal with a development workspace.", "S2"),
        V("One or more redirect URIs for your OAuth flow.", "S2"),
        V("Decide installation scope up front: Any workspace or Selected workspaces only. It cannot be changed after creation, and only 'Any workspace' connections are Marketplace-eligible.", "S2", "S3",
          quote="Installation scope is set once, at creation time, and can't be changed afterward."),
    ],
    steps=[
        st(1, "Open Public connections", "Notion Developer portal → Public connections (Build sidebar) → Create new connection.", "developer", "verified", "S2", quote="In the Build section of the sidebar, select Public connections."),
        st(2, "Fill in the connection", "Name, development workspace, redirect URI(s), installation scope and capabilities.", "developer", "verified", "S2", quote="Click Create new connection and fill in the required fields, including:"),
        st(3, "Copy the OAuth credentials", "The OAuth client ID and secret are on the Configuration tab.", "developer", "verified", "S2", quote="After creation, visit the Configuration tab to retrieve your OAuth client ID and OAuth client secret."),
        st(4, "Send users to the authorization URL", "Use client_id, redirect_uri, response_type=code and owner=user (state optional). Note: the Authorization URL field populates after the connection is submitted for review.", "agent", "verified", "S1", quote="Always use user."),
        st(5, "Exchange the code", "POST the code to https://api.notion.com/v1/oauth/token with HTTP Basic auth (CLIENT_ID:CLIENT_SECRET).", "agent", "verified", "S1", quote="The request is authorized using HTTP Basic Authentication."),
        st(6, "Store both tokens and handle refresh", "Store access_token and refresh_token; refreshing returns a new access token and a new refresh token.", "agent", "verified", "S1", quote="Refreshing an access token will generate a new access token and a new refresh token."),
        st(7, "List on the Marketplace (optional)", "Save a draft listing, check details under Listings → Connections and submit for review. Feedback arrives by email and you can resubmit.", "developer", "verified", "S3", quote="If changes are required, the Notion team sends feedback and you can resubmit after making updates."),
    ],
    callback_requirements=[
        V("Redirect URI(s) are set when creating the connection. The token request's redirect_uri is required if it was passed as a query parameter in the authorization URL, or if the connection has more than one redirect URI.", "S1",
          quote="If there are more than one redirect URIs included in your connection settings, this field is required."),
        V("The Create a token reference says redirect_uri is required in most cases, but is not allowed in the request body in some cases (the page lists conditions, including a single redirect URI in the connection settings with no redirect_uri in the Authorization URL). A mismatch is a likely source of redirect errors; check that page for the exact conditions.", "S5",
          quote="In most cases, the `redirect_uri` field is required."),
        U("No format rules (HTTPS, localhost) were stated in the text read.", "S1"),
    ],
    scopes=[
        V("Notion uses capabilities rather than scopes: Read, Update and Insert content; Read and Insert comments; user information as none, without email, or with email.", "S4",
          quote="No user information, User information without email addresses, User information with email addresses"),
        V("A change in capabilities forces users to re-authenticate; request only what you need.", "S4",
          quote="users will need to re-authenticate with a connection if the capabilities are changed"),
    ],
    testing=[
        V("Each prospective user must individually complete the auth flow for the connection.", "S1",
          quote="each prospective user needs to individually follow the auth flow for the connection."),
        U("No dedicated testing mode is described, and no official page read says whether the development workspace can use the connection before review. This could not be confirmed.", "S1"),
        V("Send the Notion-Version and Content-type headers in all API requests, and store the full token response: re-authorization may return a new access_token and refresh_token.", "S1",
          quote="also set the Notion-Version and Content-type headers in all of your requests, like so:"),
    ],
    publishing=[
        V("The Authorization URL field populates after a public connection is submitted for review (stated as an image caption under the Configuration tab screenshot). The docs do not say what 'review' means here or whether the flow works before it.", "S1",
          quote="The Authorization URL field populates after a public connection is submitted for review"),
        V("Partial authorization and page picker: if the user does not complete the flow, the connection will not have access to the selected pages; the page picker only shows pages or databases the user has full access to.", "S1",
          quote="the connection will *not* have access to the pages that were selected."),
        V("Marketplace listing is separate and only for 'Any workspace' connections. Notion says to expect to hear back within 5–10 business days by email; rejection can range from brand or trademark issues to quality concerns.", "S3",
          quote="expect to hear back from our team within 5-10 business days via email"),
    ],
    blockers=[
        bl("Authorization URL field empty until review submission", "The Authorization URL field in the portal is empty until you submit the connection for review. The docs do not say whether the flow works earlier (e.g. in the development workspace), and no timeline for the review was found on the pages read.", "Submit early; treat unknown review time as a launch risk.", "verified", "S1"),
        bl("Installation scope is permanent", "The choice between Any workspace and Selected workspaces only cannot be changed after creation.", "Create a new connection if you chose wrong.", "verified", "S2"),
        bl("Selected-workspace connections cannot be listed", "'Selected workspaces only' connections are not Marketplace-eligible.", None, "verified", "S3"),
        bl("Capability changes force re-consent", "Every user must authorize again when capabilities change.", "Settle capabilities before launch.", "verified", "S4"),
        bl("Each user authorizes individually", "Each prospective user must individually follow the auth flow. After a user authorizes, only that user can interact with the connection in their workspace.", None, "verified", "S1", "S2"),
    ],
    agent_can_do=[
        "Write the authorization redirect and the Basic-auth token exchange.",
        "Implement token storage and refresh handling.",
        "Choose the minimum capability set from your feature list.",
        "Draft Marketplace listing copy for review.",
    ],
    developer_must_do=[
        "Create the public connection in the Developer portal and choose installation scope.",
        "Submit the connection for review so the Authorization URL is populated.",
        "Submit the Marketplace listing and handle feedback emails.",
    ],
    sources=[
        src(1, "Authorization", "https://developers.notion.com/guides/get-started/authorization"),
        src(2, "Public connections", "https://developers.notion.com/guides/get-started/public-connections"),
        src(3, "List on the Marketplace", "https://developers.notion.com/guides/get-started/marketplace-listing"),
        src(4, "Connection capabilities", "https://developers.notion.com/reference/capabilities"),
        src(5, "Create a token", "https://developers.notion.com/reference/create-a-token"),
    ],
    unknowns=[
        "Redirect URI format rules (HTTPS / localhost): not stated on the Authorization, Public connections or Create a token pages.",
        "Whether the Authorization URL is usable by anyone before review submission (only the field's population is documented).",
        "Developer effort (1-3 h) is our own estimate, not from any source.",
        "Whether a public connection can be used in the development workspace before review.",
        "Whether the 5–10 business day timeline covers connection review or only Marketplace listing.",
        "Formal approval criteria (the baseline connection criteria and Best Practices pages were not read).",
    ],
    review_notes=REVIEW_NOTES + ["Reconciled against a second verification pass on 2026-10-29: 20 claims confirmed, 2 corrected, 4 left unverified."],
)
