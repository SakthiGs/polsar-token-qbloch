# Training-environment provenance assessment

## What was inspected

A file titled \`pip_freeze.txt\` is present in Google Drive. Its listed packages include **November 2026** releases, for example \`certifi==2026.10.23\` and \`astropy-iers-data==0.2026.11.2.0.34.55\`.

This proves that this file **cannot, by itself, be the exact June 2026 training-time lockfile**. Do not pin it as if it described the published EXP37 execution. It may describe a different, newer Colab environment.

## Currently reproducible

- Github Actions checks use Python 3.11 and install the declared package ranges.
- The code verifies computational structure, parameters, synthetic execution, archive integrity and checkpoint replay when assets are provided.
- The original June 2026 exact dependencies, CUDA/driver combination and source-image checksums are still not available as a verified environment manifest.

## Action when original experiment environment is available

Capture \`python --version\`, \`python -m pip freeze\`, PyTorch/CUDA information, operating system, source-data release identifier, Git commit, and SHA-256 of the original YOLO detector weights and candidate cache. Commit only package names, versions and **digests**, never private paths, access tokens or redistributable third-party data.

A modern clean install with new packages is a **compatibility test**, not exact historical environment recovery.
