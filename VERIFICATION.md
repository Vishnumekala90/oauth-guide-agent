# Verification record

How the six curated guides were checked, what changed, and what could not be confirmed.

## Method

1. **Research pass (2026-10-28).** An AI research agent read official provider documentation and drafted each guide.
2. **Independent check (2026-10-28).** A second pass re-checked **200 individual claims** against the cited pages and recorded a verdict for each in `verification/raw/*.json`.
3. **Reconciliation (2026-10-29).** One agent per provider applied the verdicts to the guide, **re-fetching the official page before promoting anything to "verified"**, and wrote the per-provider report below.

## Results across all six guides

| Verdict in the independent check | Claims |
|---|---|
| Confirmed | 143 |
| Corrected (wording fixed in the guide) | 32 |
| Unsupported (not shown as verified) | 23 |
| Unreachable (JS-rendered page, left unverified) | 2 |

Notable corrections and removals: Google "Trusted status lifts the 100-user cap" appeared on no page and was removed; HubSpot's "unverified-app banner" blocker was not on the cited page and was removed; Slack's signing-secret/mTLS requirement was downgraded; GitHub's "ten tokens per hour" became "ten tokens per user/application/scope"; Notion's "authorization URL locked until review" was overstated and softened; Salesforce's Dev Hub/scratch-org instruction was removed.

## Limits of this verification (read these)

- **Fetch tool, not a browser.** Pages were read through a summarizing fetch tool. When it did not return text verbatim, quotes were left out rather than reconstructed. Several JS-rendered pages (notably Salesforce help articles) could not be read; claims depending on them stay unverified.
- **Nothing was tested against a live provider account.** No OAuth app was created. "Verified" means *an official page supports the statement*, not *we ran it*.
- **Absence claims** ("the docs state no review time") are listed under `unknowns`, never as verified facts.
- **Effort figures are estimates** by us. Approval waits appear as numbers only where a source states them.
- Documentation changes; every guide carries its verification date.

---

## GitHub

GitHub guide reconciliation (2026-10-29)

Doc base: https://docs.github.com/en/ . Short names: CREATE = apps/oauth-apps/building-oauth-apps/creating-an-oauth-app; AUTH = .../building-oauth-apps/authorizing-oauth-apps; DIFF = .../building-oauth-apps/differences-between-github-apps-and-oauth-apps; S7 = organizations/managing-oauth-access-to-your-organizations-data/about-oauth-app-access-restrictions; CB = apps/creating-github-apps/registering-a-github-app/about-the-user-authorization-callback-url; RATE = .../building-oauth-apps/rate-limits-for-oauth-apps.

