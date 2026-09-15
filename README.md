<!--
  ~ SPDX-FileCopyrightText: 2026 Zeshan Shakil
  ~ SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-only
-->
# Techyst Cloud for Android

The Android client for **[Techyst Cloud](https://cloud.techyst.net)** — file
sync and share, calendar, contacts, notes and chat, on your own server.

This is a rebranded build of the Nextcloud Android client. It is **not**
produced, endorsed or supported by Nextcloud GmbH. Read
**[FORK.md](FORK.md)** for the upstream commit it derives from, the licence
notices, the corresponding-source offer and the full list of changes.

* Package name: `net.techyst.cloud`
* Server: pinned to `https://cloud.techyst.net` — the app does not ask for a
  server URL
* Licence: GPL-2.0-only, and AGPL-3.0-or-later for files upstream has
  relicensed. No warranty.

## Building

Requirements: JDK 21 and the Android SDK (compileSdk 37). The Gradle wrapper
brings its own Gradle.

```sh
# The generic flavour has no Firebase dependency and builds with no extra setup.
./gradlew assembleGenericDebug
```

The `gplay` flavour adds Firebase Cloud Messaging and needs a Firebase project
of its own — Nextcloud's FCM sender only serves the official apps, so push
notifications in a rebranded build require both your own Firebase project and
your own push proxy. Once you have `google-services.json`:

```sh
python3 branding/apply-firebase.py path/to/google-services.json
./gradlew bundleGplayRelease
```

### Release signing

The upload key is never committed. Provide it either through a gitignored
`keystore.properties` in the repository root:

```properties
storeFile=/absolute/path/to/upload.jks
storePassword=...
keyAlias=techyst-cloud-upload
keyPassword=...
```

…or through the environment (`TECHYST_KEYSTORE_PATH`,
`TECHYST_KEYSTORE_PASSWORD`, `TECHYST_KEY_ALIAS`, `TECHYST_KEY_PASSWORD`).
With neither present the build still succeeds and simply leaves release
artifacts unsigned, so you can build the project without our key.

Releases are produced by the `release-aab` workflow, which builds
`bundleGplayRelease` from a tagged commit and uploads the `.aab` as a run
artifact for manual upload to the Play Console.

## Branding

Every brand value lives in `app/src/main/res/values/setup.xml` and is applied
by a single re-runnable script:

```sh
python3 branding/apply-branding.py          # apply
python3 branding/apply-branding.py --check  # verify (used by CI)
```

## Reporting problems

Open an issue at
<https://github.com/zeshantech/techyst-cloud-android/issues>. Please do not
report problems with this build to Nextcloud — they cannot support it.
