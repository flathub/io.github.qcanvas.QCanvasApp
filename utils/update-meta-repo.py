# Updates the commit hash for the resources repo in the manifest to the current one

# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "gitpython",
# ]
# ///

import sys
from pathlib import Path

from git import Repo
import json

try:
    repository_path = Path(sys.argv[1])
    manifest_file = Path(sys.argv[2])
except IndexError:
    print(
        "Missing file name/path: expected <repo path> <manifest file>", file=sys.stderr
    )
    exit(1)

repo = Repo(repository_path)
latest_hash = repo.rev_parse("HEAD").hexsha

def update_commit_hash() -> None:
    with open(manifest_file, "r") as f:
        manifest = json.load(f)

    manifest["sources"][0]["commit"] = latest_hash

    with open(manifest_file, "w") as f:
        json.dump(manifest, f, indent=4)


if __name__ == "__main__":
    update_commit_hash()
