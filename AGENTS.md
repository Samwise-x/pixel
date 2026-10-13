# Agent instructions

This repository is the Pixel 11 environment and deployment control plane, not the Gallery application source.

Preserve existing device files, SSH credentials, model weights, and the adjacent `~/samwise` workspace. Inspect before modification. Never reset, clean, or overwrite an unknown worktree. Changes affecting Android host permissions or remote access require verification.

## Agent skills

### Issue tracker
GitHub Issues in `Samwise-x/pixel`; see `docs/agents/issue-tracker.md`.

### Triage labels
Canonical labels; see `docs/agents/triage-labels.md`.

### Domain docs
Single root `CONTEXT.md` for vocabulary; ADRs in `docs/adr/`; see `docs/agents/domain.md`.

On the Pixel VM, local references may also exist in `../../docs/CONTEXT.md` and `../../docs/GLOSSARY.md` relative to a `~/samwise/src/pixel` checkout. Do not overwrite those documents.

## Workflow

Start from a GitHub Issue; use Ask Matt / Wayfinder when the work needs clarification. Read root \`GLOSSARY.md\` and relevant ADRs before changing source. Research primary evidence, convert to spec and dependent tickets as needed, implement the smallest complete vertical slice, verify with deterministic gates, and summarize evidence on the issue before closing.

## Ownership

Android host owns app permissions and TPU runtime. Debian owns agent and developer tools. \`Samwise-x/pixel\` owns operational control-plane material; \`BVEnterprisess/gallery\` owns Android application source. Neither repository is a substitute for device runtime verification.

## Protection

Never reset or clean pre-existing worktrees, stage unrelated untracked files, or publish credentials. Keep \`~/samwise/docs/CONTEXT.md\` and \`~/samwise/docs/GLOSSARY.md\` unchanged. Native OpenCode gates are enforced by the installed plugin; Git hooks/CI are separate verification surfaces.
