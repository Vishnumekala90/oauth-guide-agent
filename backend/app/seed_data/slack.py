"""Seed guide: slack. Edit only this file when reconciling this provider."""
from __future__ import annotations

from ._common import *  # noqa: F401,F403
from ._common import D, REVIEW_NOTES, V, U, st, bl, src
from ..models import ApprovalWait, EffortEstimate, Guide

# ============================================================================== Slack
GUIDE = Guide(
    id="slack", slug="slack", provider_name="Slack", category="Communication",
    tagline="Instant for your own workspace; months of lead time if you want a Marketplace listing.",
    website="https://api.slack.com", generated_by="seed", verified_on=D, overall_confidence="high",
    difficulty="moderate",
    difficulty_explanation=(
        "Creating an app and installing it to a development workspace is quick and needs no review. "
        "Distributing it to other workspaces is also self-serve, but a Slack Marketplace listing requires installs on 10+ active workspaces, "
        "landing, support and privacy pages, a demo video and a multi-stage review."
    ),
    effort=EffortEstimate(short_label="~1–3 h hands-on (estimate)", min_hours=1, max_hours=3,
                          rationale="Covers app creation, scopes, HTTPS redirect URL and the code exchange for your own install. Marketplace preparation (pages, video, test accounts) is extra and not included."),
    approval_wait=ApprovalWait(
        short_label="Up to ~10 wks (Marketplace only)", status="documented",
        summary=("No Slack review is described for installing your own app or activating public distribution. For a Marketplace listing, the docs say preliminary review takes up to 10 business days to return feedback, "
                 "and functional review takes up to 10 weeks for new submissions (6 weeks for published apps resubmitting changes). Slack states it cannot skip or accelerate review. "
                 "Some workspaces also require an admin to approve installs; no timing is stated."),
        source_ids=["S4", "S3"]),
    prerequisites=[
        V("A Slack workspace to use as your development workspace.", "S2"),
        V("An HTTPS Redirect URL you control (all OAuth redirect, interaction, options-load and Events API URLs need SSL for public distribution).", "S1", "S3"),
        V("For the Marketplace: the app installed on 10 or more active workspaces (active = used in the past 28 days), plus landing page, support page and privacy policy.", "S4", "S5",
          quote="Your app has been installed on 10 or more active workspaces"),
    ],
    steps=[
        st(1, "Create the app", "On the Slack app settings page choose Create an app, select Blank app and Continue, then select the development workspace where you will build the app.", "developer", "verified", "S2",
       quote="Select the Workspace where you'll be developing your app."),
        st(2, "Add scopes and a Redirect URL", "In OAuth & Permissions add Bot Token Scopes (and user scopes if needed) and your HTTPS Redirect URL(s).", "developer", "verified", "S1", "S2"),
        st(3, "Install to your workspace", "Click Install to Workspace and Allow; the token appears under OAuth Tokens.", "developer", "verified", "S2",
       quote="You'll see an access token under OAuth Tokens."),
        st(4, "Redirect users to Slack's authorize URL", "Send users to https://slack.com/oauth/v2/authorize with client_id, scope (bot) / user_scope (user) and a state value.", "agent", "verified", "S1",
       quote="provide a `user_scope` parameter with requested user scopes instead of, or in addition to, the `scope` parameter."),
        st(5, "Handle the callback", "Verify state, then exchange the code via oauth.v2.access. The code expires after ten minutes. If several Redirect URLs are configured, send the same redirect_uri in both calls.", "agent", "verified", "S1"),
        st(6, "Distribute to other workspaces", "Manage Distribution → complete the 'Share Your App with Other Workspaces' checklist → Activate Public Distribution.", "developer", "verified", "S3",
       quote="Click Activate Public Distribution."),
        st(7, "Test on a non-development workspace", "Walk through install, onboarding, use and uninstall as a new customer. Slack cannot access your workspaces, so prepare test accounts or dummy data.", "both", "verified", "S4",
       quote="We cannot access any Slack workspaces (even created for testing)"),
        st(8, "Prepare and submit to the Marketplace (optional)", "Landing page, support page, privacy policy, 1600×1000 images, short description of 10 words or fewer, a demo video of the install/OAuth flow, and a collaborator on the app. S5 only strongly recommends the video; S4 says a new submission should include one.", "developer", "verified", "S4", "S5",
       quote="You must add a collaborator to your app."),
    ],
    callback_requirements=[
        V("redirect_uri must use HTTPS and must match, or be a subdirectory of, a configured Redirect URL. Redirect URLs cannot contain an anchor (#).", "S1",
          quote="Your `redirect_uri` must match or be a subdirectory of a Redirect URL configured under App Management."),
        V("If several Redirect URLs are configured, send redirect_uri in both the authorize and oauth.v2.access calls with the same value, otherwise you get bad_redirect_uri.", "S1",
          quote="`bad_redirect_uri`: Occurs when there are multiple `redirect_url` parameter values configured and they do not match."),
        V("PKCE can be enabled directly in app settings (no longer by request to Slack support); enabling is one-way, and all refresh tokens issued to PKCE-enabled apps expire after 30 days. Desktop redirects (custom URI schemes, and localhost redirects for PKCE-enabled apps) cannot request bot scopes.", "S7",
          quote="PKCE can now be enabled directly in your app settings without contacting Slack support."),
    ],
    scopes=[
        V("Bot scopes go in the scope parameter, user scopes in user_scope. Scopes are additive across installs and cannot be downgraded. Optional scopes can be declared via the manifest.", "S1",
          quote="It is not possible to downgrade an access token's scopes."),
        V("Marketplace: apps must follow least privilege and give a clear reason for each scope; requesting legacy/restricted scopes is prohibited, and Slack is unlikely to approve broad access to workspace message/file data.", "S5",
          quote="We are unlikely to approve broad access to workspace message/file data"),
        V("Token rotation is opt-in, cannot be turned off once turned on, and then access tokens expire every 12 hours. Marketplace apps can enable it via Published App Settings; the page does not state it is mandatory.", "S6",
          quote="Token rotation may not be turned off once it's turned on."),
    ],
    testing=[
        V("Quickstart: install to the development workspace with Install to Workspace.", "S2",
          quote="Install your app by selecting the Install to Workspace button."),
        V("Marketplace review expects testing on a non-development workspace including uninstall, test accounts or dummy data, and a demo video of the install/OAuth flow.", "S4"),
    ],
    publishing=[
        V("Public distribution (unlisted) is activated from Manage Distribution after the checklist; deactivating it removes the app from all other workspaces, and once Marketplace-listed it cannot be disabled this way.", "S3",
          quote="you cannot disable distribution in this way once your app is published within the Slack Marketplace"),
        V("Marketplace review: preliminary feedback takes up to 10 business days; functional review up to 10 weeks for new submissions and 6 weeks for published apps resubmitting changes. Slack says it cannot skip or accelerate review.", "S4",
          quote="We are unable to skip or accelerate the review process in order to coordinate with your launch"),
        V("Marketplace apps must use TLS 1.2 or greater and must use the state parameter when requesting access to customer data during OAuth.", "S5",
          quote="your app must use the state parameter when requesting access to customer data during the OAuth flow"),
        U("Marketplace apps must verify requests with a signing secret or mTLS: S5 only says the signing secret should be protected like a password and that these methods should be used instead of verification tokens; the exact requirement is a paraphrase.", "S5"),
        V("Some workspaces only allow admins to authorize apps, or only Marketplace apps; users can request installation through a guided interface.", "S3",
          quote="Some workspaces will restrict app installation so that only workspace administrators can provide authorization."),
    ],
    blockers=[
        bl("bad_redirect_uri", "Slack documents bad_redirect_uri for multiple configured redirect values that do not match across the authorize and token calls (a plain mismatch with a configured URL is not separately quoted).", "Send the identical redirect_uri to authorize and oauth.v2.access.", "verified", "S1"),
        bl("10 active installs needed before Marketplace submission", "Incomplete submissions are returned.", "Run a pilot with unlisted public distribution first.", "verified", "S4"),
        bl("Granular permissions upgrade is irreversible", "Upgrading to granular permissions is a fundamental, one-way change.", "Plan scopes before upgrading.", "verified", "S4"),
        bl("New scopes on a published app mean re-review", "Adding scopes or functionality to a published app needs a demo video or staging app and another review.", None, "verified", "S4"),
        bl("Workspace admin approval", "Workspaces that restrict app installs hold your install until an admin approves.", "Use the in-product install request; no turnaround time is stated.", "verified", "S3"),
    ],
    agent_can_do=[
        "Write the authorize redirect, state handling and oauth.v2.access exchange.",
        "Generate the app manifest with scopes and redirect URLs.",
        "Draft Marketplace copy (short description of 10 words or fewer, scope justifications) and a demo-video script.",
        "Build a checklist of the Marketplace guideline requirements.",
    ],
    developer_must_do=[
        "Create the app in your Slack account and install it to a workspace.",
        "Recruit 10+ active workspaces for the Marketplace and provide test accounts.",
        "Record the demo video and publish landing, support and privacy pages.",
        "Submit for review and answer reviewer feedback.",
    ],
    sources=[
        src(1, "Installing with OAuth", "https://docs.slack.dev/authentication/installing-with-oauth/"),
        src(2, "Creating an app from app settings", "https://docs.slack.dev/app-management/quickstart-app-settings/"),
        src(3, "App lifecycle and distribution", "https://docs.slack.dev/app-management/distribution/"),
        src(4, "Slack Marketplace review guide", "https://docs.slack.dev/slack-marketplace/slack-marketplace-review-guide/",
            note="Timeline text came through a summarizing fetch tool; re-check the live page before relying on it."),
        src(5, "Marketplace submission guidelines and requirements", "https://docs.slack.dev/slack-marketplace/slack-marketplace-app-guidelines-and-requirements/",
            note="This page itself states no review timeline."),
        src(6, "Using token rotation", "https://docs.slack.dev/authentication/using-token-rotation"),
        src(7, "PKCE now available in app settings (changelog, 2026-03-30)", "https://docs.slack.dev/changelog/2026/03/30/pkce"),
    ],
    unknowns=[
        "Whether plain localhost redirect URLs are allowed for non-PKCE apps: the OAuth page (S1) does not address localhost and requires HTTPS; the PKCE changelog mentions localhost redirects only for PKCE-enabled apps (cannot request bot scopes). Verify before relying on it.",
        "The maximum number of Redirect URLs (not stated on S1).",
        "Slack API rate limits (not on the pages read).",
        "How long workspace admins take to approve installs (no timing on S3).",
        "Whether token rotation is mandatory for Marketplace apps: S6 says such apps 'can have' it enabled, not that it is required.",
        "The ~1-3 h effort figure is our own estimate; no official page states it.",
    ],
    review_notes=REVIEW_NOTES + [
        "Reconciled against a second verification pass on 2026-10-29: 30 claims confirmed, 7 corrected, 3 left unverified.",
    ],
)
