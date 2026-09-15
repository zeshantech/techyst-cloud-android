#!/usr/bin/env python3
"""Apply the Techyst Cloud identity to this Nextcloud Android fork.

Re-runnable: every edit is an exact-value replacement on a known resource key,
so running it twice is a no-op. Run from the repository root:

    python3 branding/apply-branding.py [--check]

--check reports what would change without writing, for CI.

What this deliberately does NOT touch
-------------------------------------
* LICENCE files, SPDX headers, copyright lines and NOTICE text. Upstream holds
  the copyright; a brand pass that rewrites those misattributes their work and
  breaks the GPL notice requirements.
* `nextcloud_user_agent` / `office_user_agent`. The server reads the client name
  out of the user agent to gate client-specific behaviour, so it is an API
  compatibility identifier, not branding. `name_for_branded_user_agent` is the
  supported way to add our name, and that is what we set.
* Java/Kotlin package names (`com.owncloud.android`, `com.nextcloud.client`).
  They are internal identifiers; renaming them would churn thousands of files
  for no user-visible gain and break the merge path for upstream fixes.
"""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

DOMAIN = "cloud.techyst.net"
APP_ID = "net.techyst.cloud"
REPO = "https://github.com/zeshantech/techyst-cloud-android"

# Resource key -> new value, for app/src/main/res/values/setup.xml
MAIN_SETUP = {
    # identity
    "app_name": "Techyst Cloud",
    "default_display_name_for_root_folder": "Techyst Cloud",
    "name_for_branded_user_agent": "Techyst Cloud",
    "splashScreenBold": "Techyst",
    "splashScreenNormal": "Cloud",

    # Namespaced identifiers. These MUST differ from the official app's, or the
    # two apps collide on the device: same account type, same content provider
    # authorities, same database file.
    "account_type": "techyst",
    "authority": f"{APP_ID}.provider",
    "users_and_groups_search_authority": f"{APP_ID}.providers.UsersAndGroupsSearchProvider",
    "users_and_groups_share_with": f"{APP_ID}.providers.UsersAndGroupsSearchProvider.action.SHARE_WITH",
    "document_provider_authority": f"{APP_ID}.documents",
    "file_provider_authority": f"{APP_ID}.files",
    "image_cache_provider_authority": f"{APP_ID}.imageCache.provider",
    "db_file": "techyst_cloud.db",
    "db_name": "techyst_cloud",
    "data_folder": "techystcloud",
    "login_data_own_scheme": "techystcloud",

    # Single-tenant login: the server is fixed, so the URL field and the
    # "register with a provider" path are both removed from the login screen.
    "show_server_url_input": "false",
    "show_provider_or_own_installation": "false",
    "provider_registration_server": f"https://{DOMAIN}",
    "enforce_servers": f'[{{"name":"Techyst Cloud","url":"https://{DOMAIN}"}}]',

    # Techyst palette: master primary, brand teal for the dark variant, and the
    # family accent. See BRAND.md in the workspace root.
    "primary": "#1E7096",
    "primary_dark": "#195673",
    "color_accent": "#E77129",
    "login_text_color": "#FFFFFF",
    "login_text_hint_color": "#A8CBDD",

    "is_branded_client": "true",
    "is_branded_plus_client": "false",

    # Links. Upstream's help forum and beta channels do not cover this build,
    # so the participate screen is switched off rather than pointed at pages
    # that cannot answer for it.
    "participate_enabled": "false",
    "show_whats_new": "false",
    "help_enabled": "false",
    "url_help": "",
    "privacy_enabled": "true",
    "privacy_url": "https://techyst.net/cloud/privacy",
    "imprint_enabled": "true",
    "url_imprint": "https://techyst.net/cloud/terms",
    "recommend_enabled": "false",
    "url_app_download": f"https://play.google.com/store/apps/details?id={APP_ID}",
    "url_server_install": f"https://{DOMAIN}",
    "mail_logger": "team@techyst.net",

    # GPL: the running binary must point at the corresponding source.
    "sourcecode_enabled": "true",
    "sourcecode_url": REPO,
    "report_issue_link": f"{REPO}/issues/new",
    "report_issue_empty_link": f"{REPO}/issues",
    "contributing_link": f"{REPO}/blob/core/CONTRIBUTING.md",
    "translation_link": REPO,
    "fdroid_link": "",
    "fdroid_beta_link": "",
    "beta_apk_link": "",
    "play_store_register_beta": f"https://play.google.com/apps/testing/{APP_ID}",
    "help_link": "",
}