| Claim | Before | Verdict | After | Evidence |
|---|---|---|---|---|
| difficulty_explanation | prose | confirmed | unchanged | S7: "When you create a new organization, OAuth app access restrictions are enabled by default." ("no review" is an absence claim) |
| approval_wait | none_documented | confirmed | unchanged (absence, stays as is) | S7: "Users can request owner approval for OAuth apps they'd like to use."; no turnaround stated |
| prerequisites[0] account | verified | confirmed | verified, reworded to OAuth App + quote | CREATE: "under your personal account or under any organization you have administrative access to." |
| prerequisites[1] app type | verified | confirmed | verified + quote | DIFF: "GitHub Apps aren't subject to organization application policies." |
| prerequisites[2] callbacks | verified | confirmed | verified; "at least one" flagged as our reading | CREATE: "You can enter up to 10 callback URLs." |
| step-1 | verified | confirmed | unchanged | DIFF: "GitHub Apps use fine-grained permissions" |
| step-2 | verified | confirmed | unchanged | CREATE navigation steps (re-fetched, paraphrase) |
| step-3 | verified | confirmed | unchanged | CREATE: "Add callback URL" |
| step-4 | verified | confirmed | unchanged | CREATE: "Expire user access tokens" enabled by default |
| step-5 secret storage | unverified | unsupported | unverified; added to unknowns | AUTH re-fetch: no secret-storage guidance |
| step-6 authorize | verified | confirmed (wording corrected) | S256 only, PKCE recommended, redirect_uri optional | AUTH: "Must be `S256` - the `plain` code challenge method is not supported." |
| step-7 code exchange | verified | confirmed | verified + quote | AUTH: "The temporary code will expire after 10 minutes." |
| step-8 testing | unverified | unsupported | unverified | no official test procedure |
| callback[0] 10 URLs | verified | confirmed | verified + quote | "You can enter up to 10 callback URLs." |
| callback[1] exact/wildcard | verified | confirmed (wording imprecise) | host "excluding subdomains" fixed; recommendation to disable wildcard added | CB: "the redirect URL's host (excluding subdomains) and port must exactly match the callback URL" |
| callback[2] Aug 3 2026 | verified | corrected | not limited to GitHub Apps; cites S5 and S2 | CB: "Apps that had a single callback URL enabled prior to August 3, 2026 have wildcard matching enabled..." (also on AUTH) |
| callback[3] native loopback | unverified | confirmed | verified (S2) | AUTH: "instead to use loopback literal `127.0.0.1` or IPv6 `::1`" |
| callback[4] HTTPS | unverified | confirmed (absence) | unverified (absence stays); in unknowns | AUTH: no HTTPS requirement stated |
| scopes[0] repo | verified | confirmed | verified + quote | SCOPES: "including projects, invitations, team memberships and webhooks." |
| scopes[1] user/org/workflow | verified | confirmed | read:org wording expanded (org projects) | "Grants the ability to add and update GitHub Actions workflow files." |
| scopes[2] GitHub App perms | verified | confirmed | verified + quote | REGISTER: "The permissions that you selected in the previous step determine what webhook events are available." |
| testing[0] | verified | confirmed | verified + quote | AUTH: "Non-web authentication is available for limited situations like testing." |
| testing[1] revoke repeats consent | unverified | unsupported | unverified; in unknowns | page says users can revoke, not that consent repeats |
| publishing[0] | verified | confirmed | verified + quote | S7 quote above; S7 also says organization owners receive a notification of pending requests (summary-level) |
| publishing[1] | verified | confirmed | verified + quote | DIFF: "A GitHub App only has access to the repositories an organization owner has granted." |
| blockers[0] org blocks | verified | confirmed | unchanged | DIFF: "only an organization owner can authorize the installation of an OAuth app." |
| blockers[1] expiring tokens | verified | confirmed | unchanged | AUTH: "The access token expires after eight hours, and the refresh token expires after six months without use." |
| blockers[2] code lifetimes | verified | confirmed | unchanged | AUTH: "The default is 900 seconds or 15 minutes." |
| blockers[3] 100 apps | verified | confirmed | unchanged | CREATE: "up to 100 OAuth apps" |
| blockers[4] ten tokens/hr | unverified | corrected | verified: ten tokens per user/application/scope (not "per hour"), plus 2,000 token requests/hour (new S8) | AUTH: "There is a limit of ten tokens that are issued per user/application/scope combination"; RATE: "OAuth apps are subject to a rate limit of 2,000 access token requests per hour." |
| blockers[4] 5,000 req/hr | unverified | unsupported | unverified; moved to unknowns | RATE does not mention it |
| unknowns[0] HTTPS | unknown | confirmed (absence) | unchanged | AUTH has no HTTPS requirement |

## What I corrected
- Authorize step: PKCE method must be S256, PKCE is recommended not required, redirect_uri is optional.
- Wildcard matching: host match excludes subdomains (any subdomain matches); GitHub recommends disabling wildcard if unneeded.
- Aug 3, 2026 wildcard sentence applies to apps generally (appears on both the GitHub App and OAuth pages).
- "Ten tokens per hour" replaced with ten tokens per user/application/scope; separate 2,000 token requests/hour and ten sign-ins/hour limits.
- Prerequisite account wording restricted to OAuth Apps.
- Source S2 note: the suggested canonical path /using-oauth-apps/authorizing-oauth-apps returned a different page without the expiry text, so the building-oauth-apps URL was kept.

## What I upgraded to verified after re-fetching
- Native-app loopback redirect (port need not match; 127.0.0.1 / ::1): re-fetched AUTH and saw the loopback text. (Port sentence itself came from the verification pass; my fetch showed the loopback literal wording.)
- Token limits blocker (ten-token limit and 2,000/hour) via AUTH and the newly added S8 RATE page.
- New verified facts: users can edit requested scopes and X-OAuth-Scopes header shows granted scopes; scopes page suggests a GitHub App instead.

## What remains unverified / unknown and why
- Client secret should live server-side (step 5): good practice, but neither fetched page says it.
- 5,000 requests/hour shared limit: not on the OAuth rate-limit page; REST rate-limit page not fetched.
- Revoking an authorization repeating the consent screen; test procedure (step 8): not documented on pages read.
- HTTPS requirement for callbacks, GitHub review/Marketplace requirements, owner approval turnaround: absent from pages read.
- GitHub App owner wording ("organization you own") was not re-fetched by me.
- Fetches go through a summarizing tool, so quotes are used only where they matched the raw pass or came back as clearly verbatim strings.

---

## Google Calendar

Google Calendar guide: reconciliation report (2026-10-29)

Raw pass: `verification/raw/google-calendar.json` (34 claims: 22 confirmed, 7 corrected, 5 unsupported, 0 unreachable). Re-fetch on 2026-10-29 used WebFetch (a summarizing fetch tool; quotes below are as it returned them).

Base URLs: S1 = developers.google.com/identity/protocols/oauth2/production-readiness/overview; S2 = .../production-readiness/sensitive-scope-verification; S3 = .../oauth2/web-server; S6 = support.google.com/cloud/answer/15549945; S7 = support.google.com/cloud/answer/13461325; S8 = support.google.com/cloud/answer/13463073 (new source).

