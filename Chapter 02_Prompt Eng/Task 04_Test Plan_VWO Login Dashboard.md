# Test Plan: VWO Login Dashboard (app.vwo.com)

- **Author:** Roopa M
- **Role:** Senior Manual QA Engineer (7 years experience applied)
- **Source Document:** PRD.md (VWO Login Dashboard)
- **Governing Rules:** RICE POT Template.md, Anti_hallucination.rules.md
- **Framework:** RICEPOT (R – Requirements, I – Interfaces, C – Compatibility, E – Error/Exception, P – Performance, O – Operational/Usability/Observability, T – Security)
- **Date:** 2026-08-10

---

## 1. Introduction

### 1.1 Purpose
Define the scope, strategy, resources, schedule, and deliverables for validating the VWO (Visual Website Optimizer) login dashboard at app.vwo.com. The login dashboard is the entry point for VWO's experimentation, personalization, and analytics platform, used by over 4,000 brands across 90 countries.

### 1.2 Scope
**In scope:** Email/password authentication, session management, optional 2FA, enterprise SSO, input validation, password management (forgot/reset), Remember Me, user experience (responsive design, auto-focus, clickable labels, loading states), accessibility (screen readers, keyboard navigation, high contrast, WCAG 2.1 AA), branding (Light/Dark Mode), security (encryption, rate limiting, compliance), performance (page load, scalability, availability), and integrations (dashboard transition, analytics, support, social login).

**Out of scope (explicitly future enhancements per PRD):** Biometric authentication, adaptive/risk-based authentication, progressive web app (PWA), A/B testing of the login experience, user-behavior analytics, and personalization.

### 1.3 References
| Reference | Source |
|-----------|--------|
| PRD.md | VWO Login Dashboard product requirements |
| RICE POT Template.md | QA test generation rules and framework definition |
| Anti_hallucination.rules.md | Verification and traceability rules for all assertions |

---

## 2. Test Strategy

### 2.1 RICEPOT Coverage Strategy
| RICEPOT Pillar | Scope of Coverage | PRD Fact Reference |
|----------------|-------------------|--------------------|
| R – Requirements / Rules | Functional compliance: authentication, validation, password management, UX features | F1–F19 |
| I – Interfaces / Integration | Dashboard transition, analytics tracking, support integration, social login, SSO | F38–F44, F4 |
| C – Compatibility | Responsive/mobile layout, themes (Light/Dark), browser/device support | F12, F18, F19, F23 |
| E – Error / Exception handling | Invalid credentials, validation failures, recovery flows, throttle feedback | F8, F43, F28 |
| P – Performance | Page load ≤ 2s, assets, CDN, availability, concurrency, multi-region | F32–F37 |
| O – Operational / Usability / Observability | Usability, accessibility, success/failure tracking, observability of events | F15, F20–F23, F39 |
| T – Security | Encryption, secure storage, session security, HTTPS, rate limiting, compliance | F24–F31 |

### 2.2 Test Levels
| Level | Objective | Execution |
|-------|-----------|-----------|
| Unit (via dev teams) | Individual validation/logic modules | Developers, CI pipeline |
| Integration | Login → dashboard, analytics, support hooks | QA team |
| System (functional) | End-to-end login flows per RICEPOT pillars | QA team, manual |
| Acceptance | Business objectives: secure access, low friction, compliance | QA + Product Owner sign-off |

### 2.3 Test Types
Functional, Negative, Usability, Accessibility (WCAG 2.1 AA), Compatibility, Security, Performance (load/baseline), Regression, and Exploratory (with traceability to PRD facts only).

### 2.4 Entry / Exit Criteria
**Entry:** PRD approved; test environment available; test data (valid/invalid credentials per environment policy) provisioned; login dashboard build deployed.
**Exit:** All P1 (High priority) test cases executed and passed; no open critical/blocker defects; defects triaged with owners; test results documented and traced to PRD facts; anti-hallucination self-validation completed.

---

## 3. Scope of Testing per RICEPOT Pillar

