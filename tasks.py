# Needs invoke installed
# See https://www.pyinvoke.org/installing.html
# Usage: invoke <task> [<task2>]

from invoke import task
from pathlib import Path
import shutil

@task
def clean(c):
    for directory in ["repo", ".flatpak-builder", "builddir"]:
        shutil.rmtree(directory, ignore_errors=True)

@task
def build(c):
    c.run(f"""flatpak run org.flatpak.Builder --force-clean --sandbox --user --install --install-deps-from=flathub --ccache --mirror-screenshots-url=https://dl.flathub.org/media/ --repo=repo builddir io.github.qcanvas.QCanvasApp.yaml""")

@task
def run(c):
    c.run("flatpak run io.github.qcanvas.QCanvasApp")

@task
def lint(c):
    base_command = "flatpak run --command=flatpak-builder-lint org.flatpak.Builder" 

    c.run(f"{base_command} manifest io.github.qcanvas.QCanvasApp.yaml")
    c.run(f"{base_command} repo repo")