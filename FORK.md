# Techyst Cloud for Android — provenance and licence notices

This repository is a rebranded build of the **Nextcloud Android client**. It is
not produced, endorsed or supported by Nextcloud GmbH.

## Upstream

| | |
| --- | --- |
| Upstream project | https://github.com/nextcloud/android |
| Forked from commit | `f50eaf4b732388cf323f164e421151249977f23e` |
| Commit date | 2026-09-15T17:44:37+02:00 |
| Upstream licence | GPL-2.0-only, and AGPL-3.0-or-later for files added since the relicence |

Upstream's commit history is preserved here exactly as published. It is not
rewritten or reattributed: the GPL requires that authorship notices survive, and
several thousand commits in this history are other people's work. Only commits
made for this fork carry Techyst authorship.

## Licence and corresponding source

Techyst Cloud for Android is free software under the **GNU General Public
License, version 2** (and, for the files upstream has relicensed, the **GNU
Affero General Public License, version 3 or later**). It comes with **no
warranty**, to the extent permitted by law.

The complete corresponding source code for every published build — including
every modification described below — is this repository:

> **https://github.com/zeshantech/techyst-cloud-android**

Each Play Store release is built from a tagged commit here by the
`release-aab` GitHub Actions workflow, so the published binary and the tag
correspond. If you cannot obtain the source from that URL, write to
**team@techyst.net** and a copy will be provided.

Full licence texts are in [`LICENSE.txt`](LICENSE.txt) and
[`LICENSES/`](LICENSES/). Per-file copyright and licensing follow the
[REUSE](https://reuse.software) metadata in [`REUSE.toml`](REUSE.toml).

## Trademarks

"Nextcloud" and the Nextcloud logo are trademarks of Nextcloud GmbH. This build
does not use them:

* Upstream's launcher icon (`app/src/main/res/drawable/ic_launcher_foreground.xml`)
  and login logo (`app/src/main/res/drawable/logo.xml`) were distributed under
  `LicenseRef-NextcloudTrademarks`, which does not permit redistribution in a
  rebranded build. Both were **replaced**, along with every raster launcher and
  store icon, with the Techyst mark.
* The visible product name is "Techyst Cloud" throughout.

"Techyst" and the Techyst mark are trademarks of the Techyst project. The GPL
grants you rights to the code, not to the branding: if you redistribute a
modified version, replace the Techyst name and mark with your own.

## What was changed

All branding lives in resource values, not in code. The changes are applied by
[`branding/apply-branding.py`](branding/apply-branding.py), which is
re-runnable and self-documenting; `--check` verifies in CI that the tree is
still branded.

* **Application id** `com.nextcloud.client` → `net.techyst.cloud`, for the
  `generic` and `gplay` flavours (the ones we ship).
* **Namespaced identifiers** — account type, all four content-provider
  authorities, the database file and name, the data folder and the deep-link
  scheme — were renamed so this app can be installed alongside the official
  Nextcloud client without the two colliding.
* **Single-tenant login.** `enforce_servers` pins the app to
  `https://cloud.techyst.net`; the server URL field and the "register with a
  provider" path are removed from the login screen.
* **Push.** `push_server_url` points at this deployment's own push proxy,
  because Nextcloud's proxy only serves the official apps' FCM sender id.
* **Icons and palette** replaced with the Techyst mark and the Techyst tokens
  (primary `#1E7096`, deep `#195673`, accent `#E77129`).
* **Links** — privacy, terms, source, issues — point at Techyst pages and this
  repository. Upstream's help forum, F-Droid channels, Transifex project and
  "participate" screen are switched off rather than pointed at pages that
  cannot answer for this build.
* **Workflows.** Every inherited GitHub Actions workflow was removed: several
  targeted the `ubuntu-latest-low` runner label, which exists only in the
  Nextcloud organisation, and others required upstream-only secrets. Upstream's
  committed QA keystore was removed with them. Two workflows replace them —
  `build.yml` and `release.yml`.

### Deliberately left alone

* **Licence files, SPDX headers and copyright lines.** Upstream holds the
  copyright; rewriting those would misattribute their work.
* **`nextcloud_user_agent` / `office_user_agent`.** The server reads the
  client name out of the user agent to gate client-specific behaviour, so these
  are API compatibility identifiers rather than branding.
  `name_for_branded_user_agent` is the supported place for our name, and that
  is where it goes.
* **Java and Kotlin package names** (`com.owncloud.android`,
  `com.nextcloud.client`). Internal identifiers; renaming them would churn
  thousands of files for no user-visible gain and destroy the merge path for
  upstream security fixes.
