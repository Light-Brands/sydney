# Tech Builder Checklist

[< Back to Index](README.md) | [Prev: Builder Guardrails](16-builder-guardrails.md) | [Next: Discord Architecture >](18-discord-architecture.md)

---

**Project:** Live with Syd — Regenerative Futures Platform
**Goal:** Launch a privacy-respecting, scalable, co-creative live session ecosystem
**Owner:** Syd Griffith
**Launch Target:** February
**Stack Preference:** Open-source + privacy-first + low-friction

---

## Phase 0 — Foundational Guardrails (Do This First)

Builder must confirm in writing:

- [ ] No Zoom, Meta, or surveillance-based platforms
- [ ] No resale or third-party sharing of participant data
- [ ] No tools with ambiguous media rights clauses
- [ ] GDPR-friendly defaults
- [ ] Minimal data collection only
- [ ] Explicit consent flows for recording
- [ ] Participant opt-out from recordings supported
- [ ] Content removal on request is technically feasible
- [ ] All recordings remain fully owned by Syd
- [ ] No forced account creation for participants
- [ ] Simple UX for non-technical users

**Acceptance Criteria:**
Builder provides a 1-page stack rationale explaining why each tool meets these guardrails.

---

## Phase 1 — Live Room Infrastructure

### A) Choose & Deploy Live Platform

**Primary Option:** Jitsi (self-hosted preferred)
**Backup Option:** BigBlueButton (for scale / education mode)

### Tasks

- [ ] Select hosting method:
  - Public Jitsi (short-term)
  - OR Self-hosted Jitsi on VPS (long-term sovereignty)
- [ ] Create dedicated rooms:
  - `/mondays`
  - `/wednesdays`
  - `/fridays`
  - `/monthly` for heart sharing
- [ ] Configure default room settings:
  - Mute all on entry
  - Camera off on entry
  - Moderator-only unmute
  - Moderator-only screen share
  - Lobby mode enabled
  - Room password required
  - Waiting room visible
  - Raise-hand feature enabled
  - Recording toggle available
  - Participant list visible to moderators
- [ ] Set moderator roles:
  - Syd = Host
  - 1-2 backup co-hosts
  - Role permission tiers (Host / Moderator / Attendee)
- [ ] Test:
  - Admit from lobby
  - Mute/unmute flow
  - Raise-hand workflow
  - Kick & ban user
  - Lock room mid-session
  - Recording on/off
  - Late entry handling

**Acceptance Criteria:**
- [ ] Host can: Mute all, Lock room, Admit users, Spotlight speakers, Remove disruptive users
- [ ] Participants cannot: Unmute without permission, Share screen, Disrupt room flow

---

## Phase 2 — Registration & Anti-Spam Gate

### B) Registration Form (Tally)

### Tasks

- [ ] Create master registration form
- [ ] Required fields:
  - Full Name
  - Email
  - Session Selection (Mon/Wed/Fri/Monthly)
  - Intentionality question
  - Participation preference
  - Community agreement consent
  - Recording consent
  - Newsletter opt-in
- [ ] Enable:
  - Email verification
  - reCAPTCHA
  - Required consent checkbox
  - Duplicate submission prevention
- [ ] Connect form to Airtable backend
- [ ] Configure confirmation logic:
  - Auto-send room link
  - OR pending approval email (configurable toggle)
- [ ] Create automated emails:
  - Registration confirmation
  - Session reminder (24h + 1h before)
  - Post-session replay email

**Acceptance Criteria:**
- [ ] Bot submissions are blocked
- [ ] Users receive confirmation automatically
- [ ] Syd can toggle auto-approve vs manual approve
- [ ] Registration database is searchable & filterable

---

## Phase 3 — Speaker / Educator Intake

### C) Speaker Intake System (Tally + Airtable)

### Tasks

- [ ] Create Airtable base with fields:
  - Name
  - Email
  - Proposed Title
  - Description
  - Theme
  - Format
  - Length
  - Bio
  - Tech Needs
  - Availability
  - Consent to recording
  - Status (Pending / Approved / Scheduled / Declined)
  - Date Slot
  - Public Visibility Toggle
- [ ] Create Tally intake form:
  - Push submissions into Airtable
  - Required consent checkbox
- [ ] Create approval workflow:
  - Status defaults to "Pending"
  - Approved rows auto-appear in public view
- [ ] Create public read-only view:
  - Shows only approved proposals
  - Sortable by theme & date
  - Embedded into Notion

**Acceptance Criteria:**
- [ ] Public cannot edit entries
- [ ] Syd can approve/reject easily
- [ ] Public docket updates automatically
- [ ] Speaker consent is captured

---

## Phase 4 — Public Hub (Notion)

### D) Landing Page Build

### Tasks

