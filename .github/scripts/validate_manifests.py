#!/usr/bin/env python3
"""Validate Scoop manifests against the upstream Scoop JSON schema.

Usage:
    validate_manifests.py [manifest ...]

With no arguments every ``bucket/*.json`` relative to the repository root is
validated. Exits non-zero if any manifest fails to parse or validate.
"""

import argparse
import glob
import json
import os
import sys
import urllib.request

from jsonschema import ValidationError, validate

SCHEMA_URL = "https://raw.githubusercontent.com/ScoopInstaller/Scoop/master/schema.json"
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_schema(url):
    with urllib.request.urlopen(url, timeout=60) as response:
        return json.loads(response.read().decode())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifests", nargs="*", help="manifest paths (default: bucket/*.json)")
    parser.add_argument("--schema-url", default=SCHEMA_URL, help="Scoop schema URL")
    args = parser.parse_args()

    manifests = args.manifests or sorted(glob.glob(os.path.join(REPO_ROOT, "bucket", "*.json")))
    if not manifests:
        print("No manifests found in bucket/")
        return 1

    try:
        schema = load_schema(args.schema_url)
    except Exception as e:  # network, HTTP status, malformed JSON
        print(f"Failed to fetch Scoop schema from {args.schema_url}: {e}")
        return 1

    failed = False
    for manifest_path in manifests:
        rel = os.path.relpath(manifest_path, REPO_ROOT)
        print(f"Validating {rel}...")
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)
            validate(instance=manifest, schema=schema)
            print(f"  {rel} is valid.")
        except json.JSONDecodeError as e:
            print(f"  Error parsing JSON: {e}")
            failed = True
        except ValidationError as e:
            print(f"  Schema validation error in {rel}: {e.message}")
            failed = True
        except Exception as e:
            print(f"  Unexpected error in {rel}: {e}")
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
