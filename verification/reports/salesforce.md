# Salesforce guide reconciliation (second pass, 2026-10-29)

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
