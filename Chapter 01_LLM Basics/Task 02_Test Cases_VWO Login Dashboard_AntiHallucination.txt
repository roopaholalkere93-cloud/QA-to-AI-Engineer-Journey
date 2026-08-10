# Test Cases: VWO Login Dashboard (Anti-Hallucination Compliant)

- **Author:** Roopa M
- **Role:** QA Engineer (generated under Senior Software Engineer review)
- **Experience Level Applied:** 7 years — senior-level test design, traceability, and risk analysis
- **Source Document:** PRD.md (VWO Login Dashboard)
- **Governing Rules:** Anti_hallucination.rules.md
- **Date:** 2026-08-10

---

## 1. Verified Facts from the PRD

Facts below are extracted **only** from `PRD.md`. Every test case in Section 3 traces back to one of these facts.

### Authentication
- F1. Primary authentication is email and password-based login with secure validation.
- F2. Secure session handling with **configurable** timeout periods.
- F3. **Optional** 2FA support for enhanced security.
- F4. Enterprise SSO integration capability for organizational accounts (SAML, OAuth, and other enterprise authentication protocols).

### Input Validation & Error Handling
- F5. Field validation on **blur** to provide immediate feedback.
- F6. Automatic email format validation (with specialized mobile keyboards).
- F7. Password strength indicators — visual feedback for password requirements and strength.
- F8. Clear, actionable error messages for failed authentication attempts.

### Password Management
- F9. Forgot-password flow — streamlined reset with secure token generation.
- F10. Password recovery via multiple options, including email-based reset.
- F11. Enforced security standards for password complexity.

### User Experience
- F12. Responsive, mobile-optimized interface with touch-friendly controls.
- F13. Auto-focus on the first input field.
- F14. Clickable form labels.
- F15. Loading states providing clear feedback during authentication.
- F16. Remember Me checkbox for persistent login sessions.
- F17. Account registration link / clear free-trial signup path.
- F18. Light and Dark Mode theme options.
- F19. Brand consistency with VWO design system; professional, trustworthy appearance.

### Accessibility
- F20. Screen-reader support (ARIA labels).
- F21. Full keyboard navigation for all interactive elements.
- F22. High-contrast mode for visually impaired users.
- F23. WCAG 2.1 AA compliance.

### Security
- F24. End-to-end encryption for all authentication data transmission.
- F25. Encrypted password storage using industry-standard hashing algorithms.
- F26. Secure session-token generation and management.
- F27. HTTPS / SSL-TLS enforcement for all login communications.
- F28. Rate limiting / request throttling against brute-force attacks.
- F29. GDPR and CCPA compliance for user data handling.
- F30. Support for enterprise security policies and audit trails.
- F31. Compliance with OWASP authentication guidelines.

### Performance
- F32. Login page loads within **2 seconds** on standard connections.
- F33. Asset optimization — compressed images, minified CSS/JavaScript.
- F34. CDN integration for global performance.
- F35. 99.9% uptime (high availability).
- F36. Support for thousands of simultaneous login attempts.
- F37. Multi-region deployment.

### Integration & User Journey
- F38. Seamless transition to the main VWO dashboard after successful authentication.
- F39. Login success/failure tracking for platform optimization.
- F40. Integration with support systems for login assistance.
- F41. Social login: **optional** integration with Google, Microsoft, and other identity providers (third-party).
- F42. Returning-user journey: quick access, dashboard transition, context preservation from previous sessions.
- F43. Error-recovery flow: clear messaging for failures, multiple recovery/support paths, clear success confirmation.
- F44. Customer-support integration for login assistance.

### Future Enhancements (EXPLICITLY OUT OF CURRENT SCOPE)
- F45. Biometric authentication, adaptive authentication, PWA, A/B testing, user-behavior analytics, personalization — listed as **future enhancements**, not current requirements.

---

## 2. Missing / Unknown Information

Per Anti_hallucination.rules.md (Rule 3), the following are **not** stated in the PRD. Test cases below do **not** invent values for these; where relevant, expected results are written as behavior-level assertions and any unknown specifics are labeled `Insufficient information to determine`.

