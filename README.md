# export-gemini-context

A disciplined workflow bridging **Antigravity (AGY)** and **Gemini Chat** for large-context architectural planning and safe, evidence-backed implementation.

---

## Overview

When developing complex features or refactoring large codebases, feeding raw code into LLMs can lead to hallucinations, broken assumptions, or accidental secret leakage. 

`export-gemini-context` provides a 3-step closed-loop lifecycle:
1. **Export Snapshot (AGY)**: Generates a sanitized, evidence-backed `GEMINI_CONTEXT.md` containing repository inventory, execution paths, contracts, and configuration schemas without modifying application code or leaking secrets.
2. **Plan & Order (Gemini)**: Gemini Chat reviews the exported context, clarifies trade-offs, and produces a structured work order (`AGY_CHANGE_REQUEST.md`).
3. **Revalidate & Implement (AGY)**: AGY revalidates the work order against the live working tree (Phase 1), reports drift or discrepancies, and executes only after explicit human approval (Phase 2).

```mermaid
flowchart LR
    A["Workspace Codebase"] -->|"1. export-gemini-context"| B["GEMINI_CONTEXT.md"]
    B -->|"2. gemini-planning.md"| C["Gemini Chat Planner"]
    C -->|"Produces"| D["AGY_CHANGE_REQUEST.md"]
    D -->|"3. agy-implementation.md"| E["AGY Revalidation"]
    E -->|"Human Approval"| F["Safe Implementation"]
```

---

## Repository Structure

```text
export-gemini-context/
├── plugin.json                       # Antigravity Plugin manifest (enables / slash commands)
├── skills/                           # Plugin skills directory
│   ├── export-gemini-context/
│   │   └── SKILL.md
│   └── agy-implementation/
│       └── SKILL.md
├── .agents/skills/                   # Standard Agent Skills structure
├── prompts/
│   ├── gemini-planning.md            # Prompt for architectural planning in Gemini
│   └── agy-implementation.md         # Reference implementation prompt
├── .gitignore                        # Prevents committing exported context and secrets
└── README.md                         # Documentation and usage guide
```

---

## Quick Start

### 1. Install the Skill

Copy the `.agents/skills/export-gemini-context/` directory into your target project:

```bash
# In your target project root
mkdir -p .agents/skills/export-gemini-context
cp path/to/export-gemini-context/.agents/skills/export-gemini-context/SKILL.md .agents/skills/export-gemini-context/
```

Antigravity automatically discovers skills inside `.agents/skills/`.

### 2. Export Context in Antigravity

In your Antigravity chat console, simply type the slash command:

```text
/export-gemini-context
```

Antigravity executes the skill, redacts secrets, and writes `GEMINI_CONTEXT.md` to your workspace root.

### 3. Plan in Gemini Chat (Automate with Gemini Gems)

1. Open [Gemini](https://gemini.google.com).
2. (Recommended) Create a custom **Gem** (e.g. "AGY Architect") and paste [`prompts/gemini-planning.md`](./prompts/gemini-planning.md) into its System Instructions. You will never need to copy-paste the prompt again.
3. Attach `GEMINI_CONTEXT.md`.
4. State your requested change, business outcome, and constraints.
5. Gemini generates `AGY_CHANGE_REQUEST.md`.

### 4. Implement in Antigravity

1. Save the generated work order as `AGY_CHANGE_REQUEST.md` in your project root.
2. In your Antigravity chat console, run the implementation slash command:
   ```text
   /agy-implementation
   ```
3. AGY runs **Phase 1 (Revalidation)** and reports whether the current workspace matches the snapshot.
4. When satisfied with the revalidated plan, approve implementation with:
   ```text
   APPROVE IMPLEMENTATION: <request_id>
   ```
5. AGY executes **Phase 2 (Implementation)** and verifies the acceptance criteria.

---

## Security & Privacy Guidelines

- **Never commit context exports**: `GEMINI_CONTEXT.md` is meant for planning sessions. Keep it in `.gitignore`.
- **Review before sharing**: Although `export-gemini-context` redacts secrets and suppresses `.env` files by design, always review the generated markdown before uploading to any external chat.
- **Strict Human Approval Gate**: AGY will never modify files from a work order until you explicitly approve the revalidation report.

---

## License

MIT
