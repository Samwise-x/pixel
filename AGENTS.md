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
