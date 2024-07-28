#!/usr/bin/bash

mkdir -p .work-dir

# Clone the repo
if [ ! -d ".work-dir/QCanvas/" ]; then
  git clone https://github.com/QCanvas/QCanvasApp.git .work-dir/QCanvas
fi

# Move into the repo
cd .work-dir/QCanvas || exit

# Reset the repo, fetch tags and pull
git reset HEAD --hard
git fetch --tags

# Get the tag information
latest_tag=$(git describe --tags "$(git rev-list --tags --max-count=1)")
pypi_version_number="${latest_tag:1}" # Remove the "v" at the start of the tag

# Checkout the tag
git checkout "$latest_tag"

# Export requirements
poetry export --without-hashes -f requirements.txt -o ../requirements.txt  

# Move to root dir
cd ../..

# Re-generate the manifest
req2flatpak --requirements-file .work-dir/requirements.txt --target-platforms 311-x86_64 311-aarch64 --outfile python3-qcanvas.json --requirements qcanvas=="${pypi_version_number}"
pdm run utils/update-meta-repo.py .work-dir/QCanvas qcanvas-desktop-files.json