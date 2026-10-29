# HubSpot reconciliation report (2026-10-29)

All cited pages were re-fetched with WebFetch on 2026-10-29. Fetches return summaries, so quotes were only added where the returned text was a clear verbatim quote. Base URL: https://developers.hubspot.com/docs

| Claim | Before | Verdict | After | Evidence |
|---|---|---|---|---|
| Legacy public apps can't be created as of June 23, 2026 | V | confirmed | V, quote added | /api/creating-an-app: "As of June 23, 2026, legacy public apps can no longer be created." |
| CLI v7.6.0 asked for | V | confirmed | V, quote, note version may move | /apps/developer-platform/build-apps/create-an-app: "Make sure you're using v7.6.0 of the HubSpot CLI before proceeding." |
| Authenticate with hs account auth | V | confirmed | V | create-an-app: "`hs account auth` command" |
| hs project create, App, distribution/auth prompts | V | confirmed | V (distribution prompt wording not verbatim) | create-an-app (not re-read for this step) |
| Distribution/auth in app-hsmeta.json; Marketplace needs OAuth (step 3) | U | confirmed | V (S4) | build-apps/app-configuration: "The `distribution` field in your app schema allows you to configure how you want to distribute your app." and "ensure that you set the `type` within the `auth` property to `oauth`." |
| HTTPS redirect URL, localhost for testing | V | confirmed | V, quote | app-configuration: "Each app must have at least one auth redirect URL, and it must use HTTPS." / "The only exception is that `http://localhost` is allowed for testing." |
| Scope types; at least one scope; minimum read | V | confirmed | V, quote | app-configuration: "At a minimum, your app must include the `read` scope" |
| Unique uid in top-level app-hsmeta.json | V | confirmed | V (no quote; "before uploading" is paraphrase) | create-an-app: change the `uid` property of the app in top-level app-hsmeta.json |
| hs project upload triggers build | V | confirmed | V | create-an-app: "run the `hs project upload` CLI command" |
| hs project open, Auth tab, Client ID/secret | V | confirmed | V | create-an-app: "run `hs project open` from within your local project directory" |
| Install from Distribution tab | V | confirmed | V, quote | create-an-app: "On the *Distribution* tab, next to *Test installs*, click **Add test install(s)**." |
| Authorize URL and code exchange (step 9) | U | confirmed | V, new source S9 | /api-reference/latest/authentication/manage-oauth-tokens: "To get OAuth access and refresh tokens, make a URL-form encoded `POST` request to `/oauth/2026-09/token`." |
| Listing path, 7 tabs, Submit for review | V | confirmed | V, quote | build-apps listing-your-app page: "Click Submit for review in the top right." |
| At least 3 active unique installs, unaffiliated, 30 days | V | confirmed | V, quote ("30 days" paraphrase) | list-apps/listing-your-app/app-marketplace-listing-requirements: "your app must have at least three active, unique installs." |
| OAuth only, support contact, live Terms/Privacy, setup doc | V | confirmed | V | listing requirements: "You must include at least one support contact method." |
| Manual review, one app at a time, Partner Agreement | V | confirmed | V, quote | listing requirements: "App listing submissions are manually reviewed by the HubSpot Ecosystem Quality team." |
| Initial review 10 business days; process <= 60 days | V | confirmed | V, quote | listing requirements: "initial review within 10 business days" / "no more than 60 days" |
| Listing-process page gives no review timeline | V | confirmed | Moved to unknowns (absence claim) | listing-your-app: only timeline is unpublish requests, 10 business days |
| Request only needed scopes / use all at install | V | confirmed (half) | V for "only request scopes your app needs"; "use all at install" dropped | listing requirements: "only request scopes your app needs." |
| Sample scopes crm.objects.contacts.read/write | U | confirmed | V (no quote; summary of a sample file) | create-an-app sample app-hsmeta.json |
| hs project dev; localhost redirect | V | confirmed | V, quote; sample redirect https://localhost:3000/oauth-callback added | create-an-app: "you can run `hs project dev` to start developing your app locally." |
| Configurable test account, Add test install(s), unverified checkbox, Connect app | U (S5) | corrected | Add test install(s) = V on S3; checkbox/Connect app dialog stays U on S3; test-account creation and "unverified" wording dropped | create-an-app; install-flow page has none of the test-account text |
| Listing Preview / Edit draft runs test install | U (S7) | corrected | V on S5 for Preview; "Edit draft" path dropped | /list-apps/understand-app-install-flow: "Run through a test version of the installation process." |
| Certification details; optional | V | corrected | V without "optional" and without universal security assessment; browser-extension assessment added | /list-apps/apply-for-certification/certification-requirements: "Your app will be subjected to an additional security assessment if it includes a browser extension." |
| Legacy OAuth: domain required, no IP | U | confirmed | V, quote | /apps/legacy-apps/authentication/working-with-oauth: "You also must use a domain, as IP addresses are not supported." |
| redirect_uri must exactly match configured value | unknown | unsupported | stays in unknowns | not on legacy OAuth page or 2026-09 token page |
| Access-token lifetime | unknown | confirmed | unknown reworded; V fact that expires_in is returned | manage-oauth-tokens: "you can check the `expires_in` parameter when generating an access token to determine its lifetime (in seconds)." |
| Super Admin / Marketplace Access to install | U | confirmed | V (legacy guide, scoped as such) | legacy OAuth: "Users installing apps in their HubSpot account must either be a Super Admin or have HubSpot Marketplace Access permissions." |
| Unverified-app banner, domain verification, DNS 48h | U | unsupported | Removed from blockers; recorded in unknowns | install-flow page has no such text (re-fetched) |
| Draft mode, unsupported platform versions, classic CRM cards | U (S7) | corrected | V on S6; wording changed to "failing requirements sets Draft" | listing requirements: apps "cannot be listed in the HubSpot Marketplace"; classic CRM cards unsupported as of June 16, 2025 |
| Test installs need no review; certification separate/optional | estimate in prose | unsupported | Softened; moved to unknowns | no page states it |
| Tagline: 3 real installs first | V | confirmed | V | listing requirements |