| Claim | Before | Verdict | After | Evidence |
|---|---|---|---|---|
| approval_wait 3-5 business days | documented | confirmed | unchanged, full quote added | S2: "The sensitive scope verification process typically takes 3-5 business days to complete." |
| automated brand review a few minutes | in summary | confirmed | unchanged | S2: "The automated review usually completes in a few minutes." |
| restricted-scope timeline not stated | in summary | unsupported (absence) | kept as absence; added to unknowns | no timeline on pages read |
| effort ~3-6 h | estimate | unsupported | unchanged (labelled estimate) | none; author estimate |
| 100 test users; 7-day expiry (difficulty text) | prose | confirmed | unchanged | S6: "Authorizations by a test user will expire seven days from the time of consent." |
| verification needs domain, homepage, privacy policy, justification, video | prose | confirmed | unchanged | S2 quotes below |
| Calendar scope sensitivity not confirmed | prose | unsupported | stays unverified/unknown | S5 and S4 never use the labels |
| prereq: Cloud project + Calendar API enabled | unverified | confirmed | verified (reworded to API enablement) | S3: "Any application that calls Google APIs needs to enable those APIs in the API Console." |
| prereq: domain, homepage, privacy policy | verified | confirmed (partial) | verified, reworded: privacy policy same domain as home page; "linked from consent screen" dropped | S2: "Verify ownership of your project's authorized domains within the Google Search Console." ; "hosted within the same domain as your application's home page" |
| prereq: justification + unlisted video | verified | confirmed | verified, quote added | S2: "Upload the video to YouTube Studio and set its Visibility as Unlisted." |
| step-1 create project | unverified | unsupported | unverified (unchanged), added to unknowns | none retrieved |
| step-2 enable Calendar API | unverified | confirmed | verified ("API Library" wording removed) | S3 quote above |
| step-3 consent screen, narrow scope | unverified | confirmed (partial) | unverified; quote added; note Branding menu not seen | S5: "Generally, you should choose the most narrowly focused scope possible" |
| step-4 Web application client | unverified | confirmed (partial) | unverified; "HTTPS" removed from text | S3: "Select the Web application application type." |
| step-5 access_type=offline | unverified | confirmed | verified | S3: set `offline` if the app needs to refresh access tokens (tool-truncated, no quote used) |
| step-6 test users, 7 days | verified | confirmed | verified, quote added | S6 7-day quote; "Google will display a warning message before allowing a specified test user to authorize scopes." |
| step-7 publish first | verified | confirmed | verified, quote added | S7: "Apps in development, testing or staging are not applicable for verification." |
| step-8 submit; email owners/editors "only" | verified | corrected | "only" dropped | S7: "will occur over email to the project owners and project editors configured when setting up your project." |
| callback[0] HTTPS-only etc. | verified | corrected | split: localhost http allowed (verified); rule table (HTTPS, raw IP, googleusercontent, shorteners, wildcards...) demoted to unverified | S3: "For testing, you can specify URIs that refer to the local machine, such as http://localhost:8080." Table not reproducible on re-fetch (truncated) |
| callback[1] localhost unknown | unverified | corrected | replaced by the verified localhost fact | S3 quote above |
| scopes[0] 17 scopes | verified | confirmed | verified; added that Calendar auth page lists 20 (add-on scopes) | re-fetch counted 17 in S4 (first 100k chars); S5 lists 20; S4: "Make secondary Google calendars, and see, create, change, and delete events on them" |
| scopes[1] classification | unverified | unsupported | unverified; new verified fact that Cloud Console shows the category | S8: "scope categories (non-sensitive, sensitive, or restricted) are indicated automatically in the Google Cloud Console" |
| testing[0] 100 test users | verified | confirmed | verified, cited S6 (was S1) | S6: "limited to up to 100 test users listed in the OAuth consent screen." |
| testing[1] 7-day, exempt, Trusted overrides expiry and cap | verified | corrected | split; Trusted overriding 7-day kept (S1); Trusted lifting 100-user cap removed, noted unknown | S1: "the 7-day refresh token expiration limit for apps in the Testing status" ; S6 exception for userinfo.email, userinfo.profile, openid |
| publishing[0] verification required | verified | confirmed | verified, re-cited S1 (was S2) | S1: "Required for public apps that request sensitive and restricted scopes." |
| publishing[1] hard lifetime cap, cannot be reset | verified | corrected | "lifetime"/"cannot be reset" removed | S1: "a hard cap of 100 total users applies." |
| publishing[2] Testing not eligible | verified | confirmed | verified, quote added | S7 quote above |
| publishing[3] security assessment | verified (cited S2) | confirmed | verified, re-cited S7 | S7: "the OAuth review team will reach out to you when it's time to start the security assessment." |
| blocker 7-day tokens | verified | confirmed | verified, adds S1 | S1 7-day quote |
| blocker 100-user cap | verified | corrected | "for its lifetime" removed | S1 cap quote |
| blocker narrow scopes | verified | confirmed | verified; "invites questions" labelled our inference | S2: "You must request scopes that require the least amount of access to user data necessary to provide that functionality." |
| blocker owners/editors, 7 days | verified | corrected | reworded: results valid 7 days, keep roles current; "only" and "must act within 7 days" dropped | S2: "Compliant verification results are valid for 7 days." ; "Keep the owner and editor roles of your project's associated accounts current," |
| blocker home page | verified | confirmed | unchanged | S2: "Links to your app's listing on the Google Play Store or its Facebook page aren't considered valid application home pages." |
| tagline | n/a | confirmed | unchanged | S1 "Required for public apps..." |

