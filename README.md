# Samwise × Pixel

Canonical repository for the Pixel 11 Android host and Debian 13 VM: environment discovery, agent access, Tailscale connectivity, Android deployment, and reproducible validation.

- Existing local VM workspace: `/home/droid/samwise` (preserve in place).
- Gallery Android application source: https://github.com/BVEnterprisess/gallery
- Shizuku+ Android host service: https://github.com/thejaustin/ShizukuPlus

Android APKs, TPU models, and privileged host permissions belong to the Android runtime. This repository owns scripts, documented decisions, and validated provisioning for the Debian guest and device integration. No credentials, model weights, or private state are stored here.

## Agent workflow

The checkout on Android's Debian VM is \`~/samwise/src/pixel\`. OpenCode v2 reads \`AGENTS.md\` and \`.agents/skills/\`. Read \`GLOSSARY.md\` before changing domain language; use \`CONTEXT.md\` as supporting architecture context. GitHub Issues is the tracker; triage conventions are under \`docs/agents/\`. Durable decisions go into \`docs/adr/\`.

The app \`BVEnterprisess/gallery\` and Shizuku+ Android permission bridge are separate workstreams; neither is deployed simply by cloning this repository.

### Verification

\`node --experimental-strip-types --test .opencode/tests/*.test.mjs\` verifies current policy hook expectations; GitHub Actions runs the same suite. The v2 runtime and Android Shizuku bridge require separate integration verification on device.
