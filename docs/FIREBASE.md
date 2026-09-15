<!--
  ~ SPDX-FileCopyrightText: 2026 Zeshan Shakil
  ~ SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-only
-->
# Firebase setup for Techyst Cloud

Do these steps in order. Two artifacts come out of them:

1. **`google-services.json`** — goes into this repository (it is not a secret;
   every value in it ships inside the APK).
2. **A service account JSON key** — goes on the server, for the push proxy.
   This one **is** a secret and must never be committed.

## Why a Firebase project of our own is unavoidable

Nextcloud's push proxy at `push-notifications.nextcloud.com` sends through
Nextcloud's own FCM sender id. An FCM registration token is issued *to a
specific sender*, and no other sender can deliver to it. A rebranded app
registers with its own Firebase project, so its tokens are invisible to
Nextcloud's proxy — which is why this deployment runs its own push proxy at
`push.cloud.techyst.net`, and why that proxy needs FCM credentials of its own.

There is no way around this short of dropping native push and falling back to
periodic polling.

---

## 1. Create the Firebase project

1. Go to <https://console.firebase.google.com> and sign in with the Google
   account that should own this.
2. **Add project**.
3. Project name: `Techyst Cloud`. Accept or edit the generated project id
   (something like `techyst-cloud-4f2a1`); note it down.
4. **Google Analytics: turn it off.** The app has no analytics SDK, the Play
   data-safety declaration says we collect no analytics, and enabling it here
   would make that declaration wrong.
5. **Create project**, then wait for it to finish provisioning.

## 2. Register the Android app

1. On the project overview, click the **Android** icon ("Add app").
2. **Android package name** — exactly:

   ```
   net.techyst.cloud
   ```

   This must match `applicationId` in `app/build.gradle.kts`. A mismatch means
   the app silently receives nothing.
3. **App nickname**: `Techyst Cloud` (internal label only).
4. **Debug signing certificate SHA-1** — enter the upload key's SHA-1:

   ```
   BE:49:A7:7F:93:7D:B7:BD:2C:A9:CB:0F:1E:26:AF:BA:4A:D5:DA:3B
   ```

   (SHA-256, if a field asks for it:
   `32:E7:B6:0E:8A:0E:53:94:27:46:50:0F:D7:84:2A:81:EF:18:76:F9:26:FB:23:B9:46:5B:09:48:54:12:8E:B1`)

   FCM itself does not need a fingerprint, so this is not what makes push work
   — but registering it now avoids a confusing detour later.
5. **Register app**, then **Download `google-services.json`**.
6. Skip the "Add Firebase SDK" and "Verify installation" steps. This project
   configures Firebase through string resources, not through the
   `google-services` Gradle plugin, so there is nothing to add to the build
   files.

### After Play App Signing is enabled

Google re-signs your bundle with its own key, so production builds carry a
**different** certificate from the one you uploaded with. Once you have
uploaded the first bundle:

1. Play Console → your app → **Test and release → Setup → App integrity → App
   signing**.
2. Copy the **App signing key certificate** SHA-1.
3. Firebase Console → **Project settings → General → Your apps →** the Android
   app → **Add fingerprint**, and paste it.

Do this before promoting beyond internal testing. Skipping it is the usual
reason push works for an internally tested build and then stops in production.

## 3. Put the configuration into the app

From the repository root:

```sh
python3 branding/apply-firebase.py ~/Downloads/google-services.json
```

That writes the eight Firebase values into
`app/src/gplay/res/values/setup.xml` and stores a copy of the file at
`app/src/gplay/google-services.json`. It refuses to proceed if the file has no
Android client for `net.techyst.cloud`, which is the mistake that is otherwise
hardest to spot.

Commit both files:

```sh
git add app/src/gplay/res/values/setup.xml app/src/gplay/google-services.json
git commit -m "Configure Firebase for net.techyst.cloud"
git push
```

The `release-aab` workflow refuses to build while `google_app_id` is empty, and
also refuses if `gcm_defaultSenderId` is still Nextcloud's — so a build can
never quietly ship without working notifications.

## 4. Create the service account for the push proxy

The proxy sends through the FCM HTTP v1 API, which authenticates with a service
account rather than a legacy server key.

1. Firebase Console → **Project settings** (gear icon) → **Service accounts**.
2. **Generate new private key** → **Generate key**. A JSON file downloads.
3. That file is a credential. Do not commit it, do not paste it into chat, and
   do not email it.

If you would rather scope it tightly, create the account in Google Cloud IAM
instead and grant only **Firebase Cloud Messaging API Admin**
(`roles/firebasecloudmessaging.admin`); the key Firebase generates above has
broader project access than the proxy needs.

Also confirm the API is on: Google Cloud Console →
**APIs & Services → Enabled APIs** → *Firebase Cloud Messaging API*. It is
normally enabled with the project.

## 5. Install the key on the server

```sh
# from the workspace root, with the downloaded key at ~/Downloads/fcm-sa.json
scp -i saas-techyst.pem ~/Downloads/fcm-sa.json \
    ec2-user@100.60.251.232:/tmp/fcm-sa.json

ssh -i saas-techyst.pem ec2-user@100.60.251.232 '
  install -d -m 700 ~/saas/25-nextcloud/.secrets
  install -m 600 /tmp/fcm-sa.json ~/saas/25-nextcloud/.secrets/fcm-service-account.json
  shred -u /tmp/fcm-sa.json
  cd ~/saas/25-nextcloud && docker compose up -d push-proxy
  sleep 5 && curl -fsS http://127.0.0.1:8001/healthz'
```

`/healthz` should report `"fcm_configured": true`. Until the key is in place the
proxy answers `503` on `/notifications` — deliberately, so the Nextcloud side
logs a clear reason instead of assuming delivery succeeded.

## 6. Verify end to end

With a signed build installed and signed in:

```sh
# On the server: watch the proxy register the device, then deliver.
ssh -i saas-techyst.pem ec2-user@100.60.251.232 \
  'docker logs -f techyst-cloud-push-proxy'

# Force Nextcloud to send a test notification to your user.
ssh -i saas-techyst.pem ec2-user@100.60.251.232 \
  'docker exec --user www-data nextcloud-aio-nextcloud php occ \
     notification:generate <your-username> "Techyst Cloud" -l "push test"'
```

You should see, in order:

1. `registered device …` in the proxy log, when the app first signs in.
2. A `POST /notifications` in the proxy log when the test fires.
3. The notification on the phone.

If step 1 never happens, the app is not reaching the proxy — check DNS for
`push.cloud.techyst.net` and the Caddy route. If step 2 happens but the phone
stays silent, the FCM token belongs to a different sender: confirm
`gcm_defaultSenderId` in the app matches the `project_number` of the Firebase
project whose service account the proxy is using.
