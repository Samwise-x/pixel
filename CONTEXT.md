# Pixel domain vocabulary

- **Android host** — Pixel 11 Android runtime; owns APK execution, microphone/audio, permissions, Shizuku+, and TPU inference.
- **Debian guest** — Linux VM; hosts local source, development tooling, agent access, and diagnostics.
- **Pixel worktree** — this repository, intended for `~/samwise/src/pixel` in the guest.
- **Gallery fork** — `BVEnterprisess/gallery`, the Android app source.
- **Tailnet identity** — a distinct Tailscale node for Debian, separate from Android host Tailscale.
- **Agent access** — authenticated remote control over Tailscale and SSH.

Operational evidence belongs in tests, scripts, and ADRs, not in the vocabulary.