## What I corrected
- Test-install text: re-attributed "Add test install(s)" to the create-an-app page, dropped test-account creation and the "unverified app" checkbox wording.
- Listing Preview moved to the install-flow page (S5); "Edit draft" menu path removed.
- Certification: removed "optional" and the blanket security-assessment claim; added the browser-extension assessment.
- Draft-mode/unsupported-version/classic-CRM-card blocker re-sourced to the listing-requirements page (S6), reworded to "failing the requirements".
- Approval summary no longer asserts that test installs need no review.
- Difficulty text softened for the same reason.

## What I upgraded to verified after re-fetching
- Step 3 (distribution field, OAuth auth type for Marketplace) from app-configuration.
- Step 9 (authorize URL, code exchange at /oauth/2026-09/token) using the new 2026-09 token page (added as S9).
- Legacy OAuth domain/no-IP rule and the Super Admin / Marketplace Access installer rule (legacy guide only).
- Sample contacts scopes; the expires_in fact; the October 26, 2026 install-experience notice (S5); the sample https://localhost:3000/oauth-callback redirect.

## What remains unverified / unknown and why
- The test-install dialog (checkbox then Connect app): the second-pass fetch did not return that text, so it stays unverified.
- Authorize query parameters (client_id, scope, redirect_uri): not re-read on the token page, so the guide says so.
- Exact redirect_uri matching and a redirect URL count limit: no page states them.
- Fixed token lifetime: none stated; read expires_in.
- Whether test installs are reviewed, and whether certification is optional: no page says.
- Unverified-app banner, domain verification, DNS delay, configurable test accounts: the cited page has none of it; a changelog entry (developer-identity-for-hubspot-apps) was not read.
- Developer-account signup: not covered by the pages read.
- Source S1 slug: the fetch worked at the old URL; search shows a newer slug (oauth-quickstart-guide). Noted on the source, not switched, because the new URL was not fetched.
