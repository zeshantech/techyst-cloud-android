<!--
  ~ SPDX-FileCopyrightText: 2026 Zeshan Shakil
  ~ SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-only
-->
# Play Store listing — Techyst Cloud

Draft copy for the Play Console. Character limits are Google's and are noted
next to each field; the counts given are for the text as written here.

Everything below describes what the app actually does today. Nothing claims a
feature the build does not ship — a listing that oversells is both a review
risk and a support burden.

---

## App details

| Field | Value |
| --- | --- |
| App name (30) | `Techyst Cloud` (13) |
| Package name | `net.techyst.cloud` |
| Default language | English (United States) |
| App or game | App |
| Free or paid | Free |
| Category | Productivity |
| Tags | Files, Cloud storage, Collaboration |
| Contact email | team@techyst.net |
| Contact website | https://techyst.net/cloud |
| Contact phone | *optional — leave blank* |
| External marketing | Off (no ads) |

## Short description (80 max)

> Private file sync, calendar, contacts and notes on your Techyst Cloud account.

*(75 characters)*

## Full description (4000 max)

> Techyst Cloud keeps your files on your own server and in sync with your
> phone — nothing is shared with an advertising network, and no third party
> holds the keys.
>
> The app connects to a single Techyst Cloud account. Sign in with your
> credentials and your files, calendars, contacts and notes are available
> offline and kept up to date in the background.
>
> WHAT YOU CAN DO
>
> • Browse, search, open and share every file in your account
> • Upload photos and videos automatically as you take them, on Wi-Fi only if
>   you prefer
> • Work offline — mark anything as available offline and changes sync when you
>   reconnect
> • Share files and folders with other people, or by link with an optional
>   password and expiry date
> • Open and edit documents, spreadsheets and presentations in the built-in
>   office suite
> • Back up your contacts and calendars
> • Read and write notes, and keep task boards up to date
> • Protect the app with a passcode, your fingerprint or your device
>   credentials
> • Turn on two-factor authentication for your account
>
> PRIVACY
>
> Your data lives on the Techyst Cloud server, not in a shared platform. The
> app talks only to that server and to Google's notification service, which is
> used to tell your phone that something changed — the contents of every
> notification are encrypted with a key that only your device holds, so neither
> Google nor the notification relay can read them.
>
> The app contains no advertising, no analytics and no third-party trackers.
>
> WHAT YOU NEED
>
> An account on Techyst Cloud. The app does not create accounts and cannot
> connect to any other server.
>
> OPEN SOURCE
>
> Techyst Cloud for Android is free software, released under the GNU General
> Public License. It is a modified version of the Nextcloud Android client and
> is not produced, endorsed or supported by Nextcloud GmbH. The complete
> corresponding source code for this app, including every modification, is
> published at:
>
> https://github.com/zeshantech/techyst-cloud-android
>
> This program is distributed in the hope that it will be useful, but WITHOUT
> ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
> FOR A PARTICULAR PURPOSE.

*(approximately 2,050 characters)*

---

## Graphic assets Google requires

These must be produced before the listing can be submitted. Sizes are Google's
current requirements.

| Asset | Requirement | Status |
| --- | --- | --- |
| App icon | 512 × 512 PNG, 32-bit, no alpha | Generate from `.brand` — see below |
| Feature graphic | 1024 × 500 PNG or JPEG, no alpha | **Not yet produced** |
| Phone screenshots | 2–8 images, 16:9 or 9:16, min 1080 px on the short side | **Not yet produced** — needs a signed build on a device or emulator |
| 7-inch tablet screenshots | optional | Not planned |
| 10-inch tablet screenshots | optional | Not planned |

The 512 px icon comes from the workspace brand pipeline rather than being
hand-drawn:

```sh
python3 - <<'PY'
import sys; sys.path.insert(0, '../.brand')
import products, gen_raster
b = products.brand('techyst')
gen_raster.render(512, letter=b['mark'], primary=b['primary'], dot=b['dot'],
                  tile=b['deep'], ink='#F1F5F9').save('play-icon-512.png')
PY
# Play rejects alpha channels on the store icon, so flatten it:
#   convert play-icon-512.png -background '#14435A' -alpha remove -alpha off play-icon-512-flat.png
```

Screenshots cannot be produced until there is an installable build, which needs
the Firebase configuration. Capture them from the internal-testing build.

## Content rating questionnaire

Answer the Play questionnaire as follows. These answers describe this app
honestly; do not copy them to a different app without rechecking.

| Question | Answer |
| --- | --- |
| Category | Utility, productivity, communication or other |
| Violence, sexuality, profanity, drugs, gambling | No to all |
| Does the app share user location? | No |
| Does the app allow users to interact or exchange content? | **Yes** — users can share files and links with other users of the same server |
| Does the app allow users to purchase digital goods? | No |
| Is the app primarily a news app? | No |
| Does the app contain ads? | No |

The "users can interact" answer matters: file and link sharing is
user-to-user content exchange, and answering no would be inaccurate.

## Data safety form

| Data type | Collected | Shared | Purpose | Notes |
| --- | --- | --- | --- | --- |
| Files and documents | Yes | No | App functionality | Uploaded to the user's own Techyst Cloud server at their instruction |
| Photos and videos | Yes | No | App functionality | Only when the user enables auto-upload or uploads by hand |
| Contacts | Yes | No | App functionality | Only when the user enables contacts backup |
| Calendar | Yes | No | App functionality | Only when the user enables calendar backup |
| Name, email address | Yes | No | Account management | The account the user signs in with |
| App activity, crash logs, diagnostics | No | No | — | No analytics or crash reporting SDK is present |
| Device or other identifiers | Yes | No | App functionality | The FCM registration token, used only to deliver notifications |

Also declare:

* **Data is encrypted in transit** — yes (HTTPS throughout; the app will not
  connect over plain HTTP).
* **Users can request data deletion** — yes, via the server administrator at
  team@techyst.net. Provide that address as the deletion-request URL/contact.
* **Independent security review** — no.
* **Committed to the Play Families policy** — no (not aimed at children).

## Release plan

1. **Internal testing** first, as decided. Create the track, add testers by
   email address, upload the `.aab` from the `release-aab` workflow run.
2. Google will ask you to opt into **Play App Signing** on the first upload.
   Accept: our key (`techyst-cloud-upload`) then becomes the *upload* key only,
   and Google holds the app signing key.
3. After Google generates the app signing certificate, copy **both** SHA-1
   fingerprints — the upload certificate's and the app signing certificate's —
   into the Firebase Android app, or push notifications will not reach
   production builds. See `docs/FIREBASE.md`.
4. Promote to closed or production testing only once notifications, login and
   auto-upload have been confirmed on a real device.

## First-release fields Google will also ask for

* **App access** — the app requires an account. Provide review credentials: a
  dedicated Techyst Cloud test account, not a real user's. Create it with
  `occ user:add` on the server and note it in the Play Console's "All or some
  functionality is restricted" section.
* **Ads** — no.
* **Target audience** — 18+ (this is an account-holder tool, not a general
  consumer app).
* **News app** — no.
* **COVID-19 apps** — no.
* **Data safety** — as above.
* **Government apps** — no.
* **Financial features** — none.
* **Health** — none.
