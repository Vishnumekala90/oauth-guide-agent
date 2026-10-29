# Slack reconciliation (second pass, 2026-10-29)

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
