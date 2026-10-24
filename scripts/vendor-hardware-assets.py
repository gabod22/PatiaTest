"""Fetch pinned official assets at build time; never invoked by the running monitor."""
import hashlib
import json
from pathlib import Path
import shutil
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def fetch(url, destination, sha256=None):
    if destination.exists() and (sha256 is None or hashlib.sha256(destination.read_bytes()).hexdigest() == sha256):
        return
    request = urllib.request.Request(url, headers={"User-Agent": "PatiaTest-build/1"})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read()
    if sha256 and hashlib.sha256(data).hexdigest() != sha256:
        raise RuntimeError("Asset checksum mismatch: " + url)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)


def main():
    manifest = json.loads((ROOT / "scripts/hardware-dependencies.json").read_text())
    driver = manifest["pawnio"]
    fetch(driver["url"], ROOT / "runtime/setup/PawnIO_setup.exe", driver["sha256"])
    licenses = ROOT / "runtime/licenses"
    licenses.mkdir(parents=True, exist_ok=True)
    for name in ("MPL-2.0", "MIT", "GPL-2.0-only", "LGPL-2.1-only"):
        fetch(f"https://raw.githubusercontent.com/spdx/license-list-data/v3.27.0/text/{name}.txt", licenses / f"{name}.txt")
    fetch("https://raw.githubusercontent.com/LibreHardwareMonitor/LibreHardwareMonitor/3d331e3370efb858411f19511373eff65a218701/THIRD-PARTY-NOTICES.txt",
          licenses / "LibreHardwareMonitor-NOTICES.txt")
    fetch("https://raw.githubusercontent.com/namazso/PawnIO/master/COPYING", licenses / "PawnIO-COPYING.txt")
    fetch("https://raw.githubusercontent.com/namazso/PawnIO/master/README.md", licenses / "PawnIO-README.md")
    fetch("https://raw.githubusercontent.com/amerkoleci/Vortice.Windows/9e609cb9439c9872aa1b339f177e40ec96f77239/LICENSE",
          licenses / "Vortice-LICENSE.txt")
    libraries = {}
    for project in ("PatiaHardwareHost", "PatiaLoadHost"):
        assets_file = ROOT / "native" / project / "obj/project.assets.json"
        if assets_file.exists():
            assets = json.loads(assets_file.read_text())
            libraries.update(assets["libraries"])
            for framework in assets["project"]["frameworks"].values():
                for package in framework.get("downloadDependencies", []):
                    version = package["version"].strip("[]").split(",")[0].strip()
                    path = package["name"].lower() + "/" + version
                    if (ROOT / "build/nuget" / path).is_dir():
                        libraries[package["name"] + "/" + version] = {"type": "package", "path": path}
    notes = ["PatiaTest hardware/load dependencies and runtime packs (unmodified upstream libraries)", "",
             f"PawnIO {driver['version']}: {driver['url']}", "SHA-256: " + driver["sha256"],
             "Driver source and license exception: https://github.com/namazso/PawnIO",
             "Modules source: https://github.com/namazso/PawnIO.Modules", ""]
    for identity, library in sorted(libraries.items()):
        if library["type"] != "package" or identity.startswith("runtime."):
            continue
        package = ROOT / "build/nuget" / library["path"]
        spec = next(package.glob("*.nuspec"))
        metadata = ET.parse(spec).getroot().find("{*}metadata")
        license_node = metadata.find("{*}license")
        license_url = metadata.findtext("{*}licenseUrl", "")
        repository = metadata.find("{*}repository")
        source = metadata.findtext("{*}projectUrl", "")
        if repository is not None:
            source = repository.get("url", source)
            if repository.get("commit"):
                source += "/tree/" + repository.get("commit")
        notes.extend([identity, "Source: " + source, "License: " + ((license_node.text or "") if license_node is not None else license_url), ""])
        copyright_text = metadata.findtext("{*}copyright", "")
        if copyright_text:
            notes.extend([copyright_text, ""])
        target = licenses / identity.replace("/", "-")
        target.mkdir(exist_ok=True)
        shutil.copy2(spec, target / spec.name)
        for file in package.iterdir():
            if file.is_file() and any(word in file.name.lower() for word in ("license", "copying", "notice")):
                shutil.copy2(file, target / file.name)
    (licenses / "DEPENDENCIES.txt").write_text("\n".join(notes), encoding="utf-8")
    shutil.copy2(ROOT / "scripts/hardware-dependencies.json", licenses / "hardware-dependencies.json")
    print("Instalador verificado y licencias preparados en runtime/.")


if __name__ == "__main__":
    main()
