# Google Calendar guide: reconciliation report (2026-10-29)

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