- [ ] Create Notion landing page using provided layout (see [Notion Landing Page](14-notion-landing-page.md))
- [ ] Sections to include:
  - Hero
  - What This Is
  - Weekly Themes
  - Grief Circles
  - Upcoming Sessions (database view)
  - Propose a Topic
  - How to Participate
  - Community Agreements
  - Past Replays
  - About Syd
  - CTAs
- [ ] Embed:
  - Tally registration form
  - Speaker intake form
  - Airtable public views
  - Replay videos
- [ ] Create Notion databases:
  - Sessions DB
  - Replays DB
  - Proposed Topics DB
- [ ] Add filters:
  - Upcoming only
  - Sorted by date
  - Theme tags

**Acceptance Criteria:**
- [ ] Page loads cleanly on mobile
- [ ] Registration & intake forms work in-page
- [ ] Upcoming sessions auto-update
- [ ] Replays embed correctly
- [ ] CTAs are visible top & bottom

---

## Phase 5 — Streaming + Recording

### E) OBS Setup

### Tasks

- [ ] Install OBS
- [ ] Create scenes:
  - Opening title
  - Live discussion
  - Speaker spotlight
  - Closing gratitude
  - Heart sharing circle mode (no recording)
- [ ] Configure outputs:
  - Local recording
  - YouTube stream key
- [ ] Optional:
  - Restream integration
- [ ] Test:
  - Audio sync
  - Scene switching
  - Screen sharing
  - Recording quality
  - Stream stability

**Acceptance Criteria:**
- [ ] Clean audio
- [ ] Stable stream
- [ ] Local recordings saved correctly
- [ ] Ability to turn recording off for heart sharing circles

---

## Phase 6 — Moderation & Safety Controls

### F) Room Safety Rules

### Tasks

- [ ] Enable:
  - Mute all on entry
  - Moderator-only unmute
  - Lobby mode
  - Room lock after start
  - Raise-hand queue
- [ ] Create moderator quick panel:
  - Admit user
  - Mute user
  - Remove user
  - Lock room
  - Spotlight speaker
- [ ] Define moderator role permissions
- [ ] Add emergency removal workflow

**Acceptance Criteria:**
- [ ] No one can speak without permission
- [ ] Disruptive users can be removed in <10 seconds
- [ ] Room can be locked during live sessions
- [ ] Late entries go to lobby

---

## Phase 7 — Automation & Scale Readiness

### G) Automation Layer

### Tasks

- [ ] Connect:
  - Tally -> Airtable
  - Airtable -> Email automation
  - Airtable -> Notion (session display)
- [ ] Create automation rules:
  - On new registration -> confirmation email
  - On approval -> room link email
  - 24h before -> reminder
  - 1h before -> reminder
  - Post-session -> replay email

**Acceptance Criteria:**
- [ ] Zero manual emailing required
- [ ] Registrants always get correct link
- [ ] Cancellations auto-notify users

---

## Phase 8 — Quality Assurance & Launch

### H) Testing Protocol

### Tasks

- [ ] Dry run with 3-5 people
- [ ] Stress test with 15-20 people
- [ ] Test heart sharing circle (no recording)
- [ ] Test speaker intake -> public display
- [ ] Test moderation controls live
- [ ] Test removal of disruptive user
- [ ] Test late entry lock
- [ ] Test replay publishing workflow

**Acceptance Criteria:**
- [ ] No critical failures
- [ ] Registration -> room entry works end-to-end
- [ ] Moderation works cleanly
- [ ] Recordings publish smoothly
- [ ] Consent is respected

---

## Phase 9 — Documentation & Handoff

### I) Builder Deliverables

Builder must provide:

- [ ] 1-page system architecture diagram
- [ ] Tool credentials & access list
- [ ] Moderator SOP (how to run sessions)
- [ ] Emergency protocol
- [ ] Automation flow map
- [ ] Simple "how to update sessions" guide
- [ ] Troubleshooting checklist
- [ ] Backup plan if a tool fails

---

## Optional Future Upgrades (Do Not Build Yet)

- [ ] Membership tiers
- [ ] Sliding-scale payments
- [ ] Token-gated sessions
- [ ] Guild role dashboards
- [ ] DAO integrations
- [ ] CRM donor tracking
- [ ] Community reputation system
- [ ] Multi-language support

---

## Final Acceptance Sign-Off

Builder confirms:

- [ ] All privacy guardrails met
- [ ] All moderation controls functional
- [ ] All automation workflows stable
- [ ] Syd trained on:
  - Admitting users
  - Muting/unmuting
  - Locking rooms
  - Recording
  - Publishing replays
- [ ] System is:
  - Scalable
  - Ethical
  - Low-friction
  - Fully owned by Syd
  - Ready for public launch

---

[< Back to Index](README.md) | [Prev: Builder Guardrails](16-builder-guardrails.md) | [Next: Discord Architecture >](18-discord-architecture.md)
