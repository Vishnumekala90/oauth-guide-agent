"""Seed guide: google calendar. Edit only this file when reconciling this provider."""
from __future__ import annotations

from ._common import *  # noqa: F401,F403
from ._common import D, REVIEW_NOTES, V, U, st, bl, src
from ..models import ApprovalWait, EffortEstimate, Guide

# ================================================================== Google Calendar
GUIDE = Guide(
    id="google-calendar", slug="google-calendar", provider_name="Google Calendar", category="Productivity",
    tagline="Quick in Testing mode, a verification project if you go public with sensitive scopes.",
    website="https://developers.google.com/workspace/calendar", generated_by="seed", verified_on=D, overall_confidence="medium",
    difficulty="hard",
    difficulty_explanation=(
        "Getting a client working takes an afternoon, but Testing mode caps you at 100 test users and tokens issued there expire after 7 days. "
        "Going public with sensitive or restricted scopes means verification: verified domain ownership, a public homepage, a privacy policy, a per-scope justification and a demo video. "
        "Which Calendar scopes count as sensitive vs restricted was not confirmed from the pages we read."
    ),
    effort=EffortEstimate(short_label="~3–6 h hands-on (estimate)", min_hours=3, max_hours=6,
                          rationale="Cloud project, consent screen, client and flow code, plus preparing the verification submission (justification text, demo video). Excludes writing a privacy policy or buying a domain."),
    approval_wait=ApprovalWait(
        short_label="3–5 business days (sensitive scopes)", status="documented", min_days=3, max_days=5,
        summary=("Google says sensitive-scope verification typically takes 3–5 business days; automated brand review usually completes in a few minutes. "
                 "The timeline for restricted-scope security assessment is not stated in the docs we read."),
        source_ids=["S2"], quote="The sensitive scope verification process typically takes 3-5 business days to complete."),
    prerequisites=[
        V("The Google Calendar API must be enabled for the project that makes the calls; the web-server guide says any application that calls Google APIs needs to enable them in the API Console.", "S3",
          quote="Any application that calls Google APIs needs to enable those APIs in the API Console."),
        V("To verify an app that requests sensitive scopes: verified ownership of your authorized domain(s) in Search Console, an application home page (a Google Play Store or Facebook page does not count), and a privacy policy visible to users and hosted on the same domain as the home page.", "S2",
          quote="Verify ownership of your project's authorized domains within the Google Search Console."),
        V("A detailed justification for each requested sensitive scope and a demo video uploaded to YouTube with Unlisted visibility for the verification submission.", "S2",
          quote="Upload the video to YouTube Studio and set its Visibility as Unlisted."),
    ],
    steps=[
        st(1, "Create or choose a Google Cloud project", "Everything (API enablement, consent screen, OAuth client) lives in one project.", "developer", "unverified", "S3"),
        st(2, "Enable the Google Calendar API", "Enable the Calendar API for the project in the API Console.", "developer", "verified", "S3",
           quote="Any application that calls Google APIs needs to enable those APIs in the API Console."),
        st(3, "Configure the consent screen (Branding, Audience, scopes)", "Add app details, developer contact and the Calendar scopes you need. Prefer the narrowest scope (for example calendar.events.readonly over calendar). The Audience page exists in the Cloud Console; the exact Branding menu was not seen in the pages read.", "developer", "unverified", "S5", "S6",
           quote="Generally, you should choose the most narrowly focused scope possible"),
        st(4, "Create a Web application OAuth client", "Cloud Console → Clients → Create Client → Web application, with redirect URIs that meet Google's rules. Download client_secret.json and keep it out of git (our advice, not from the docs).", "developer", "unverified", "S3",
           quote="Select the Web application application type."),
        st(5, "Implement the web-server flow", "Redirect to Google's authorization endpoint with access_type=offline if you need refresh tokens, then exchange the code on your server. The default is online; offline is what returns a refresh token.", "agent", "verified", "S3"),
        st(6, "Test in Testing mode with listed test users", "Add each tester under Audience. Only listed test users can authorize, they see a warning screen, and authorizations (including refresh tokens) expire after 7 days.", "both", "verified", "S1", "S6",
           quote="Authorizations by a test user will expire seven days from the time of consent."),
        st(7, "Publish the app (Testing → In production)", "Apps in Testing cannot be verified; publish first, then use 'Prepare for Verification'.", "developer", "verified", "S7",
           quote="Apps in development, testing or staging are not applicable for verification."),
        st(8, "Submit for verification", "Provide scope justifications and the demo video, then Submit for Verification. The review team communicates by email with the project owners and project editors configured on the project.", "developer", "verified", "S2", "S7",
           quote="will occur over email to the project owners and project editors configured when setting up your project."),
    ],
    callback_requirements=[
        V("For testing, redirect URIs may refer to the local machine, for example http://localhost:8080.", "S3",
          quote="For testing, you can specify URIs that refer to the local machine, such as http://localhost:8080."),
        U("The web-server page's redirect URI validation table (reported: HTTPS required except for localhost; raw-IP and googleusercontent.com hosts disallowed; URL-shortener domains disallowed unless you own the domain; no wildcards, fragments, userinfo, path traversal or open redirects; domain on the public suffix list) was only paraphrased by the first pass and could not be reproduced on re-fetch, so it is not marked verified. Check the page's table before registering URIs.", "S3"),
    ],
    scopes=[
        V("The OAuth scopes page lists 17 Calendar API v3 scopes (in the first 100k characters read), including calendar, calendar.readonly, calendar.events, calendar.events.readonly, calendar.freebusy, calendar.settings.readonly and calendar.app.created. The Calendar API 'Choose scopes' page lists 20, adding the add-on scopes calendar.addons.execute, calendar.addons.current.event.read and calendar.addons.current.event.write.", "S4", "S5",
          quote="Make secondary Google calendars, and see, create, change, and delete events on them"),
        V("Google says scope categories (non-sensitive, sensitive, restricted) are indicated automatically in the Google Cloud Console, so you can read each Calendar scope's category there.", "S8",
          quote="scope categories (non-sensitive, sensitive, or restricted) are indicated automatically in the Google Cloud Console"),
        U("Which Calendar scopes are non-sensitive, sensitive or restricted: neither the Calendar auth page nor the scopes page labels them, so no per-scope classification was confirmed.", "S4", "S5", "S8"),
    ],
    testing=[
        V("Testing status allows at most 100 test users listed on the consent screen; only they can authorize.", "S6",
          quote="limited to up to 100 test users listed in the OAuth consent screen."),
        V("Authorizations by a test user expire seven days after consent; the exception is apps requesting only userinfo.email, userinfo.profile and openid.", "S6",
          quote="Authorizations by a test user will expire seven days from the time of consent."),
        V("The overview page says marking an app Trusted overrides the 7-day refresh token expiration limit for apps in Testing. That Trusted status also lifts the 100-test-user cap was not found on any page read.", "S1",
          quote="the 7-day refresh token expiration limit for apps in the Testing status"),
    ],
    publishing=[
        V("Verification is required for public apps requesting sensitive or restricted scopes; internal apps do not need it.", "S1",
          quote="Required for public apps that request sensitive and restricted scopes."),
        V("For unverified apps requesting sensitive or restricted scopes, a hard cap of 100 total users applies and users see unverified-app warnings. Whether the cap is permanent or can be reset was not stated in the text read.", "S1",
          quote="a hard cap of 100 total users applies."),
        V("Apps in Testing are not eligible for verification and must be published first.", "S7",
          quote="Apps in development, testing or staging are not applicable for verification."),
        V("Restricted scopes additionally require a security assessment; the OAuth review team reaches out when it is time to start it.", "S7",
          quote="the OAuth review team will reach out to you when it's time to start the security assessment."),
        V("Apps that use only non-sensitive scopes are not required to complete app verification; a lighter 'brand verification' applies if you want your app name and logo shown.", "S8",
          quote="If your app utilizes only non-sensitive scopes, it is not mandatory for your app to complete the app verification process."),
        V("Refresh tokens remain valid until the user revokes access or the token expires.", "S3",
          quote="Refresh tokens are valid until the user revokes access or the refresh token expires."),
    ],
    blockers=[
        bl("Test-mode tokens expire after 7 days", "Refresh tokens issued to test users stop working after a week, which looks like random auth failures.", "Re-consent test users weekly, or have a Workspace admin mark the app Trusted.", "verified", "S1", "S6"),
        bl("100-user cap on unverified public apps", "A published but unverified app with sensitive or restricted scopes has a hard cap of 100 total users.", "Start verification before you need user 101.", "verified", "S1"),
        bl("Over-broad scopes", "The docs advise requesting the narrowest scope; the verification page says you must request scopes needing the least access to user data necessary (that over-broad requests draw reviewer questions is our inference).", "Use calendar.events.* or calendar.freebusy instead of full calendar access where possible.", "verified", "S2"),
        bl("Review emails go only to owners and editors", "The review team communicates by email with the project owners and project editors configured on the project, and Google says to keep those roles current. Compliant verification results are valid for 7 days. Missing an email can stall the review (our inference).", "Use a monitored owner address.", "verified", "S2"),
        bl("Home page requirements", "The home page cannot be a Play Store or Facebook page.", None, "verified", "S2"),
    ],
    agent_can_do=[
        "Write the server-side authorization and token-exchange code, including refresh handling.",
        "Draft per-scope justification text and a demo-video script showing the consent flow and each scope in use.",
        "Check that redirect URIs meet Google's HTTPS and host rules.",
        "Prepare a privacy-policy outline for review by a human.",
    ],
    developer_must_do=[
        "Create the Cloud project, consent screen and OAuth client (needs your Google account).",
        "Verify domain ownership in Search Console and publish a privacy policy and home page.",
        "Record and upload the unlisted YouTube demo video.",
        "Submit for verification and respond to reviewer emails.",
    ],
    sources=[
        src(1, "OAuth app state overview (production readiness)", "https://developers.google.com/identity/protocols/oauth2/production-readiness/overview"),
        src(2, "Sensitive scope verification", "https://developers.google.com/identity/protocols/oauth2/production-readiness/sensitive-scope-verification"),
        src(3, "Using OAuth 2.0 for web server applications", "https://developers.google.com/identity/protocols/oauth2/web-server"),
        src(4, "OAuth 2.0 scopes for Google APIs", "https://developers.google.com/identity/protocols/oauth2/scopes", note="Only the first ~100k of ~165k characters were read in the re-fetch; the first pass searched the rest for calendar+sensitive and found nothing."),
        src(5, "Choose Google Calendar API scopes", "https://developers.google.com/workspace/calendar/api/auth"),
        src(6, "Manage app audience (Cloud Console Help)", "https://support.google.com/cloud/answer/15549945?hl=en"),
        src(7, "Submitting your app for verification (Cloud Console Help)", "https://support.google.com/cloud/answer/13461325?hl=en"),
        src(8, "Unverified apps / app verification (Cloud Console Help)", "https://support.google.com/cloud/answer/13463073?hl=en"),
    ],
    unknowns=[
        "Per-scope sensitivity classification for Calendar scopes (the docs say the Cloud Console shows it; no read page lists it per Calendar scope).",
        "The full redirect URI validation table on the web-server page (HTTPS requirement, raw IP, googleusercontent.com, shorteners, wildcards, etc.): the fetch tool truncated or paraphrased it, so it is not verified.",
        "The exact Cloud Console menu path for the consent screen (Audience seen; Branding and the Clients > Create Client button path not confirmed).",
        "Whether Trusted status also lifts the 100-test-user cap, and whether the 100-user cap on unverified apps is permanent or resettable (not found on any page read).",
        "That the privacy policy must be linked from the consent screen (not seen).",
        "Timeline and cost of the restricted-scope security assessment (no timeline found on the pages read).",
        "Whether step 1 (creating a Cloud project) is documented on the cited web-server page: no supporting text was retrieved.",
        "The last ~20k characters of the web-server page and the last ~65k of the scopes page were not read in the re-fetch.",
    ],
    review_notes=REVIEW_NOTES + [
        "Reconciled against a second verification pass on 2026-10-29: 22 claims confirmed, 7 corrected, 5 left unverified.",
    ],
)