### R – Requirements / Rules (Functional)
| Test Focus | Requirement (PRD) | Verification Approach |
|-----------|-------------------|----------------------|
| Primary login | Email/password authentication with secure validation (F1) | Positive login with valid credentials; transition to dashboard |
| Session management | Configurable session timeout (F2) | Verify session honors configured timeout; config changes reflected |
| Optional 2FA | Optional 2FA support (F3) | Verify 2FA step for configured accounts; absent for unconfigured |
| Enterprise SSO | SSO for organizational accounts (F4) | Verify SSO authentication via enterprise IdP (SAML/OAuth) |
| Validation on blur | Field validation on blur (F5) | Move focus away; verify immediate feedback |
| Email format | Automatic email format verification (F6) | Enter malformed email; verify validation triggered |
| Password strength | Visual strength/requirement indicators (F7) | Observe feedback while typing/submitting |
| Error handling | Clear, actionable error messages (F8) | Invalid credentials; verify clear messaging |
| Forgot password | Secure token-based reset (F9) | Initiate reset; verify secure token flow |
| Recovery options | Multiple recovery options incl. email (F10) | Verify email-based recovery path available |
| Password complexity | Enforced complexity standards (F11) | Verify non-compliant passwords blocked per defined rule |

### I – Interfaces / Integration
| Test Focus | Requirement (PRD) | Verification Approach |
|-----------|-------------------|----------------------|
| Dashboard transition | Seamless transition after auth (F38) | Verify successful login lands on main VWO dashboard |
| Analytics | Success/failure tracking (F39) | Verify login events tracked in analytics/logs |
| Support integration | Support systems for login assistance (F40, F44) | Verify support/help path reachable from login |
| Social login | Optional Google/Microsoft/other IdP (F41) | Verify optional social login integration when configured |
| Returning-user journey | Quick access, context preservation (F42) | Verify context preserved from previous sessions |
| Error recovery flow | Messaging, recovery paths, success confirmation (F43) | Verify all recovery paths and confirmation |

### C – Compatibility
| Test Focus | Requirement (PRD) | Verification Approach |
|-----------|-------------------|----------------------|
| Responsive/mobile | Mobile-optimized, touch-friendly (F12) | Test on mobile viewports/devices |
| Themes | Light and Dark Mode (F18) | Verify both themes render consistently |
| Branding | Design system consistency (F19) | Verify visual alignment with VWO design system |
| Accessibility standards | WCAG 2.1 AA (F23) | Accessibility audit per WCAG 2.1 AA |

### E – Error / Exception Handling
| Test Focus | Requirement (PRD) | Verification Approach |
|-----------|-------------------|----------------------|
| Failed auth messaging | Clear actionable error messages (F8, F43) | Invalid credentials → verify message quality and recovery options |
| Recovery options | Multiple recovery paths (F43) | Verify forgot-password and support paths |
| Throttle feedback | Rate limiting (F28) | Repeated failures → verify throttling behavior and feedback |
| Validation failures | Blur validation and email format (F5, F6) | Malformed input → verify blocking feedback |

### P – Performance
| Test Focus | Requirement (PRD) | Verification Approach |
|-----------|-------------------|----------------------|
| Page load | ≤ 2 seconds (F32) | Measure time to load on standard connection |
| Asset optimization | Compressed images, minified CSS/JS (F33) | Verify optimized assets served |
| CDN | CDN utilization (F34) | Verify global content delivery |
| Availability | 99.9% uptime (F35) | Monitor/validate availability |
| Concurrency | Thousands of simultaneous logins (F36) | Load test with concurrent login attempts |
| Multi-region | Multi-region deployment (F37) | Verify latency/behavior across regions |

### O – Operational / Usability / Observability
| Test Focus | Requirement (PRD) | Verification Approach |
|-----------|-------------------|----------------------|
| Loading states | Clear feedback during auth (F15) | Verify loading feedback during request |
| Auto-focus | Focus on first input (F13) | Verify initial focus on page load |
| Clickable labels | Accessible labels (F14) | Verify label clicks activate fields |
| Screen reader | ARIA labels (F20) | Verify screen-reader navigation (NVDA/VoiceOver) |
| Keyboard nav | Full keyboard accessibility (F21) | Verify Tab/Enter/Space-only navigation |
| High contrast | Mode for visually impaired (F22) | Verify usability in high-contrast mode |
| Observability | Login success/failure tracking (F39) | Verify events observable in analytics/logs |

