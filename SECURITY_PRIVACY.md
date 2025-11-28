Security, Privacy, and Moderation

Security Controls
- Authentication: argon2 password hashing; rotate refresh tokens; lockout on repeated failures; email verification.
- Authorization: least privilege RBAC (user, moderator, admin) + ownership checks.
- Transport Security: HTTPS everywhere; HSTS; secure cookies (HttpOnly, Secure, SameSite=Lax).
- Input Validation: Pydantic schemas; server-side validation; size limits on uploads; MIME type checks.
- Rate Limiting: Redis-backed per-IP and per-user limits; stricter on auth endpoints.
- Headers: CSP (strict, nonce-based for inline if any), X-Frame-Options=DENY, Referrer-Policy, X-Content-Type-Options, Permissions-Policy.
- Secrets Management: environment variables from secret store; no secrets in repo; key rotation procedures.
- Data at Rest: managed Postgres encryption; S3 server-side encryption; optional KMS keys.
- Backups & DR: daily DB backups; tested restores; object storage versioning for critical buckets.
- Logging: structured logs without sensitive data; PII scrubbing; request IDs.

Privacy & Compliance
- Data Minimization: collect only required PII (email, profile info user provides).
- Consent & Policies: clear privacy policy and content guidelines; cookie/analytics consent where applicable.
- User Rights: export account data, delete account; retention schedule for deleted content (e.g., 30 days) then purge.
- Children’s Data: age gate to avoid underage accounts per jurisdiction.
- Internationalization: store locale/timezone; comply with GDPR/CCPA where users reside.

Content Safety & Moderation
- Reporting: users can report items/users/comments with reasons; moderation queue for staff.
- Takedown Workflow: open → reviewing → actioned/dismissed; audit log of actions.
- Policy Automation (future): ML classifiers for nudity, hate symbols, spam; manual review gate.
- Abuse Prevention: shadow bans for spam; CAPTCHA on suspicious signups/actions.

Threat Model (selected)
- Account Takeover: mitigated via strong hashing, rate limits, optional 2FA later.
- CSRF/XSS: HttpOnly cookies + CSRF tokens for state changes; CSP and output encoding.
- SSRF/RCE: no remote downloads on server; validate URLs; sandbox image processing libs.
- IDOR: strict authZ in every resource access; avoid guessable IDs; use UUIDs.
- DoS: rate limits, request size/time limits, circuit breakers, autoscaling.

