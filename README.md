# pkg-rpm-kgsl

This repository has RPM packaging rules and scripts for kgsl project present at https://github.com/qualcomm-linux/kgsl.

## Branch model

This template follows the Fedora/CentOS **dist-git** convention: **one branch per
distro stream**, with the packaging files at that branch's root.

| Branch | Role | Contents |
|---|---|---|
| `main` | Template + docs home. **Nothing is built here.** | This README, [docs/](docs/), community files, workflows. |
| `c10s` | **CentOS 10 Stream package branch — where you work.** | Your `kgsl-dkms.spec` + `sources` at the root, plus the workflows. |

Future streams get their own branch (`c11s`, …) off the same model, so one repo
can carry a package for several distro versions without branching history.

## Updating the package version

This is the everyday workflow — **two edits on `c10s`, no tarball in git**:

1. Bump `Version:` in the spec (and the `Source0:` URL if its path changed).
2. Recompute the checksum for the new tarball:
   ```bash
   sha512sum --tag <component>-<newversion>.tar.gz > sources
   ```
3. Commit the spec + `sources`, open a PR (build verifies it), merge, then run
   **Release**. The first release fetches the new upstream tarball, verifies it,
   and caches it back to Artifactory automatically.

### License

pkg-rpm-kgsl is licensed under the [BSD-3-Clause License](https://spdx.org/licenses/BSD-3-Clause.html). See [LICENSE.txt](https://github.com/qualcomm-linux/pkg-rpm-kgsl/blob/main/LICENSE.txt) for the full license text.