### T – Security
| Test Focus | Requirement (PRD) | Verification Approach |
|-----------|-------------------|----------------------|
| Data encryption | E2E encryption of auth data (F24) | Verify encrypted transmission |
| Password storage | Industry-standard hashing (F25) | Verify hashed (not plaintext) storage |
| Session security | Secure token generation/management (F26) | Verify token security practices |
| HTTPS | SSL/TLS enforcement (F27) | Verify HTTPS on all login communications |
| Rate limiting | Brute-force protection (F28) | Verify request throttling behavior |
| Compliance | GDPR, CCPA, OWASP, enterprise audit (F29–F31) | Verify compliance controls and audit trails |

---

## 4. Test Environment
- **Application under test:** app.vwo.com login dashboard (test environment as provisioned).
- **Browsers:** Supported browser matrix — `Insufficient information to determine` (per PRD; matrix not specified).
- **Mobile devices/viewports:** Mobile-optimized behavior must be validated; exact device list — `Insufficient information to determine`.
- **Network:** Standard connection for baseline performance (per F32); test environment network for functional testing.
- **Test data:** Valid/invalid credentials provisioned per environment policy; password-reset email accounts; 2FA/SSO-enabled test accounts as available.

---

## 5. Test Data Requirements
| Data Type | Description | Source |
|-----------|-------------|--------|
| Valid credentials | Registered email + password | Test environment provisioning |
| Invalid credentials | Incorrect email/password combos | Test environment provisioning |
| Recovery email | Accessible mailbox for reset flow | Test environment provisioning |
| 2FA account | Account with 2FA enabled (mechanism per config) | Test environment provisioning |
| SSO account | Enterprise account with SSO enabled | Test environment provisioning |
| Mobile viewport | Simulated mobile widths | Browser dev tools / device lab |

---

## 6. Roles and Responsibilities
| Role | Responsibility |
|------|----------------|
| QA Engineer | Test plan/tc authoring, execution, defect reporting |
| Senior QA Review | Traceability and anti-hallucination review |
| Developer | Build/fix, unit-level verification |
| Product Owner | Clarify unknowns (see Open Questions), sign-off |

---

## 7. Schedule and Deliverables
**Deliverables:**
1. Test Plan (this document)
2. Test Cases (separate document: Task 04_Test Cases_VWO Login Dashboard.md) — RICEPOT-categorized, PRD-traceable
3. Defect reports (as defects arise)
4. Test execution summary (pass/fail per TC, traced to PRD facts)

---

## 8. Defect Management
- Defects logged with: severity, priority, RICEPOT pillar, steps-to-reproduce, expected vs actual, PRD fact reference.
- Triage: P1 (blocker/critical-path) → immediate; P2 → next iteration; P3 → backlog.
- Retest and regression on fix per the affected pillar.

---

## 9. Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| Unknown exact rules (complexity, timeout, thresholds) | Precise assertions impossible | Escalate as Open Questions; assert behavior-level outcomes with `Insufficient information to determine` |
| Unknown browser/device matrix | Incomplete compatibility coverage | Flag as Open Question; test documented baseline |
| No production credentials in PRD | Cannot test live account flows | Use test-environment provisioning |
| 2FA/SSO test accounts unavailable | Cannot execute those flows | Provision accounts; else document as blocked |
| Hallucinated requirements leak into tests | False test expectations | Anti-hallucination self-validation on every deliverable |

---

## 10. Open Questions (Escalated — not assumptions)
1. Exact password complexity rule (length/character classes) — required for precise complexity assertions.
2. Session timeout default value and range — required for timeout assertions.
3. Failed-attempt threshold for rate limiting — required for throttling assertions.
4. 2FA delivery mechanism (SMS/TOTP/authenticator) — required for 2FA flow detail.
5. Email/password validation error message text — required for message-level assertions.
6. Supported browser/device matrix — required to scope compatibility execution.

---

## 11. Approval
| Role | Name | Sign-off |
|------|------|----------|
| QA Engineer | Roopa M | |
| Senior QA Review | | |
| Product Owner | | |

---

*End of Test Plan. Generated deterministically from PRD.md using RICE POT Template.md and Anti_hallucination.rules.md (Steps 1–4).*
