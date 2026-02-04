# Recommended Stack & Setup

[< Back to Index](README.md) | [Prev: Platform Comparison](04-platform-comparison.md) | [Next: Implementation Phases >](06-implementation-phases.md)

---

## A. Live Room Platform (Non-Zoom)

### Option 1: Jitsi (Open Source — Recommended Start)

**Pros:**
- Fully open source
- No accounts required
- Password-protected rooms
- Mute all on entry
- Lock room
- Kick users
- Recording (self-hosted or local)
- Very low cost

**Cons:**
- UI less polished
- Needs setup for advanced moderation

**Setup Steps:**
1. Choose: Public Jitsi server (quick start) OR self-hosted Jitsi (best long-term sovereignty)
2. Create one room per theme (e.g., `jitsi.yourdomain.org/mondays`)
3. Enable: Lobby mode, mute on entry, moderator-only unmute, password access
4. Configure: Only moderators can enable cameras/audio; disable screen sharing for attendees
5. Add recording toggle (local or server)

### Option 2: BigBlueButton (Education-Grade)

**Pros:**
- Open source
- Built-in: raise hand, speaker queue, mute all, lock microphones, whiteboards, breakout rooms
- Excellent for teaching

**Cons:**
- Heavier hosting cost
- More setup complexity

**Setup Steps:**
1. Deploy BigBlueButton on a VPS
2. Create room templates per theme
3. Set defaults: mute all on entry, attendees must raise hand, moderator approves mic
4. Configure recording rules
5. Assign co-hosts/moderators

---

## B. Registration & Anti-Spam Gate

**Tool: Tally Forms (Recommended)**

1. Create registration form with: Name, Email, Why are you joining?, Which session (Mon/Wed/Fri), Agree to community agreements, Consent to recording
2. Enable required email verification and reCAPTCHA
3. Connect form to Airtable (backend database)
4. Set automation: On submit -> send email with room link, or -> send "pending approval" email

---

## C. Speaker / Educator Intake

**Tools: Airtable + Tally**

1. Create Airtable base with fields: Name, Topic, Theme, Bio, Links, Status, Date Slot
2. Create Tally intake form that pushes submissions into Airtable
3. Create public Airtable "Read-Only View" showing only approved rows
4. Embed public view into Notion or website

**Workflow:**
- New submission -> status = Pending
- Approved -> status = Approved -> auto-appears publicly

---

## D. Public Hub (Discoverability)

### Option 1: Notion (Fastest)
1. Create pages: "Live with Syd" with one subpage per theme
2. Embed: registration forms, upcoming sessions (Airtable view), replay videos
3. Add tags: Capital / Planetary Party / Sanctuaries

### Option 2: WordPress or Ghost (More Professional)
1. Create landing page
2. Connect Airtable via API
3. Auto-populate upcoming sessions
4. Embed YouTube replays
5. Add SEO tags

---

## E. Streaming & Recording

**Tool: OBS Studio (Open Source)**

1. Install OBS
2. Create scenes: title card, live discussion, speaker overlay, closing gratitude slide
3. Set outputs: local recording, stream to YouTube
4. Optional: connect Restream to multistream

---

## F. Anti-Disruption & Moderation Safeguards

### Required Settings (Jitsi or BigBlueButton):

1. **Mute All on Entry** — Default: everyone muted, camera off
2. **Moderator-Only Controls** — Only host/co-hosts can unmute participants, enable video, share screen
3. **Lobby Mode** — People wait in a holding area; admit manually or auto-admit trusted users
4. **Room Lock** — Lock room 5-10 minutes after start to prevent late bombers
5. **Raise Hand / Queue** — Participants request to speak; approve one at a time
6. **Kick + Ban** — Immediate removal of disruptive users; IP ban (if self-hosted)

---

## G. Scalability Layer (If Interest Explodes)

If sessions start getting 50-200+ people:

- Add dedicated moderator role
- Switch to BigBlueButton
- Add waiting room rules
- Tiered roles: speaker / listener / co-host
- Segment sessions: "Listener room" + "Speaker room"

---

[< Back to Index](README.md) | [Prev: Platform Comparison](04-platform-comparison.md) | [Next: Implementation Phases >](06-implementation-phases.md)