## What I corrected
- Step 8 / email blocker: dropped "only" and "must act within 7 days"; replaced with the page's wording (email with owners and editors; compliant results valid 7 days).
- Redirect URIs: the original "must use HTTPS" statement was wrong as stated (localhost http is allowed for testing). The verified fact is now the localhost sentence.
- Testing/Trusted: removed the claim that Trusted lifts the 100-user cap (not found anywhere).
- 100-user cap: removed "lifetime" and "cannot be reset".
- Restricted-scope assessment and verification-required facts re-cited to the page that actually supports them (S7, S1).
- Prerequisite wording: removed "linked from the consent screen"; added same-domain privacy policy and the Play/Facebook exclusion.

## What I upgraded to verified after re-fetching
- Calendar API enablement (prerequisite and step 2), S3 quote seen.
- Step 5 (access_type=offline for refresh tokens), seen in S3 though the tool's quote was truncated.
- New verified facts: Cloud Console shows scope categories (S8); apps with only non-sensitive scopes need not complete verification, brand verification is lighter (S8); refresh tokens valid until revoked or expired (S3); Calendar auth page lists 20 scopes incl. add-on scopes (S5).

## What remains unverified / unknown and why
- Redirect URI validation table (HTTPS, raw IP, googleusercontent.com, shorteners, wildcards, fragments, userinfo, path traversal, public suffix list): both fetches returned the page truncated at the table or paraphrased it; kept as an unverified fact.
- Per-scope sensitivity/restriction for Calendar scopes: no read page lists it (Cloud Console shows it).
- Step 1 (create project), step 3 menu details (Branding), step 4 "Create Client" path: no supporting text retrieved.
- Whether Trusted lifts the 100-user cap; whether the unverified 100-user cap is permanent.
- Privacy policy linked from consent screen.
- Restricted-scope security assessment timeline and cost: absence claim only.
- Effort estimate (3-6 h): author estimate, labelled as such.
- Last ~20k chars of the web-server page and ~65k of the scopes page were not read in the re-fetch. No claims were unreachable.

---

## Slack

Slack reconciliation (second pass, 2026-10-29)

All seven pages in the raw file were re-fetched with WebFetch (a summarizing tool; quotes below are the fragments it returned). S1 = installing-with-oauth, S2 = quickstart-app-settings, S3 = distribution, S4 = review guide, S5 = guidelines-and-requirements, S6 = using-token-rotation, S7 = changelog/2026/03/30/pkce.

