#!/usr/bin/env python3
"""Fold a Firebase google-services.json into the gplay flavour's resources.

This fork does NOT apply the com.google.gms.google-services Gradle plugin —
upstream configures Firebase through plain string resources in
app/src/gplay/res/values/setup.xml, and the Firebase SDK reads those. So the
build never parses google-services.json; this script transcribes it.

    python3 branding/apply-firebase.py path/to/google-services.json

The file is not a secret: everything in it ships inside the APK and is
world-readable there. It is committed so CI can build without extra inputs.
"""
import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SETUP = ROOT / "app/src/gplay/res/values/setup.xml"
PACKAGE = "net.techyst.cloud"


def pick_client(data, package):
    for client in data.get("client", []):
        if client.get("client_info", {}).get("android_client_info", {}).get("package_name") == package:
            return client
    have = [
        c.get("client_info", {}).get("android_client_info", {}).get("package_name")
        for c in data.get("client", [])
    ]
    sys.exit(
        f"google-services.json has no Android client for {package}.\n"
        f"Clients present: {have or 'none'}\n"
        f"Add an Android app with package name {package} in the Firebase console "
        f"and download the file again."
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("google_services_json")
    ap.add_argument("--package", default=PACKAGE)
    args = ap.parse_args()

    data = json.loads(pathlib.Path(args.google_services_json).read_text())
    info = data["project_info"]
    client = pick_client(data, args.package)

    api_keys = client.get("api_key") or []
    if not api_keys:
        sys.exit("the Android client in google-services.json carries no api_key")
    api_key = api_keys[0]["current_key"]

    # client_type 3 is the OAuth web client; only present when a Google sign-in
    # provider is configured. The Nextcloud client does not use Google sign-in,
    # so an empty value here is expected and harmless.
    web_client = next(
        (o["client_id"] for o in client.get("oauth_client", []) if o.get("client_type") == 3),
        "",
    )

    values = {
        "project_id": info["project_id"],
        "gcm_defaultSenderId": info["project_number"],
        "google_app_id": client["client_info"]["mobilesdk_app_id"],
        "google_api_key": api_key,
        "google_crash_reporting_api_key": api_key,
        "google_storage_bucket": info.get("storage_bucket", ""),
        "firebase_database_url": info.get("firebase_url", ""),
        "default_web_client_id": web_client,
    }

    text = original = SETUP.read_text(encoding="utf-8")
    for key, value in values.items():
        pattern = re.compile(
            rf'(<string\s+name="{re.escape(key)}"((?:\s+[a-zA-Z:]+="[^"]*")*)\s*)(?:/>|>(.*?)</string>)',
            re.DOTALL,
        )
        m = pattern.search(text)
        if not m:
            sys.exit(f"{SETUP.name} has no <string name=\"{key}\">")
        old = m.group(3) or ""
        if old != value:
            print(f"{key}: {old or '(empty)'} -> {value or '(empty)'}")
        text = text[:m.start()] + f"{m.group(1)}>{value}</string>" + text[m.end():]

    if text != original:
        SETUP.write_text(text, encoding="utf-8")
        print(f"\nwrote {SETUP.relative_to(ROOT)}")
    else:
        print("already up to date")

    # Keep the canonical file alongside the flavour for reference and so the
    # Firebase console's own tooling finds it where it expects.
    dest = ROOT / "app/src/gplay/google-services.json"
    dest.write_text(json.dumps(data, indent=2) + "\n")
    print(f"wrote {dest.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
