# GitHub guide reconciliation (2026-10-29)

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