| Claim | Before | Verdict | After | Evidence |
|---|---|---|---|---|
| prerequisites[0] dev workspace | verified S2 | confirmed | unchanged | S2 "Select the Workspace where you'll be developing your app." |
| prerequisites[1] HTTPS redirect, SSL URLs | verified S1,S3 | confirmed | unchanged | S1 "The `redirect_uri` must use HTTPS."; S3 "Your app must support SSL for all of the following URLs:" |
| prerequisites[2] 10+ active workspaces / 28 days | verified S4 | confirmed | unchanged, quote added | S4 "Your app has been installed on 10 or more active workspaces" |
| prerequisites[2] landing/support/privacy pages | cited S4 only | corrected | S5 added as source | S5 "All Slack Marketplace apps must include a clear privacy policy..."; "your landing page needs to be publicly accessible" |
| step-1 create app | verified; "Create New App", new_app=1 URL | corrected | reworded to "Create an app", URL removed | S2 "Select Blank app. Click Continue." |
| step-2 scopes + Redirect URL | verified S1,S2 | confirmed | unchanged | S1 Redirect URL under App Management; S2 OAuth & Permissions scopes (S2 not re-quoted on Redirect URL) |
| step-3 install | verified S2 | confirmed | quote added | S2 "You'll see an access token under OAuth Tokens." |
| step-4 authorize URL | verified S1 | confirmed | quote added | S1 "provide a `user_scope` parameter ... instead of, or in addition to, the `scope` parameter." (client_id/state are paraphrase) |
| step-5 callback, 10 min | verified S1 | confirmed | unchanged | S1 "...temporary authorization code, which expires after ten minutes." |
| step-5 multi redirect_uri | verified S1 | confirmed | unchanged | S1 bad_redirect_uri sentence (see callback[1]) |
| step-6 distribution | verified S3 | confirmed | quote added | S3 "Activate Public Distribution" |
| step-7 test on non-dev workspace | verified S4 | confirmed | quote added | S4 "We cannot access any Slack workspaces (even created for testing)" |
| step-8 images 1600x1000 | verified S4,S5 | confirmed (S5) | unchanged | S5 "Use a 1600px by 1000px size (8:5 ratio)." |
| step-8 description <=10 words | verified | confirmed | unchanged | S5 "keep it short and sweet at 10 words (or fewer)" |
| step-8 demo video | verified | confirmed | detail clarifies S4 vs S5 | S4 "a video showing the full installation and OAuth flow"; S5 only "strongly recommend" |
| step-8 collaborator | verified | confirmed | quote added | S5 "You must add a collaborator to your app." |
| callback[0] HTTPS/match/anchor | verified S1 | confirmed | quote added | S1 "must match or be a subdirectory of a Redirect URL..."; "can not contain an anchor (#)" |
| callback[1] same redirect_uri | verified S1 | confirmed | quote replaced with re-fetched wording | S1 "`bad_redirect_uri`: Occurs when there are multiple `redirect_url` parameter values configured and they do not match." |
| scopes[0] scope/user_scope, additive | verified S1 | confirmed | quote added | S1 "It is not possible to downgrade an access token's scopes." ("additive" sentence not returned by re-fetch; "no way to remove scopes ... without revoking" was) |
| scopes[1] Marketplace scope rules | verified S4,S5 | corrected | rewritten, S5 only | S5 "We are unlikely to approve broad access to workspace message/file data" |
| testing[0] | verified S2 | confirmed | quote added | S2 "Install your app by selecting the Install to Workspace button." |
| testing[1] | verified S4 | confirmed | unchanged | S4 video + test accounts quotes |
| publishing[0] | verified S3 | confirmed | quote added | S3 "you cannot disable distribution in this way once your app is published within the Slack Marketplace" |
| publishing[1] review timelines | verified S4 | confirmed | quote added | S4 "up to 10 weeks for new submissions and 6 weeks for published apps resubmitting changes"; "unable to skip or accelerate" |
| publishing[2] TLS/state/signing secret/mTLS | verified S4 | corrected | split: TLS+state verified (S5); signing secret/mTLS downgraded to unverified | S5 "your app must use the state parameter when requesting access to customer data during the OAuth flow"; only "The signing secret should be protected like a password." |
| publishing[3] admin/Marketplace-only | verified S3 | confirmed | quote added | S3 "Some workspaces will restrict app installation so that only workspace administrators can provide authorization." |
| blockers[0] bad_redirect_uri | verified S1 | confirmed (half) | detail narrowed to documented case | S1 multiple redirect values that do not match; plain mismatch with configured URL not quoted |
| blockers[1] 10 active installs | verified S4 | confirmed | unchanged | S4 "We will return submissions that are not ready for review." Pilot advice is ours, not Slack's |
| blockers[2] granular permissions | verified S4 | confirmed | unchanged | S4 "Upgrading to granular permissions is a fundamental change to your app." "cannot be undone." |
| blockers[3] new scopes re-review | verified S4 | confirmed | unchanged | S4 "Adding new scopes to your app" (video demo/test app) |
| blockers[4] admin approval | verified S3 | confirmed | unchanged | S3 same admin sentence; no timing |
| approval_wait | documented | confirmed | unchanged | S4 "the functional review takes up to 10 weeks for new submissions"; "no review for own install" is absence-of-statement |
| difficulty_explanation | prose | confirmed | unchanged | S4 10+ workspaces; pages from S5, video from S4 |
| effort ~1-3 h | estimate | unsupported | stays labelled estimate; added to unknowns | no official source |
| agent_can_do "under 10 words" | "under 10" | corrected | "10 words or fewer" | S5 "10 words (or fewer)" |
| unknowns[0] localhost | unknown | corrected | rewritten; PKCE fact added as verified | S7 "Desktop redirects (custom URI schemes and localhost redirects for PKCE-enabled apps) cannot request bot scopes." S1 does not mention localhost |
| unknowns[1] max Redirect URLs | unknown | unsupported | stays unknown | S1 re-fetch: no maximum stated |
| unknowns[2] rate limits | unknown | unsupported | stays unknown | not on fetched pages |
| unknowns[3] token rotation | unknown | corrected | removed from unknowns; verified fact added; "mandatory for Marketplace?" kept unknown | S6 "Token rotation may not be turned off once it's turned on."; "With token rotation, it expires every 12 hours." |
| unknowns[4] admin approval time | unknown | confirmed | unchanged | S3 no timing |

