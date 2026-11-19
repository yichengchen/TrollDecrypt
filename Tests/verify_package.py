#!/usr/bin/env python3
"""Check the actual TrollStore archive, including its runtime library paths."""
import plistlib
import stat
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


def output(*command):
    return subprocess.check_output(command, text=True)


def verify(archive):
    with zipfile.ZipFile(archive) as package:
        assert package.testzip() is None, "Corrupt ZIP entry"
        names = package.namelist()
        assert names and all(name.startswith("Payload/") for name in names)
        root = "Payload/TrollDecrypt.app/"
        info = plistlib.loads(package.read(root + "Info.plist"))
        assert info["CFBundleIdentifier"] == "com.fiore.trolldecrypt"
        assert info["MinimumOSVersion"] == "14.0"
        assert root + "Assets.car" in names
        assert not any("Assets.xcassets/" in name or ".dSYM/" in name for name in names)
        binaries = ["TrollDecrypt", "Frameworks/SSZipArchive.framework/SSZipArchive"]
        for binary in binaries:
            assert stat.S_IMODE(package.getinfo(root + binary).external_attr >> 16) & 0o111
        with tempfile.TemporaryDirectory(prefix="trolldecrypt-verify-") as temporary:
            package.extractall(temporary)
            app = Path(temporary) / root
            for binary in binaries:
                path = str(app / binary)
                assert output("lipo", "-archs", path).strip() == "arm64"
                dependencies = output("otool", "-L", path)
                assert "@rpath/SSZipArchive.framework/SSZipArchive" in dependencies, dependencies
                assert "\t/Library/" not in dependencies and "/var/jb/" not in dependencies
                commands = output("otool", "-l", path)
                assert "LC_CODE_SIGNATURE" in commands
                assert "minos 14.0" in commands
            assert "@executable_path/Frameworks" in output("otool", "-l", str(app / "TrollDecrypt"))
            entitlements = plistlib.loads(output("ldid", "-e", str(app / "TrollDecrypt")).encode())
            source = Path(__file__).resolve().parent.parent / "TrollDecrypt.entitlements"
            assert entitlements == plistlib.loads(source.read_bytes())
            property_lists = list(app.rglob("*.plist")) + list(app.glob("*.lproj/Localizable.strings"))
            subprocess.run(["plutil", "-lint", *map(str, property_lists)], check=True, stdout=subprocess.DEVNULL)
    print("TrollStore archive, arm64/iOS 14 target, bundled framework, assets, plists and entitlements: PASS")


if __name__ == "__main__":
    verify(sys.argv[1])
