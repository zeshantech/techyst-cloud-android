<!--
  ~ SPDX-FileCopyrightText: 2026 Zeshan Shakil
  ~ SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-only

  DRAFT — two facts must be supplied before this is published, because they are
  legal statements that cannot be inferred from the code:

    1. The legal name and postal address of the data controller (the person or
       company operating cloud.techyst.net). "Techyst" alone is a trade name,
       and GDPR Art. 13 requires the controller's identity and contact details.
    2. The governing jurisdiction, which also decides whether a data protection
       officer or an EU/UK representative has to be named.

  Both appear below marked with >>> . Have the final text reviewed by someone
  qualified in the jurisdiction you choose; this draft is written to be accurate
  about what the software does, which is a different question from whether it
  satisfies a particular regulator.

  Publish at: https://techyst.net/cloud/privacy  (the app links to that URL from
  Settings, and Google Play requires a reachable privacy policy URL).
-->
# Techyst Cloud — Privacy Policy

**Last updated:** 15 September 2026

This policy explains what Techyst Cloud does with your information. It covers
the Techyst Cloud service at `cloud.techyst.net` and the Techyst Cloud app for
Android.

>>> The controller of your personal data is **[legal name]**, **[postal
>>> address]**. You can reach us at **team@techyst.net**.

## The short version

Your files stay on the Techyst Cloud server. We do not sell your data, we do not
advertise to you, and the app contains no analytics or tracking SDKs. The only
third party involved in normal use is Google, whose notification service tells
your phone that something changed — and it cannot read what changed.

## What we hold, and why

### Your account

When an account is created we store your username, display name, email address
and a hash of your password. We need these to authenticate you and to send you
service email such as a password reset or a share notification.

If you register yourself through the sign-up page, we also record that your
email address was verified and that an administrator approved the account.

**Lawful basis:** performance of our contract with you.

### Your content

Files, folders, photos, calendars, contacts, notes, task boards, chat messages
and anything else you put into Techyst Cloud are stored on our server so we can
give them back to you. We do not read them, index them for advertising, or
disclose them, except as described under *Disclosure* below.

Some content is stored because you asked the app to store it:

* **Photos and videos** are uploaded only if you turn on auto-upload, or when
  you upload them by hand.
* **Contacts and calendars** are backed up only if you turn on those backups.

**Lawful basis:** performance of our contract with you.

### Technical records

* **Server logs.** Web server and application logs record the request, the
  time, the response status, your IP address and your user agent. They exist to
  operate the service, investigate faults and detect abuse such as brute-force
  login attempts.
* **Sessions and devices.** We record the devices and app sessions connected to
  your account so you can see and revoke them.
* **Notification registration.** If you use the Android app, we store a token
  issued by Google Firebase Cloud Messaging that identifies your app
  installation, together with your device's public key.

**Lawful basis:** our legitimate interest in running a secure, working service.

## How long we keep it

| Data | Retention |
| --- | --- |
| Account and content | Until you or an administrator deletes it |
| Deleted files | In your trash until you empty it or the server's retention window expires, then permanently |
| File versions | Per the server's version-retention settings |
| Server logs | 30 days, then rotated away |
| Notification registrations | Until you sign out, remove the account, or uninstall the app |

## Who we share it with

We do not sell your data and we do not share it for advertising. Data reaches a
third party only in these cases:

### Google Firebase Cloud Messaging

To notify your phone promptly, the app registers with Google's Firebase Cloud
Messaging and we send notifications through it.

What Google receives is a message addressed to your app installation whose
payload is **encrypted with your device's own RSA public key** before it leaves
our server. Google, and our own notification relay, can see that a notification
was sent and to which installation, but not what it says. Your app decrypts it
on your phone.

Google's handling of this is governed by the
[Firebase Privacy and Security](https://firebase.google.com/support/privacy)
terms. If you install a build of the app without Google Play Services, no
notification token is created and nothing is sent to Google.

### Email delivery

Service email — verification, password resets, share notifications — is sent
through Google's SMTP service. The recipient address and the message content
pass through it.

### Hosting

The server runs on Amazon Web Services infrastructure in the `us-east-1`
region (Northern Virginia, United States). AWS provides the machine and storage;
it does not process your content for its own purposes.

>>> If your users are in the EEA or the UK, note that this means personal data
>>> is transferred to the United States, and the final policy must say which
>>> transfer mechanism you rely on.

### Other people you share with

If you share a file or folder, the people you share it with can see it. If you
create a public link, anyone holding that link can see it until it expires or
you delete it. That is the feature working as intended, but it is a disclosure
you control, so it is worth stating plainly.

### When we are legally required to

We may disclose data if we are compelled to by valid legal process, or where it
is necessary to protect the rights, safety or property of our users or
ourselves.

## Security

* All connections use HTTPS. The app refuses to connect over plain HTTP.
* Passwords are stored only as hashes.
* Notification contents are end-to-end encrypted between the server and your
  device, as described above.
* Two-factor authentication is available and we recommend turning it on.
* The app can be locked with a passcode, a fingerprint or your device
  credentials.
* Repeated failed logins are rate-limited.

No system is perfectly secure. If you believe your account has been
compromised, email **team@techyst.net**.

## Your rights

Depending on where you live, you may have the right to access, correct, export,
delete or restrict the processing of your personal data, and to object to it.
Several of these you can exercise yourself:

* **Access and export** — *Settings → Personal → Data exported* in the web
  interface produces an archive of your account.
* **Correction** — edit your profile in the web interface.
* **Deletion** — ask us and we will delete your account and content.

For anything else, email **team@techyst.net**. We will respond within 30 days.

>>> If you believe we have handled your data improperly you may complain to
>>> your local data protection authority. Name the relevant authority for your
>>> chosen jurisdiction here.

## Children

Techyst Cloud is not intended for children under 16, and we do not knowingly
collect their personal data. If you believe a child has created an account,
email **team@techyst.net** and we will remove it.

## Changes

If we change this policy we will update the date at the top and, where the
change is significant, tell account holders by email.

## Contact

**team@techyst.net**