| # | Unknown Item | Consequence for Test Design |
|---|--------------|------------------------------|
| U1 | Exact email validation error message | Test asserts validation is *triggered*, not a specific message text |
| U2 | Exact password validation error message | Assert behavior-level feedback only |
| U3 | Exact password complexity rules (length, character classes) | Assert that *a* defined complexity rule is enforced; exact rule `Insufficient information to determine` |
| U4 | Exact session timeout value | Assert timeout is *configurable* and honored; value `Insufficient information to determine` |
| U5 | Exact 2FA mechanism (SMS, TOTP app, etc.) and screens | Assert optional 2FA *flow* exists; mechanism `Insufficient information to determine` |
| U6 | Exact SSO login UI (button names, IdP pages) | Assert SSO capability; UI specifics `Insufficient information to determine` |
| U7 | Exact Remember Me duration | Assert persistence behavior exists; duration `Insufficient information to determine` |
| U8 | Exact failed-attempt count before rate limiting triggers | Assert throttling exists; threshold `Insufficient information to determine` |
| U9 | Exact rate-limit error message | Assert throttling feedback; text `Insufficient information to determine` |
| U10 | Exact API endpoints, HTTP status/error codes | Not used in any test |
| U11 | Exact dashboard URL | Assert transition to main dashboard; URL `Insufficient information to determine` |
| U12 | Exact loading-indicator design | Assert loading feedback exists; design `Insufficient information to determine` |
| U13 | Exact mobile breakpoints | Assert mobile-optimized behavior; breakpoints `Insufficient information to determine` |
| U14 | Exact supported browsers/devices | Test execution matrix `Insufficient information to determine` |
| U15 | Exact accessibility test data (contrast ratios, etc.) | Assert WCAG 2.1 AA compliance at behavior level |
| U16 | Exact analytics event names/payloads | Assert tracking exists; events `Insufficient information to determine` |
| U17 | Social login details (button labels, IdP flow) | Assert optional integration capability only |
| U18 | Session-token implementation details | Assert secure token management; specifics `Insufficient information to determine` |

---

## 3. Generated Test Cases

Generated **only** from the verified facts in Section 1. Priority: P1 = High, P2 = Medium, P3 = Low (P1 defined as security/critical-path blockers).

