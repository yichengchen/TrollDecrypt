#!/bin/sh
set -eu
cd "$(dirname "$0")"

: "${THEOS:?Set THEOS to your Theos installation (with the iPhoneOS16.5 SDK).}"
make_command=${MAKE:-gmake}
if ! command -v "$make_command" >/dev/null 2>&1; then
    make_command=make
fi

"$make_command" clean FINALPACKAGE=1 ARCHS=arm64 THEOS_PACKAGE_SCHEME=
"$make_command" stage FINALPACKAGE=1 ARCHS=arm64 THEOS_PACKAGE_SCHEME= PACKAGE_TIPA=1
python3 Tests/verify_package.py TrollDecrypt.tipa

mkdir -p dist
cp TrollDecrypt.tipa dist/TrollDecrypt.ipa
cp TrollDecrypt.tipa dist/TrollDecrypt.tipa
(
    cd dist
    shasum -a 256 TrollDecrypt.ipa TrollDecrypt.tipa > SHA256SUMS
)
{
    git log -1 --format='Source: %H'
    if test -n "$(git status --porcelain --untracked-files=no)"; then
        echo 'Source has local modifications.'
    fi
    printf 'Theos: '
    git -C "$THEOS" rev-parse HEAD
    xcodebuild -version
    echo 'Target: arm64, iOS 14.0 minimum, iPhoneOS16.5 SDK'
} > dist/BUILD-INFO.txt
printf '\nTrollStore packages: dist/TrollDecrypt.ipa and dist/TrollDecrypt.tipa\n'