## What I corrected
- Step 1: dropped "Create New App" and the `?new_app=1` URL (page says "Create an app"; URL not on page).
- Landing/support/privacy prerequisite now also cites S5.
- Marketplace scope rule: "extensive-data scopes not permitted" was too strong; now "unlikely to approve broad access to message/file data"; legacy/restricted prohibited; source S5 only.
- TLS 1.2 and state parameter re-attributed to S5; signing secret/mTLS requirement downgraded to unverified.
- bad_redirect_uri blocker narrowed to the documented condition.
- "under 10 words" changed to "10 words or fewer".
- Unknowns for localhost and token rotation rewritten.

## What I upgraded to verified after re-fetching
No existing unverified fact was upgraded (all were already verified). Newly added verified facts after re-fetch: PKCE enable-in-settings, one-way, 30-day refresh tokens, desktop/localhost redirect limits (S7); token rotation opt-in, irreversible, 12-hour tokens, Marketplace Published App Settings (S6). New sources S6, S7. Quotes added to 15 items. Caveat: the fetch tool summarizes, so quotes are fragments; two earlier-recorded quotes ("additive to the scopes you've already been awarded", "otherwise, you will encounter a bad_redirect_uri error") were not returned verbatim on re-fetch and were not used.

## What remains unverified / unknown and why
- Signing secret or mTLS requirement (unverified fact): S5 gives only related sentences.
- Effort estimate (~1-3 h): our own estimate.
- Max number of Redirect URLs, rate limits, admin-approval timing: not stated on fetched pages.
- Plain localhost redirects for non-PKCE apps: not addressed; S1 requires HTTPS.
- Token rotation being mandatory for Marketplace apps: S6 says only "can have".
- "No Slack review for own install" is an absence claim, kept as consistent with S2/S3 but not quoted.

---

## HubSpot

HubSpot reconciliation report (2026-10-29)

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

---

## Notion

Notion reconciliation report (second pass, 2026-10-29)

All five pages (authorization, public-connections, marketplace-listing, capabilities, create-a-token) were re-fetched with WebFetch on 2026-10-29. Quotes below are as returned by the fetch tool.

| Claim | Before | Verdict | After | Evidence |
|---|---|---|---|---|
| Authorization URL field populates after submission (tagline, difficulty, step-4, publishing[0]) | verified | confirmed | verified, tagline/difficulty softened, quote added | /guides/get-started/authorization: "The Authorization URL field populates after a public connection is submitted for review" (image caption) |
| Blocker: cannot hand out URL until review | verified, "locked" | corrected | reworded: field empty until submission; docs silent on earlier use | same page |
| Prereq: portal + dev workspace | verified | confirmed | verified | public-connections: "Connection name and development workspace" |
| Prereq: redirect URIs | verified | confirmed | verified | "Redirect URI(s) for the OAuth flow" |
| Prereq: installation scope permanent, Marketplace eligibility | verified | confirmed | verified, quote added | "Installation scope is set once, at creation time, and can't be changed afterward." |
| Step 1 portal navigation | verified | confirmed | verified + quote | "In the Build section of the sidebar, select Public connections." |
| Step 2 form fields | verified | confirmed | verified + quote | "Click Create new connection and fill in the required fields, including:" |
| Step 3 credentials on Configuration tab | verified | confirmed | verified + quote | "After creation, visit the Configuration tab to retrieve your OAuth client ID and OAuth client secret." |
| Step 4 auth URL params | verified | confirmed | verified + quote | authorization: "Always use user." |
| Step 5 token exchange Basic auth | verified | confirmed | verified + quote | "The request is authorized using HTTP Basic Authentication." |
| Step 6 refresh returns new pair | verified | confirmed | verified + quote | "Refreshing an access token will generate a new access token and a new refresh token." |
| Step 7 Marketplace flow | verified | confirmed | verified + quote | marketplace-listing: "If changes are required, the Notion team sends feedback and you can resubmit after making updates." |
| callback[0] redirect_uri requirement | verified | confirmed | verified + quote | authorization: "If there are more than one redirect URIs included in your connection settings, this field is required." |
| callback[1] no redirect URI format rules | unverified | unsupported (absence) | unverified, also in unknowns | not stated on S1, S2, create-a-token |
| scopes[0] capabilities list | verified | confirmed | verified + quote | capabilities: "No user information, User information without email addresses, User information with email addresses" |
| scopes[1] capability change re-auth | verified | confirmed | verified + quote | "users will need to re-authenticate with a connection if the capabilities are changed" |
| testing[0] no testing mode / dev workspace use | unverified | unsupported | split: individual-auth sentence verified; testing/dev-workspace stays unverified | authorization: "each prospective user needs to individually follow the auth flow for the connection." |
| publishing[1] Marketplace 5-10 business days, rejections | verified | confirmed | verified | marketplace-listing: "expect to hear back from our team within 5-10 business days via email." |
| approval_wait 5-10 days (listing only) | documented | confirmed | unchanged | same; page does not tie it to connection review |
| blockers[1] scope permanent | verified | confirmed | verified | public-connections quote above |
| blockers[2] selected-workspace not listable | verified | confirmed | verified | "Only public connections with an installation scope of Any workspace can be listed on the Marketplace." |
| blockers[3] capability change re-consent | verified | confirmed | verified | capabilities quote above ("users", not "every user") |
| blockers[4] each user authorizes; no workspace-wide grant | verified | corrected | reworded; inference dropped; added "only that user can interact" (S2) | public-connections: "After a user authorizes a public connection, only that user can interact with the connection in their workspace." |
| difficulty_explanation | n/a | confirmed | "no timeline" softened to "none found on the pages read" | authorization page silent |
| effort ~1-3 h | estimate | unsupported | kept labelled estimate; added to unknowns | no source |
| unknowns[1] dev workspace use before review | unknown | unsupported | stays unknown | no official page says |