| TC ID | Test Scenario | Preconditions / Test Data | Test Steps | Expected Result | Priority | PRD Fact(s) |
|-------|---------------|---------------------------|------------|-----------------|----------|-------------|
| TC-001 | Login with valid email and password | Valid registered email + valid password | 1. Open login page<br>2. Enter email<br>3. Enter password<br>4. Submit login | User is authenticated and transitioned to the VWO main dashboard | P1 | F1, F38 |
| TC-002 | Login with invalid credentials | Invalid/incorrect email and/or password | 1. Enter invalid credentials<br>2. Submit login | Clear, actionable error message for failed authentication is displayed | P1 | F8, F43 |
| TC-003 | Email format validation on blur | Email with a format that fails the defined format rule | 1. Enter malformed email<br>2. Move focus away from the email field (blur) | Email format validation is triggered on blur | P1 | F5, F6 |
| TC-004 | Password strength feedback | Password that fails the PRD-defined complexity requirement | 1. Enter password<br>2. Observe feedback while typing / on submit | Visual password-strength/requirement feedback is displayed | P1 | F7, F11 |
| TC-005 | Password complexity enforcement | Password not meeting defined complexity rule | 1. Attempt login with non-compliant password | Login is blocked / user is prompted to meet complexity requirements (per applied rule) | P1 | F11 |
| TC-006 | Forgot password flow | User on login page, email field populated | 1. Select Forgot Password<br>2. Follow the presented flow | Password reset flow is initiated with secure token generation | P1 | F9 |
| TC-007 | Email-based password recovery | Valid recovery email address | 1. Initiate password recovery via email option | Email-based recovery path is available and initiated | P1 | F10 |
| TC-008 | Remember Me — checked | Valid credentials | 1. Check Remember Me<br>2. Authenticate<br>3. Close browser / return later | Persistent login/session behavior is provided as per product configuration (duration: `Insufficient information to determine`) | P2 | F16 |
| TC-009 | Remember Me — unchecked | Valid credentials | 1. Do not check Remember Me<br>2. Authenticate | Login completes without Remember Me persistence behavior | P2 | F16 |
| TC-010 | Optional 2FA — enabled account | Account configured with optional 2FA | 1. Authenticate with valid credentials<br>2. Complete the presented 2FA step | Optional 2FA flow is supported (mechanism: `Insufficient information to determine`) | P1 | F3 |
| TC-011 | Optional 2FA — not configured | Account without 2FA configured | 1. Authenticate with valid credentials | Login proceeds without a 2FA step | P1 | F3 |
| TC-012 | Enterprise SSO login | Enterprise account enabled for SSO | 1. Initiate SSO authentication<br>2. Authenticate via enterprise IdP | SSO authentication capability is available (protocol per config: SAML/OAuth) | P1 | F4 |
| TC-013 | Session handling — active session | Valid authenticated session | 1. Authenticate<br>2. Continue using application normally | Session remains valid and is handled securely | P1 | F2, F26 |
| TC-014 | Session timeout — inactivity | Authenticated session; configured timeout period | 1. Authenticate<br>2. Remain inactive until the configured timeout elapses | Session ends per the configured timeout (value: `Insufficient information to determine`) | P1 | F2 |
| TC-015 | Session timeout configurability | Admin/config access (as applicable) | 1. Change timeout configuration<br>2. Verify session behavior reflects new value | Timeout is configurable and honored after change | P1 | F2 |
| TC-016 | HTTPS enforcement | Login page accessed over network | 1. Access login page<br>2. Inspect connection security | Login communications use HTTPS/SSL/TLS encryption | P1 | F27 |
| TC-017 | Brute-force protection | Repeated failed login attempts | 1. Perform repeated failed authentication attempts | Request throttling / rate limiting protects against brute-force attacks (threshold: `Insufficient information to determine`) | P1 | F28 |
| TC-018 | Encrypted password storage | Backend data access (test environment) | 1. Store/verify password in data store | Passwords stored using industry-standard hashing — not plaintext | P1 | F25 |
| TC-019 | Login page load time | Standard network connection | 1. Trigger login page load<br>2. Measure time to interactive load | Login page loads within 2 seconds | P1 | F32 |
| TC-020 | Loading state during authentication | Valid credentials; network request in progress | 1. Submit login<br>2. Observe UI during request | Clear loading feedback is displayed during authentication processing | P2 | F15 |
| TC-021 | Auto-focus on first input | Fresh login page load | 1. Load login page<br>2. Observe initial focus | First input field receives automatic focus | P2 | F13 |
| TC-022 | Clickable labels | Login page loaded | 1. Click on email label / password label | Label click focuses/activates its associated field | P2 | F14 |
| TC-023 | Keyboard navigation | Login page | 1. Navigate all interactive elements using Tab/Enter/Space only | All interactive elements are fully keyboard accessible | P1 | F21, F23 |
| TC-024 | Screen-reader support (ARIA) | Screen reader enabled (e.g., NVDA/VoiceOver) | 1. Navigate login page with screen reader | Interface provides screen-reader support via ARIA labels | P1 | F20, F23 |
| TC-025 | High-contrast mode | High-contrast accessibility mode available | 1. Enable high-contrast mode<br>2. View login page | Login interface remains usable in high-contrast mode | P2 | F22, F23 |
| TC-026 | Responsive / mobile layout | Mobile device or mobile viewport | 1. Open login page on mobile viewport | Interface is mobile-optimized with touch-friendly controls (breakpoints: `Insufficient information to determine`) | P1 | F12 |
| TC-027 | Light and Dark Mode | Theme options available | 1. Switch between Light and Dark Mode | Both themes are supported and consistent with the design system | P2 | F18, F19 |
| TC-028 | Registration / free-trial link | New user on login page | 1. Locate registration path on login page | Clear call-to-action to free-trial signup is available | P2 | F17 |
| TC-029 | Dashboard transition after success | Valid credentials | 1. Authenticate successfully | User transitions seamlessly to the main VWO dashboard | P1 | F38, F42 |
| TC-030 | Context preservation (returning user) | Previously authenticated session/context | 1. Authenticate as returning user<br>2. Observe dashboard state | Context from previous sessions is preserved (per product behavior) | P2 | F42 |
| TC-031 | Login success tracking | Successful login performed | 1. Authenticate successfully<br>2. Verify analytics/logs | Successful login is tracked for platform optimization (event names: `Insufficient information to determine`) | P2 | F39 |
| TC-032 | Login failure tracking | Failed login performed | 1. Attempt failed login<br>2. Verify analytics/logs | Failed login is tracked for platform optimization | P2 | F39 |
| TC-033 | Social login (optional) | Integration configured for Google/Microsoft | 1. Locate social login option<br>2. Authenticate via provider | Optional social login integration is available (flow details: `Insufficient information to determine`) | P3 | F41 |
| TC-034 | Success confirmation | Successful authentication | 1. Complete login | Clear indication of successful login is provided | P2 | F43 |
| TC-035 | Support path from login | Login assistance needed | 1. Locate support/help path from login page | Support integration for login assistance is reachable | P3 | F40, F44 |

**Test execution notes (senior-level):**
- Positive/negative pairing is explicit (TC-001/TC-002, TC-008/TC-009, TC-010/TC-011) — boundary and equivalence reasoning applied without inventing data.
- Every expected result is written as a **behavior-level assertion** that can be verified without undocumented specifics.
- Any value not present in the PRD is flagged `Insufficient information to determine` rather than fabricated.

---

## 4. Self-Validation Check (Anti-Hallucination Rule 4)

