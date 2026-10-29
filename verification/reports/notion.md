# Notion reconciliation report (second pass, 2026-10-29)

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
