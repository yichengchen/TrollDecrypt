# Upstream PR integration

Upstream: https://github.com/donato-fiore/TrollDecrypt

Base: `c4bd8c1` (upstream `main`, checked 2026-11-19).

| PR | Result |
| --- | --- |
| [#16](https://github.com/donato-fiore/TrollDecrypt/pull/16) Quality of life changes | Excluded at the user's request. No directory reorganization or URL scheme was imported. |
| [#17](https://github.com/donato-fiore/TrollDecrypt/pull/17) Clang build fixes (closed, unmerged) | Merged with the deletion of the obsolete `TDDumpDecrypted.m` retained. Current `MemoryUtilities` already uses typed 64-bit addresses, avoiding the old pointer/integer and ASLR-width errors. |
| [#29](https://github.com/donato-fiore/TrollDecrypt/pull/29) App bundle only output | Integrated; search, row selection, deletion and counts now use filtered arrays for all three output sections. Existing sharing remains available. |
| [#33](https://github.com/donato-fiore/TrollDecrypt/pull/33) iOS 26 image lookup | Integrated; keeps dyld lookup, VM-region fallback and boundary-tolerant memory reads. |
| [#34](https://github.com/donato-fiore/TrollDecrypt/pull/34) Newer-iOS executable support | Integrated into all three output modes. Uses suspended helpers, transactional binary replacement, remaining-encryption checks and process/work-directory cleanup. |
| [#35](https://github.com/donato-fiore/TrollDecrypt/pull/35) Framework path matching | Integrated into both dyld and VM lookup; normalizes `/private/` on both paths without modifying the input buffers. |

The framework install name is also set to `@rpath/SSZipArchive.framework/SSZipArchive`
so TrollStore loads the copy inside the app's `Frameworks` directory.

Validation: `sh Tests/run.sh`, release arm64 compilation and package inspection
(Payload structure, embedded framework dependency, minimum OS, property lists,
entitlements and archive integrity). Actual FairPlay decryption still requires
testing on a supported physical device with TrollStore and an installed app.