## What I corrected
- Blocker "Authorization URL locked until review" overstated the docs; now says the portal field is empty until submission and the docs do not say whether the flow works earlier.
- Blocker "each user authorizes individually" dropped the inferred "no shared workspace-wide grant"; replaced with two stated facts (S1, S2).
- Tagline and difficulty text softened to match; "no timeline" now "none found on the pages read".

## What I upgraded to verified after re-fetching
No fact changed from unverified to verified. Re-fetch confirmed these pieces, added as new verified facts: the individual-auth sentence (split out of the testing item); Notion-Version/Content-type headers and token-pair storage (S1); page picker and partial-authorization caveat (S1); Create a token redirect_uri rule (new source S5). For the S5 item the fetch returned only a summary of the "not allowed" conditions ("This field is not allowed in the request body if:" plus conditions paraphrased), so the guide hedges and defers to the page; the quote used is "In most cases, the `redirect_uri` field is required." Verbatim quotes were added to most facts/steps.

## What remains unverified / unknown and why
- Redirect URI format rules (HTTPS/localhost): not on any page read.
- Whether the connection works in the development workspace before review, and what "review" means or how long it takes: no official page says; the 5-10 business days is documented only for the Marketplace listing.
- The 1-3 h effort figure: our own estimate.
- Formal approval criteria (baseline connection criteria / Best Practices pages not read).
- Note: the Authorization URL caption is an image caption, not body text.

---

## Salesforce

Salesforce guide reconciliation (second pass, 2026-10-29)

Re-fetched with WebFetch on 2026-10-29: S1, S2, S3, S4 (eca-create), S5, S6, S7, S8, and the hosted-MCP page (new S11). All returned content matching their titles. S9 and S10 were not re-fetched (raw pass: JS shell only); they stay unreachable.
Totals: 20 confirmed, 10 corrected, 4 unsupported, 2 unreachable (36 claims).