| Rule | Check Result |
|------|--------------|
| No invented features | ✅ All 35 TCs map to PRD facts F1–F44 (see traceability column) |
| No assumed default/typical behavior | ✅ No "5 attempts", "30 minutes", "6-digit OTP", or "/dashboard" invented anywhere |
| Missing info handled per Rule 3 | ✅ U1–U18 explicitly listed; all affected TCs assert behavior-level outcomes |
| Every assertion traceable to input | ✅ Traceability column links each TC to a specific PRD fact |
| Inferences labeled | ✅ No unlabeled inferences; unknowns marked `Insufficient information to determine` |
| Deterministic / repeatable | ✅ Output is fully determined by PRD.md + Anti_hallucination.rules.md |
| Contradictions | ✅ None found between PRD statements and generated cases |
| Future features excluded from scope | ✅ Biometric/PWA/adaptive auth (F45) deliberately NOT tested as current scope |

---

## 5. Impact of Using vs. NOT Using Anti-Hallucination Rules

### What anti-hallucination rules protect
The rules forbid inventing features, error codes, UI elements, or behavior (Rule 1), forbid assuming "typical" behavior (Rule 2), and force `Insufficient information to determine` for gaps (Rule 3).

### Concrete example — real PRD facts vs. hallucinated test cases

| PRD says (actual) | With Anti-Hallucination (correct) | Without Anti-Hallucination (hallucinated) |
|-------------------|----------------------------------|-------------------------------------------|
| "Email format verification" (F6) | TC-003: blur → *email format validation is triggered* | "Enter `abc@` and verify error `Invalid email address`" — message not in PRD |
| "Rate limiting against brute force" (F28) | TC-017: repeated failures → *throttling protects* | "After 5 failed attempts, account locks for 15 minutes" — numbers not in PRD |
| "Configurable timeout" (F2) | TC-014/015: *configurable, honored* | "User logged out after 30 minutes" — value not in PRD |
| "Password complexity requirements" (F11) | TC-005: *complexity rule enforced* | "Must contain 8 chars, 1 upper, 1 number, 1 special" — rule not in PRD |
| "Optional 2FA" (F3) | TC-010/011: *2FA flow supported when configured* | "Enter 6-digit SMS OTP" — mechanism not in PRD |
| "SSO: SAML, OAuth, and other protocols" (F4) | TC-012: *SSO capability* | "Click `Login with SAML` button, enter corporate credentials" — UI not in PRD |
| "Transition to main dashboard" (F38) | TC-029: *transitions to main dashboard* | "Verify URL is `/dashboard`" — URL not in PRD |

### Quality comparison table

| Area | With Anti-Hallucination | Without Anti-Hallucination |
|------|-------------------------|----------------------------|
| Requirement traceability | ✅ Every TC maps to a PRD fact | ❌ TCs may cite details absent from the PRD |
| Accuracy | ✅ Assertions provable from source | ⚠️ Mix of facts and invented specifics |
| False positives (test passes but should fail) | Low | Higher — invented expectations can't be verified |
| False negatives (real bugs missed) | Transparent — gaps declared | Hidden — gaps filled with plausible-looking assumptions |
| Maintenance | Easy — source changes re-derive TCs | Difficult — invented values go stale silently |
| Developer confidence | High — "this is exactly what the PRD says" | Low — "where did 5 attempts / 30 min come from?" |
| QA review effort | Low — reviewer verifies against one PRD | High — reviewer must hunt for every unsupported claim |
| Requirement gap discovery | ✅ Gaps (U1–U18) are explicit backlog items | ❌ Gaps dressed up as tests, so nobody files them |
| Test execution | Deterministic — pass/fail clearly defined | Ambiguous — testers clarify or guess, execution varies |
| Auditability | Strong — every line traces to a source | Weak — provenance of assertions unknown |
| Risk of misleading coverage | Low | High — "looks tested" but isn't grounded |

### Bottom line (senior engineering view)
Without the rules, the suite *looks* more complete and more precise, but the precision is fictional. Numbers like "5 attempts", "30 minutes", "6-digit OTP", and URLs like `/dashboard` look testable until a developer reads the PRD and finds none of them specified — then the tests fail on wrong expectations, waste cycles, and erode trust. With the rules, each test is a verified contract with the PRD, gaps are surfaced as explicit open questions (U1–U18) that become backlog items, and the suite stays deterministic and auditable. That is the difference between a test suite that documents a product and one that fabricates it.

---

## 6. Open Questions (Escalated to Product Owner — not assumptions)

1. Exact password complexity rule (length/character classes) — required to write precise TC-004/TC-005 assertions.
2. Session timeout default value and range — required for TC-014.
3. Failed-attempt threshold for rate limiting — required for TC-017.
4. 2FA delivery mechanism (SMS/TOTP/authenticator) — required for TC-010.
5. Email validation error message text — required for message-level assertion of TC-003.
6. Supported browser/device matrix — required to scope cross-browser execution of TC-019/TC-026.

---

*End of document. Generated deterministically from PRD.md using Anti_hallucination.rules.md process (Steps 1–4).*
