"""Seed guide: salesforce. Edit only this file when reconciling this provider."""
from __future__ import annotations

from ._common import *  # noqa: F401,F403
from ._common import D, REVIEW_NOTES, V, U, st, bl, src
from ..models import ApprovalWait, Blocker, EffortEstimate, Guide

# =========================================================================== Salesforce
GUIDE = Guide(
    id="salesforce", slug="salesforce", provider_name="Salesforce", category="CRM",
    tagline="New integrations use External Client Apps; AppExchange distribution adds a multi-week security review.",
    website="https://developer.salesforce.com", generated_by="seed", verified_on=D, overall_confidence="medium",
    difficulty="hard",
    difficulty_explanation=(
        "Salesforce states that as of Spring '26 new Connected Apps cannot be created and new integrations must use External Client Apps (ECAs); one Salesforce page words it as 'restricted', with a Support route. "
        "Our judgement: using your own org is mostly admin configuration, while distributing to customers adds packaging, ISV Partner Program enrollment and an AppExchange security review whose stated estimates run to several weeks. "
        "The Spring '26 release note itself could not be read."
    ),
    effort=EffortEstimate(short_label="~3–6 h hands-on (estimate)", min_hours=3, max_hours=6,
                          rationale="ECA creation, OAuth settings and policies for a single org plus the flow code. Packaging and security-review preparation (scanner runs, disclosures) is a separate, larger effort not included."),
    approval_wait=ApprovalWait(
        short_label="Weeks (AppExchange review)", status="documented",
        summary=("Inside your own org no Salesforce review step was found in the pages we read; your admin's policy settings govern access (this is an absence of evidence, not a Salesforce statement). For AppExchange, Salesforce's security-review page gives estimates: verification 1–2 weeks, first-time testing 3–4 weeks, resubmission testing 2–3 weeks. No end-to-end duration was seen on the page, and it says 'The time frames are estimates.'"),
        source_ids=["S8"], quote="The time frames are estimates."),
    prerequisites=[
        V("A Salesforce org where an admin can create External Client Apps, started from Setup → Quick Find → App Manager.", "S4",
          quote="From Setup, in the Quick Find box, enter App Manager, and then select App Manager."),
        V("New integrations must use an External Client App; new Connected Apps cannot be created as of Spring '26 (S1). The Mobile SDK page words it as 'Connected apps creation is restricted as of Spring '26' and says to contact Salesforce Support if you must continue creating them (S3).", "S1", "S3",
          quote="As of Spring '26, new Connected Apps cannot be created."),
        V("For AppExchange: ISV Partner Program enrollment, Partner Console connection, and scanner results (Code Analyzer, Checkmarx) with issues fixed or documented.", "S8",
          quote="Enroll your solution in the ISV Partner Program."),
        V("A security review fee is paid through the submission interface unless you distribute your solution for free; the amount is not stated on the page.", "S8",
          quote="If you plan to distribute your solution for free, you don\u2019t pay the fee."),
    ],
    steps=[
        st(1, "Create an External Client App", "Setup → Quick Find 'App Manager' → New External Client App. Enter the app details; set Distribution State to Local (own org) or Packaged (to distribute).", "developer", "verified", "S4",
           quote="To develop an external client app for your local org, select Local."),
        st(2, "Enable OAuth settings", "Under API (Enable OAuth Settings) check Enable OAuth Settings, enter the Callback URL and choose scopes (for example api, web, refresh_token/offline_access, id, profile, email).", "developer", "verified", "S4",
           quote="check Enable OAuth Settings."),
        st(3, "Adjust secret requirements for your client type", "The Mobile SDK guide unchecks Require Secret for Web Server Flow and Refresh Token Flow and recommends JWT-based access tokens for named users. Whether server-side web apps should keep the secret requirement is not stated in the pages we read.", "developer", "verified", "S4",
           quote="Uncheck Require Secret for Web Server Flow."),
        st(4, "Create, then edit Policies", "Edit the app's OAuth policies and set Permitted Users, for example 'Admin approved users are pre-authorized', then authorize users through profiles or permission sets. The exact click sequence is not spelled out in the pages we read.", "developer", "verified", "S7",
           quote="Admin approved users are pre-authorized."),
        st(5, "Set token lifetimes", "Under App Authorization set the refresh token expiration and session timeout. The DX page calls a maximum of 90 days for refresh token expiration a security best practice and uses 15 minutes for session timeout, then Save.", "developer", "verified", "S5",
           quote="Setting a maximum of 90 days for the refresh token expiration is a security best practice."),
        st(6, "Avoid the username-password flow", "External client apps do not support the username-password flow, and migration cannot detect its use. The migration page suggests the web server flow with PKCE or the client credentials flow instead. Implement the flow in your code accordingly.", "agent", "verified", "S6",
           quote="External client apps don't support username-password flow."),
        st(7, "Package and submit for AppExchange (optional)", "Package the ECA; partners must meet the four security controls where they apply (partner Connected Apps/ECAs in use by more than two customer production orgs), then submit through the Partner Console. For packaged ECAs share only the client key, never the secret, in submission documents.", "developer", "verified", "S1", "S2",
           quote="For packaged ECAs, share the client key in the submission documents only \u2014 don't share the client secret."),
    ],
    callback_requirements=[
        V("Callback URL is any URL string in the Mobile SDK examples (for example mysampleapp://auth/success); the Salesforce DX example uses http://localhost:1717/OauthRedirect, configurable via oauthLocalPort in sfdx-project.json.", "S4", "S5",
          quote="Set Callback URL to any URL string, real or fictional"),
        V("The callback URL in your client must exactly match what is configured in Salesforce. This comes from a hosted-MCP-servers troubleshooting page, not an ECA setup page.", "S11",
          quote="Make sure the callback (redirect) URL in your client exactly matches what is configured in Salesforce."),
        U("No official page we read states an HTTPS requirement for ECA callback URLs; the Mobile SDK page allows custom non-HTTPS schemes.", "S4"),
    ],
    scopes=[
        V("api, web, refresh_token/offline_access and the identity scopes id, profile, email, address and phone; optional sfap_api and chatbot_api.", "S4", quote="Access the identity URL service"),
    ],
    testing=[
        V("Once saved, the DX page says the external client app is ready to use and gives a localhost callback for CLI auth. No dedicated ECA test procedure was found.", "S5", quote="Your external client app is ready to use."),
    ],
    publishing=[
        V("In your own org, access is governed by Permitted Users: set 'Admin approved users are pre-authorized' and assign profiles or permission sets. Users with the Use Any API Client permission can still reach any ECA, and changing the policy can cut off users it does not cover.", "S7",
          quote="If users have the Use Any API Client permission, they can access any external client app."),
        V("A security review is required to distribute managed packages and Salesforce Platform API solutions (the S8 page is now titled 'AgentExchange'; S2 still says AppExchange). S2 says CAs and ECAs 'should be packaged' for distribution; packaging is required for the authorization code flow when the ISV controls the callback URLs and for Canvas integrations. Other cases may create the ECA in the subscriber org after install and must be documented (see S2 for the flow table).", "S8", "S2",
          quote="CAs and ECAs should be packaged for distribution on AppExchange."),
        V("Stated review estimates: verification 1–2 weeks, first-time testing 3–4 weeks, resubmission testing 2–3 weeks; the page says these are estimates.", "S8",
          quote="The time frames are estimates."),
        V("Partner deadline: ISVs have until May 11, 2026 to meet four security controls (OAuth PKCE, Refresh Token Rotation, Refresh Token Idle TTL, Refresh Token IP Allowlist) on Connected Apps/ECAs used with a Partner Application in more than two customer production orgs; Salesforce said it would then begin enforcing them. Single-production-org and customer-created apps are out of scope, and no formal extension program was planned. This pre-deadline FAQ cannot confirm that enforcement actually started.", "S1",
          quote="As of now, there are no plans for a formal extension program."),
    ],
    blockers=[
        bl("You cannot create a new Connected App", "As of Spring '26 new Connected Apps cannot be created. If you must continue creating them, the Mobile SDK docs say to contact Salesforce Support. Existing connected apps continue to work during and after Spring '26.", "Use an External Client App; existing Connected Apps keep working and can be migrated if eligible.", "verified", "S1", "S3"),
        Blocker(title="Migration is not always possible", detail="Per the migration page: User Provisioning must be disabled and any custom Apex handler removed first; SAML encryption must be switched from Triple DES to AES; Canvas and Dynamic Client Registration apps cannot be migrated; single sign-on connected apps cannot be migrated; standard notification subscriptions on non-internal apps block migration. Migration cannot detect username-password flow use, which ECAs do not support. Migration preserves the consumer key and secret; the original becomes a read-only copy that should not be deleted.", resolution="Fix the fixable items first; check username-password flow use manually.", status="verified", source_ids=["S6"], quote="Migration preserves your consumer key and secret, so existing integrations continue to work."),
        bl("Policy changes can lock users out", "Switching from self-authorization to admin pre-authorization removes access for users not covered by the chosen profiles or permission sets.", "Assign profiles or permission sets before switching.", "verified", "S7"),
        bl("Missing integration credentials delay security review", "Submissions need disclosure of how ECAs are used and how secrets are secured, plus integration credentials; never share the secret.", None, "verified", "S2"),
        bl("A failed security review blocks listing", "The solution cannot be listed or distributed until resubmitted with updated scans.", None, "verified", "S8"),
    ],
    agent_can_do=[
        "Draft the ECA configuration values (scopes, callback URL, policy choices) for an admin to enter.",
        "Write the OAuth code, including the localhost CLI flow and refresh handling.",
        "Prepare the AppExchange submission checklist and the disclosure of ECA usage and secret handling.",
        "Review which of your Connected Apps are migration-eligible.",
    ],
    developer_must_do=[
        "Create and edit the ECA in Setup as an org admin and choose Permitted Users policy.",
        "Enroll in the ISV Partner Program, run the required scanners and pay any review fee.",
        "Package the ECA and submit through the Partner Console.",
        "Contact Salesforce Support if a new Connected App is truly required.",
    ],
    sources=[
        src(1, "Connected Apps and ECA Security Controls: Partner App FAQs", "https://help.salesforce.com/s/articleView?id=005387798&language=en_US&type=1"),
        src(2, "CA and ECA AppExchange Security Review Submission Guidance", "https://help.salesforce.com/s/articleView?id=005232552&language=en_US&type=1"),
        src(3, "External Client Apps and Connected Apps (Mobile SDK)", "https://developer.salesforce.com/docs/platform/mobile-sdk/guide/connected-apps.html"),
        src(4, "Create an External Client App (Mobile SDK)", "https://developer.salesforce.com/docs/platform/mobile-sdk/guide/eca-create.html"),
        src(5, "Create an External Client App in your org (Salesforce DX)", "https://developer.salesforce.com/docs/platform/sfdx-dev/guide/sfdx-dev-auth-eca.html"),
        src(6, "Connected App to External Client App migration", "https://help.salesforce.com/s/articleView?language=en_US&id=xcloud.connected_app_to_external_client_app_migration.htm&type=5"),
        src(7, "Preauthorize user app access through ECA policies", "https://help.salesforce.com/s/articleView?language=en_US&id=xcloud.preauth_user_app_access_through_eca.htm&type=5"),
        src(8, "How the AppExchange security review works", "https://developer.salesforce.com/docs/atlas.en-us.packagingGuide.meta/packagingGuide/security_review_how_it_works.htm"),
        src(9, "New Connected Apps can no longer be created in Spring '26 (article 005228017)", "https://help.salesforce.com/s/articleView?language=en_US&id=005228017&type=1", conf="low",
            note="Unreachable: JS-rendered shell only, content did not match the title. Nothing in this guide relies on it."),
        src(10, "Creation of new Connected Apps is disabled by default (release note)", "https://help.salesforce.com/s/articleView?language=en_US&id=release-notes.rn_security_identity_connected_app_creation_disabled.htm&release=260&type=5", conf="low",
            note="Unreachable: JS-rendered shell only, content did not match the title. Nothing in this guide relies on it."),
        src(11, "Authentication issues (Hosted MCP servers)", "https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/authentication-issues.html",
            note="About hosted MCP servers, not ECA setup; used only for the callback exact-match sentence."),
    ],
    unknowns=[
        "Whether a self-service setting exists to re-enable Connected App creation; only a contact-Support route is documented (the Spring '26 release note, S10, and article 005228017, S9, could not be read).",
        "Whether the 'disabled by default' wording of the release note is accurate; it remains unconfirmed because that page was unreachable.",
        "The security review fee amount (a fee exists unless you distribute for free).",
        "Any propagation delay for new ECAs or policy changes.",
        "An HTTPS requirement for ECA callback URLs (none found on pages read).",
        "Whether server-side web apps should keep Require Secret for Web Server Flow; the Mobile SDK page only covers mobile apps.",
        "Whether orgs using only their own ECAs face any Salesforce review; no page read states this either way.",
        "The 'Create, then Edit' click sequence and the exact 'New External Client App' button label; neither was in the extracted page text.",
        "Where the ECA should be created for packaging (e.g. Dev Hub / packaging org); not found on the pages read.",
    ],
    review_notes=REVIEW_NOTES + [
        "Reconciled against a second verification pass on 2026-10-29: 20 claims confirmed, 10 corrected, 6 left unverified.",
    ],
)
