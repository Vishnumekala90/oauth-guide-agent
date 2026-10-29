"""Seed guide: hubspot. Edit only this file when reconciling this provider."""
from __future__ import annotations

from ._common import *  # noqa: F401,F403
from ._common import D, REVIEW_NOTES, V, U, st, bl, src
from ..models import ApprovalWait, EffortEstimate, Guide

# ============================================================================ HubSpot
GUIDE = Guide(
    id="hubspot", slug="hubspot", provider_name="HubSpot", category="CRM",
    tagline="New apps now start in the HubSpot CLI; a Marketplace listing needs 3 real installs first.",
    website="https://developers.hubspot.com", generated_by="seed", verified_on=D, overall_confidence="medium",
    difficulty="moderate",
    difficulty_explanation=(
        "Legacy public apps can no longer be created (as of June 23, 2026), so a new app is a CLI project with app-hsmeta.json, uploaded with hs project upload. "
        "Test installs are added from the Distribution tab of the app. Listing in the HubSpot Marketplace is a manual review that needs at least 3 active installs from unaffiliated production accounts."
    ),
    effort=EffortEstimate(short_label="~2–4 h hands-on (estimate)", min_hours=2, max_hours=4,
                          rationale="CLI project setup, redirect URL and scopes, test install and the token exchange. Marketplace listing (7 tabs, support and legal URLs, setup guide) is extra."),
    approval_wait=ApprovalWait(
        short_label="~10 business days to first review", status="documented",
        summary=("Marketplace listing is reviewed manually. Initial review is stated as within 10 business days, and the overall process as no more than 60 days from the time feedback is shared. "
                 "The pages read do not say whether test installs on your own accounts are reviewed (the create-app guide simply has you add test installs from the Distribution tab). Certification is a separate application with its own requirements."),
        source_ids=["S6"], quote="within 10 business days"),
    prerequisites=[
        V("The new developer platform: create apps as a CLI project (hs project create → App) and upload it. Legacy public apps can no longer be created.", "S2", "S3",
          quote="As of June 23, 2026, legacy public apps can no longer be created."),
        V("At least one HTTPS auth redirect URL (http://localhost is allowed for testing) and at least one required scope; the app must include at minimum the read scope.", "S4",
          quote="Each app must have at least one auth redirect URL, and it must use HTTPS."),
        V("For the Marketplace: at least 3 active unique installs from unaffiliated production accounts with activity in the past 30 days, OAuth as the only auth method, a live support contact, live Terms and Privacy URLs and a public setup guide.", "S6",
          quote="your app must have at least three active, unique installs."),
        V("Token responses include expires_in, which gives the access-token lifetime in seconds; read it from the response rather than hardcoding a lifetime.", "S9",
          quote="you can check the `expires_in` parameter when generating an access token to determine its lifetime (in seconds)."),
    ],
    steps=[
        st(1, "Install the HubSpot CLI and authenticate", "The create-app guide asks for v7.6.0 of the HubSpot CLI (the pinned version on the page may change). Authenticate it with hs account auth.", "developer", "verified", "S3",
           quote="Make sure you're using v7.6.0 of the HubSpot CLI before proceeding."),
        st(2, "Create the app project", "Run hs project create, choose App as the base contents, and answer the prompts for distribution (marketplace or private), authentication (OAuth for multi-account installs) and features.", "both", "verified", "S3"),
        st(3, "Review app-hsmeta.json", "The distribution field in the app schema sets how the app is distributed; for Marketplace distribution the auth type must be oauth.", "agent", "verified", "S4",
           quote="The `distribution` field in your app schema allows you to configure how you want to distribute your app."),
        st(4, "Add redirect URLs and scopes", "Add at least one HTTPS redirectUrl (http://localhost is allowed for testing) and your requiredScopes, optionalScopes and conditionallyRequiredScopes, including at minimum read. Request only what you need.", "agent", "verified", "S4",
           quote="Each app must have at least one auth redirect URL, and it must use HTTPS."),
        st(5, "Set a unique app uid", "Change the uid property of the app in the top-level app-hsmeta.json to a unique value before uploading.", "agent", "verified", "S3"),
        st(6, "Upload the project", "Run hs project upload to upload the project to your HubSpot account and trigger a build.", "both", "verified", "S3"),
        st(7, "Copy the credentials", "Run hs project open from the project directory, go to the Auth tab and copy the Client ID and Client secret into your OAuth server configuration.", "developer", "verified", "S3"),
        st(8, "Install the app", "On the Distribution tab, next to Test installs, click Add test install(s) to install in a developer test account or a standard account.", "developer", "verified", "S3",
           quote="On the *Distribution* tab, next to *Test installs*, click **Add test install(s)**."),
        st(9, "Authorize and exchange the code", "Send the user to https://app.hubspot.com/oauth/authorize; HubSpot appends a code query parameter to the redirect URL. Exchange it with a URL-form-encoded POST to /oauth/2026-09/token for access and refresh tokens. (The authorize query parameters were not re-read; check the token page for the exact list.)", "agent", "verified", "S9",
           quote="To get OAuth access and refresh tokens, make a URL-form encoded `POST` request to `/oauth/2026-09/token`."),
        st(10, "List on the Marketplace (optional)", "Development → App Listings → Create listing. Complete 7 tabs (Listing info, App details, Pricing, App features, Support info, Testing info, Review info), fix validation errors, then Submit for review. Only one app can be submitted at a time (stated on the listing-requirements page).", "developer", "verified", "S7", "S6",
           quote="Click Submit for review in the top right."),
    ],
    callback_requirements=[
        V("Each app needs at least one auth redirect URL and it must be HTTPS; http://localhost is allowed for testing. Set in app-hsmeta.json redirectUrls.", "S4",
          quote="The only exception is that `http://localhost` is allowed for testing."),
        V("Legacy OAuth guide: the redirect_uri must use a domain; IP addresses are not supported.", "S1",
          quote="You also must use a domain, as IP addresses are not supported."),
    ],
    scopes=[
        V("requiredScopes, optionalScopes and conditionallyRequiredScopes in app configuration; at least one required scope, and at minimum read.", "S4",
          quote="At a minimum, your app must include the `read` scope"),
        V("The sample app-hsmeta.json on the create-app page lists crm.objects.contacts.read and crm.objects.contacts.write as required scopes.", "S3"),
        V("Marketplace listing: request only the scopes the app needs.", "S6", quote="only request scopes your app needs."),
    ],
    testing=[
        V("After installing in a test account, hs project dev starts local development. The create-app boilerplate is preset to https://localhost:3000/oauth-callback as the redirect URL; http://localhost is also an allowed redirect URL for testing.", "S3", "S4",
          quote="you can run `hs project dev` to start developing your app locally."),
        V("Test installs are added from the Distribution tab next to Test installs via Add test install(s).", "S3",
          quote="On the *Distribution* tab, next to *Test installs*, click **Add test install(s)**."),
        U("After clicking Add test install(s), a dialog asks you to review the app's requirements, tick a checkbox and click Connect app (reported for the create-app page; the dialog text was not re-read in the second pass).", "S3"),
        V("For listings, the install-flow page has a Preview the install flow section: Preview (top right of the listing editor) runs a test version of the installation process.", "S5",
          quote="Run through a test version of the installation process."),
    ],
    publishing=[
        V("Marketplace listings are manually reviewed by the HubSpot Ecosystem Quality team; at least 3 active unique installs required; one app submitted at a time; HubSpot's Technology Partner Program Agreement must be agreed to.", "S6",
          quote="App listing submissions are manually reviewed by the HubSpot Ecosystem Quality team."),
        V("Initial review is stated as within 10 business days; the overall process no more than 60 days from the time feedback is shared.", "S6",
          quote="the HubSpot Ecosystem Quality team will complete an initial review within 10 business days."),
        V("Certification requires being listed for at least six months, at least 60 active unique installs, an average API success rate above 95%, association with a verified domain and a demo video; apps with a browser extension get an additional security assessment. HubSpot responds to certification requests within 10 business days.", "S8",
          quote="Your app must be listed in the HubSpot Marketplace for at least six months."),
        V("Install-flow page notice: after October 26, 2026, selecting an install experience is required in all accounts the next time you edit an app's listing.", "S5",
          quote="After this date, it will be required in all accounts to select an install experience when you next edit an app's listing."),
    ],
    blockers=[
        bl("Legacy apps are gone", "Legacy public apps can no longer be created as of June 23, 2026; older tutorials show a flow that no longer works for new apps.", "Use the CLI project flow.", "verified", "S2"),
        bl("Only Super Admins or Marketplace-access users can install", "Per the legacy OAuth guide, users installing an app must be a Super Admin or have HubSpot Marketplace Access permissions (the new-platform pages were not checked for this).", "Install with an admin account.", "verified", "S1"),
        bl("Need 3 real installs before the Marketplace", "Unaffiliated production accounts only, with successful activity in the past 30 days.", "Recruit pilot customers early.", "verified", "S6"),
        bl("Listing requirements that send a listing to Draft", "Failing the listing requirements sets the listing to Draft mode only. Apps on a developer platform version announced as unsupported cannot be listed, and apps cannot use classic CRM cards (no longer supported as of June 16, 2025).", "Check these against your app before submitting.", "verified", "S6"),
    ],
    agent_can_do=[
        "Scaffold app-hsmeta.json with redirect URLs, scopes and stable uids.",
        "Write the authorize and token-exchange handler and refresh logic.",
        "Draft the listing copy, support page and setup-guide outline.",
        "Check the listing requirements against your app before submission.",
    ],
    developer_must_do=[
        "Install the CLI, authenticate and upload the project with your HubSpot account.",
        "Create test accounts and approve the install as an admin.",
        "Recruit 3 active production installs for a Marketplace listing.",
        "Agree to the Technology Partner Program Agreement and submit the listing.",
    ],
    sources=[
        src(1, "Working with OAuth (legacy apps)", "https://developers.hubspot.com/docs/apps/legacy-apps/authentication/working-with-oauth",
            note="Fetched at this URL; search results show the current slug as .../legacy-apps/authentication/oauth-quickstart-guide (same title)."),
        src(2, "Public apps (legacy)", "https://developers.hubspot.com/docs/api/creating-an-app"),
        src(3, "Create a new app using the CLI", "https://developers.hubspot.com/docs/apps/developer-platform/build-apps/create-an-app"),
        src(4, "App configuration", "https://developers.hubspot.com/docs/apps/developer-platform/build-apps/app-configuration"),
        src(5, "Understand the app installation flow", "https://developers.hubspot.com/docs/apps/developer-platform/list-apps/understand-app-install-flow"),
        src(6, "App listing requirements in the HubSpot Marketplace", "https://developers.hubspot.com/docs/apps/developer-platform/list-apps/listing-your-app/app-marketplace-listing-requirements"),
        src(7, "Listing your app in the HubSpot Marketplace", "https://developers.hubspot.com/docs/apps/developer-platform/list-apps/listing-your-app/listing-your-app/"),
        src(8, "Certification requirements", "https://developers.hubspot.com/docs/apps/developer-platform/list-apps/apply-for-certification/certification-requirements"),
        src(9, "Manage OAuth tokens (API reference, 2026-09)", "https://developers.hubspot.com/docs/api-reference/latest/authentication/manage-oauth-tokens"),
    ],
    review_notes=REVIEW_NOTES + [
        "Independent re-check (2026-10-28): the June 23, 2026 legacy-app cutoff, the HTTPS/localhost redirect rule, the minimum 'read' scope and the CLI create-app steps match the live pages. Correction made: distribution and auth are chosen via CLI prompts during hs project create, not hand-edited first. Removed an unconfirmed claim about uid changes.",
        "Reconciled against a second verification pass on 2026-10-29: 25 claims confirmed, 4 corrected, 3 left unverified.",
    ],
    unknowns=[
        "How to sign up for a HubSpot developer account (not covered on the pages read; the create-an-app page says one is not strictly required).",
        "A fixed access-token lifetime: the token page says to read expires_in from the response and gives no fixed number in the text read.",
        "Whether the new-platform OAuth guide differs from the legacy one beyond the token page (authorize query parameters not re-read).",
        "Whether redirect_uri must exactly match the configured URL, and any maximum number of redirect URLs (not stated on the legacy OAuth page or the 2026-09 token page).",
        "Whether the listing-process page gives a review timeline: it does not; its only stated timeline is 10 business days for unpublish requests. The review timeline lives on the listing-requirements page.",
        "Whether test installs on your own accounts need any HubSpot review, and whether certification is optional (no page read says either; the certification page only describes requirements).",
        "Any unverified-app banner at install, domain verification (one domain per account, DNS delay) and creation of configurable test accounts: the install-flow page has no such text; a changelog entry 'developer-identity-for-hubspot-apps' surfaced in search was not read.",
    ],
)