| Claim | Before | Verdict | After | Evidence |
|---|---|---|---|---|
| difficulty_explanation[1] Spring '26 no new CAs | verified | confirmed | verified; S3 'restricted' wording added | S1 "As of Spring '26, new Connected Apps cannot be created." (S3: "Connected apps creation is restricted as of Spring '26.") |
| difficulty_explanation[2] mostly admin config; weeks of review | prose | unsupported | labelled "Our judgement" | Author characterisation; no page states it |
| effort ~3-6 h | estimate | unsupported | unchanged, estimate | No official figure |
| approval_wait 1-2 / 3-4 / 2-3 weeks | verified | confirmed | verified, quote added | S8 "The time frames are estimates." |
| approval_wait: no review in own org | stated as fact | unsupported | reworded as absence of evidence; added to unknowns | None |
| approval_wait: no end-to-end duration | stated | confirmed (absence) | kept as "not seen" | S8 per-stage estimates only |
| prerequisites[0] App Manager path | verified | confirmed | verified, quote; button label dropped | S4 "From Setup, in the Quick Find box, enter App Manager, and then select App Manager." |
| prerequisites[1] ECA required | verified | confirmed | verified | S1 quote above |
| prerequisites[2] ISV, Partner Console, scanners, fee | verified | corrected | split: enrollment/scanners fact; fee fact "unless free"; "provider profile" removed | S8 "If you plan to distribute your solution for free, you don't pay the fee." |
| step-1 Local/Packaged | verified | confirmed | verified, quote; "contact email" removed | S4 "To develop an external client app for your local org, select Local." |
| step-2 Enable OAuth | verified | confirmed | verified, quote | S4 "check Enable OAuth Settings." |
| step-3 secret / JWT | unverified | confirmed | verified; "server-side usually keep secret" removed (to unknowns) | S4 "Uncheck Require Secret for Web Server Flow." |
| step-4 Permitted Users | verified | confirmed | verified, cites S7 only, click sequence caveated | S7 "Admin approved users are pre-authorized." |
| step-5 token lifetimes | verified | confirmed | verified; 90 days = best-practice maximum | S5 "Setting a maximum of 90 days for the refresh token expiration is a security best practice." |
| step-6 no username-password flow | unverified | confirmed | verified, now cites S6; generic flow sentence dropped | S6 "External client apps don't support username-password flow." |
| step-7 packaging / four controls | verified | corrected | scoped controls; DevHub/PBO claim removed; client-key-only kept | S2 "share the client key in the submission documents only"; S1 scope >2 customer prod orgs |
| callback[0] any URL / localhost | verified | confirmed | verified, quote | S4 "Set Callback URL to any URL string, real or fictional" |
| callback[1] exact-match/HTTPS unknown | unverified | corrected | exact-match verified via new S11; HTTPS stays unverified | S11 "Make sure the callback (redirect) URL in your client exactly matches what is configured in Salesforce." |
| scopes | verified | confirmed | verified, quote | S4 "Access the identity URL service" |
| testing[0] | verified | confirmed | verified, quote | S5 "Your external client app is ready to use." |
| publishing[0] Permitted Users / Use Any API Client | verified | confirmed | verified, quote | S7 "If users have the Use Any API Client permission, they can access any external client app." |
| publishing[1] review required; ECAs packaged "in most cases" | verified | corrected | "should be packaged"; mandatory for auth-code (ISV-controlled callbacks) and Canvas | S2 "CAs and ECAs should be packaged for distribution on AppExchange." |
| publishing[2] review estimates | verified | confirmed | verified, quote | S8 "The time frames are estimates." |
| publishing[3] four controls enforced May 11 | verified | corrected | partner deadline, scope, names, no extension program; enforcement start unconfirmed | S1 "As of now, there are no plans for a formal extension program." |
| blockers[0] no new CA | verified | corrected | Dev Hub sentence removed; Support route and existing-apps added | S3 "If you must continue creating connected apps, contact Salesforce Support." |
| blockers[1] migration limits | verified | corrected | rewritten with fixable vs non-migratable cases, username-password caveat | S6 "Migration preserves your consumer key and secret, so existing integrations continue to work." |
| blockers[2] lockout | verified | confirmed | verified | S7 "anyone using the app loses access" (remedy is our advice) |
| blockers[3] credentials | verified | confirmed | verified | S2 "Submit credentials for integrations, including web apps and REST APIs, to avoid delays in the security review." |
| blockers[4] failed review | verified | confirmed | verified ("updated scans" detail not seen, not relied on) | S8 "You can't list your solution on AgentExchange or distribute it to customers." |
| sources[9] article 005228017 | low-conf source | unreachable | unchanged; note says unreachable | JS shell |
| sources[10] release note | low-conf source | unreachable | unchanged; note says unreachable | JS shell |
| unknowns[0] re-enable creation | unknown | corrected | Support route documented; self-service setting still unknown | S3 "If you must continue creating connected apps, contact Salesforce Support." |
| unknowns[1] names of four controls | unknown | corrected | removed from unknowns, now in publishing | S1 "OAuth PKCE, Refresh Token Rotation, Refresh Token Idle time-to-live (TTL), and Refresh Token IP Allowlist" |
| unknowns[2] fee amount | unknown | confirmed | still unknown; fee-waiver for free noted | S8 fee sentence |
| unknowns[3] propagation delay | unknown | unsupported | stays unknown | none |
| unknowns[4] HTTPS/exact-match | unknown | corrected | exact-match verified (S11); HTTPS unknown | S11 quote above |

## What I corrected
- Fee: "a fee applies" became "unless you distribute for free"; "provider profile" removed (not on page).
- Four controls: now a partner deadline with scope (more than two customer production orgs), named controls, and no claim that enforcement started.
- Packaging: "must in most cases" became "should", mandatory for authorization code flow with ISV-controlled callbacks and Canvas.
- Blockers: removed the unsupported Dev Hub/scratch-org sentence; migration list split into fixable and non-migratable; username-password caveat added.
- Step 7: removed the unfound DevHub/PBO instruction; step 4: removed the unconfirmed "Create then Edit" and contact-email details.

## What I upgraded to verified after re-fetching
- Step 3 (secret requirements/JWT) and step 6 (no username-password flow), plus the callback exact-match fact (new S11). Quotes were added to most facts. Added missing items: four control names/scope, packaging conditions, migration username-password limitation.

## What remains unverified / unknown and why
- S9 and S10 (JS-rendered, unreachable): "disabled by default" wording and any self-service re-enable setting.
- Own-org review absence, effort figure, and "mostly admin configuration" are our judgement or absence of evidence.
- HTTPS callback rule, fee amount, propagation delay, secret guidance for server-side apps, click-sequence/button labels, and where to create the ECA for packaging: not on any page read.
- The S2 fetch summary did not reliably list JWT Bearer among mandatory-packaging flows (raw pass said it did), so the guide cites only auth code and Canvas.
- Whether the May 11 enforcement actually began: the FAQ predates the deadline.

---

