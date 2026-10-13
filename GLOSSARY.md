# Pixel 11 ? Domain glossary

Canonical vocabulary for agents operating this repository.
The adjacent Debian workspace glossary remains an independent document.

- **Android host** ? Pixel 11 Android runtime; owns permissions, applications, TPU execution, Shizuku+, and voice IO.
- **Debian guest** ? Android Virtualization Framework VM; owns development tools, Git checkout, OpenCode runtime, and SSH.
- **Tailnet identity** ? separately authenticated Debian Tailscale node, distinct from Android.
- **Pixel repository** ? \`Samwise-x/pixel\`, environment operations and development control plane.
- **Gallery fork** ? \`BVEnterprisess/gallery\`, Android application implementation; not installed by this repository.
- **Shizuku+** ? Android-host privileged service; does not automatically authorize Debian or OpenCode.
- **Agent bridge** ? explicitly authorized interface linking Android actions to Debian tools; not deployed.
- **Execution gate** ? a deterministic policy hook that admits or denies an operation independent of model output.
- **ADR** ? a versioned record for a lasting architecture decision.

## Existing VM glossary reference

# Glossary
- **AVF**: Android Virtualization Framework.
- **Guest**: Isolated Linux virtual machine on the Pixel.
- **APT**: Debian package manager.
- **Remote Desktop Commander**: Authorized remote terminal access.
