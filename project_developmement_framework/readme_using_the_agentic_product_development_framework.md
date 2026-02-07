# Agentic Product Development Framework

## Purpose of This Repository

This repository contains a **production-grade framework** for building software systems using AI coding agents **safely, incrementally, and explainably**.

The framework is designed to:
- Survive LLM context loss
- Survive platform changes (Cursor, Warp, AntiGravity, etc.)
- Preserve human engineering intent
- Prevent hallucinations and unsafe assumptions
- Enforce testing, security, and change discipline

This is **not** a codebase-first system. It is a **governance-first system**.

---

## Core Mental Model (Read This First)

### You do NOT:
- Directly tell an agent to “build the whole system”
- Rely on chat history
- Assume the agent understands intent
- Bypass tests or phases

### You DO:
- Express intent through **structured prompts**
- Let the framework control scope and safety
- Develop in **explicit phases**
- Treat documentation as authoritative

Think of prompts as **commands**, not conversations.

---

## Repository as the Source of Truth

The repository itself is the system’s memory.

Authoritative files include:
- `PRINCIPLES.md` – non-negotiable design rules
- `AGENT_RULES.md` – what agents may and may not do
- `ENGINEER_INTENT.md` – explicit human intent and rationale
- `PROJECT_LIFECYCLE.md` – phases and gates
- `SECURITY_MODEL.md` – safety and threat constraints

Chat history is **never** authoritative.

---

## How You Work Day-to-Day

You interact with the framework using **prompt templates**, not ad-hoc instructions.

### Typical Flow

1. **Cold-start the agent**
   - Use the *Cold-Start Bootstrap Prompt*
   - Forces the agent to reorient from repo state

2. **If starting from an idea**
   - Use the *Ideation → PRD Realization Prompt*
   - No code is written at this stage

3. **When building features**
   - Use *Phase-Gated Development + Mandatory Testing Prompt*
   - Testing is required before phase completion

4. **When fixing bugs**
   - Use *Dependency-Aware Debugging Prompt*
   - Then apply *Scoped Fix Prompt*

5. **Before marking anything complete**
   - Use *Test-First Validation Prompt*

6. **If something looks wrong but intentional**
   - Use *Engineer Intent Preservation Prompt*

7. **If the system or agent is wrong**
   - Use *Human Override & Feedback Prompt*

8. **If working in production**
   - Use *Production-Only Safety Prompt*

9. **When adding new features**
   - Use *Feature-Addition Control Prompt*

10. **When tools are involved**
    - Use *Minimal Free Tool Stack Mapping Prompt*

---

## You Do NOT Need to Understand the Framework Internals

You are **not expected** to know:
- Which markdown files to edit
- How lifecycle rules are enforced
- Where safeguards live

Your responsibility is to:
- Clearly describe what you want
- Use the correct prompt

The framework routes changes correctly.

---

## Human Authority Is Absolute

AI agents:
- Can suggest
- Can simulate
- Can warn

They **cannot**:
- Override documented human intent
- Undo explicit human decisions
- “Correct” unconventional designs

If you say something is intentional, it is treated as such.

---

## Testing Is Not Optional

Every phase:
- Requires tests
- Requires test summaries
- Cannot be advanced without validation

If tests are missing, the phase is incomplete.

---

## Security Is a Design Requirement

Inputs, APIs, and integrations must be designed as:
- Malicious by default
- Validated and constrained
- Safe against common attack classes

This applies even in prototypes.

---

## Platform & Tool Independence

You may:
- Change IDEs
- Change coding agents
- Lose chat history
- Onboard new engineers mid-project

As long as the repository remains intact, development can resume safely.

---

## If You Are Ever Unsure

Do **not** guess.

Instead:
- Ask for clarification
- Flag uncertainty
- Halt and wait for instruction

Silence and assumptions cause more damage than delays.

---

## Final Rule

This framework exists to protect:
- The product
- The engineers
- The users

Follow the prompts.
Trust the process.