# app/src/gplay/res/values/setup.xml — our own push proxy, because Nextcloud's
# proxy only serves the official apps' FCM sender ID.
GPLAY_SETUP = {
    "push_server_url": f"https://push.{DOMAIN}",
}

TAGS = ("string", "bool", "color", "integer")


def patch_setup(path: pathlib.Path, values: dict, check: bool) -> list[str]:
    text = original = path.read_text(encoding="utf-8")
    changes = []
    for key, new in values.items():
        hit = False
        for tag in TAGS:
            # Matches <string name="x">old</string> and the self-closing/empty
            # <string name="x"/> form, keeping any extra attributes intact.
            pattern = re.compile(
                rf'(<{tag}\s+name="{re.escape(key)}"((?:\s+[a-zA-Z:]+="[^"]*")*)\s*)(?:/>|>(.*?)</{tag}>)',
                re.DOTALL,
            )
            m = pattern.search(text)
            if not m:
                continue
            hit = True
            old = m.group(3) if m.group(3) is not None else ""
            escaped = new.replace("&", "&amp;").replace("<", "&lt;")
            if old != escaped:
                changes.append(f"{path.name}: {key}: {old!r} -> {escaped!r}")
                text = text[:m.start()] + f"{m.group(1)}>{escaped}</{tag}>" + text[m.end():]
            break
        if not hit:
            changes.append(f"{path.name}: MISSING KEY {key} (upstream changed?)")
    if text != original and not check:
        path.write_text(text, encoding="utf-8")
    return changes


def patch_application_id(check: bool) -> list[str]:
    """Point the shipping flavours at our application id.

    Only `generic` (F-Droid-style, no Google dependency) and `gplay` (Firebase)
    are ours. `versionDev`, `qa` and `huawei` keep upstream ids because we do
    not publish them, and leaving them alone keeps the diff to upstream small.
    """
    path = ROOT / "app" / "build.gradle.kts"
    text = original = path.read_text(encoding="utf-8")
    changes = []

    # defaultConfig
    text, n = re.subn(r'(\n        applicationId = )"com\.nextcloud\.client"',
                      rf'\1"{APP_ID}"', text, count=1)
    if n:
        changes.append(f'build.gradle.kts: defaultConfig applicationId -> {APP_ID}')

    # the two flavours we ship
    for flavour in ("generic", "gplay"):
        pattern = re.compile(
            rf'(register\("{flavour}"\)\s*\{{[^}}]*?applicationId = )"com\.nextcloud\.client"',
            re.DOTALL,
        )
        text, n = pattern.subn(rf'\1"{APP_ID}"', text, count=1)
        if n:
            changes.append(f'build.gradle.kts: flavour {flavour} applicationId -> {APP_ID}')

    if text != original and not check:
        path.write_text(text, encoding="utf-8")
    return changes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    changes = []
    changes += patch_setup(ROOT / "app/src/main/res/values/setup.xml", MAIN_SETUP, args.check)
    changes += patch_setup(ROOT / "app/src/gplay/res/values/setup.xml", GPLAY_SETUP, args.check)
    changes += patch_application_id(args.check)

    missing = [c for c in changes if "MISSING KEY" in c]
    for c in changes:
        print(("would change: " if args.check else "changed: ") + c)
    if not changes:
        print("already branded; nothing to do")
    if missing:
        print(f"\n{len(missing)} resource key(s) not found — upstream layout changed",
              file=sys.stderr)
        return 1
    if args.check and changes:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
