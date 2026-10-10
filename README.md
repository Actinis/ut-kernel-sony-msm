# Sony MSM kernel for Ubuntu Touch Noble

Experimental Actinis community kernel for Sony Xperia 10 III `pdx213`/`lena`,
Halium 11 and **Ubuntu Touch 24.04 Noble**. XQ-BT52 is the prototype variant;
other models and firmware revisions are not qualified.

The `main` branch contains the buildable kernel source and repository
infrastructure. `upstream/sony-halium-11` provides the upstream baseline for
comparison. Full Sony/mer-hybris upstream history, authorship and licences
are preserved. `docs/UPSTREAM.json` records the exact upstream base, AppArmor
source and submodule pins. No blanket relicensing is applied.

AppArmor Unix peer mediation and the Linux 4.19 inode API adaptation are in-tree.
The cfg80211 PMF/IGTK key-index repair is also in-tree. **Do not reapply any
backport during a build.** Merge `arch/arm64/configs/pdx213_noble.config` over
`aosp_lena_pdx213_defconfig`, then build with NDK r23b and a separate `O=` directory.

The [device repository](https://github.com/Actinis/ut-device-sony-pdx213) pins
this branch by commit and provides the reproducible kernel/boot entry point.
`python3 ci/test_cfg80211_pmf.py .` checks 80 actual-function capability cases.
Build success is separate from device qualification; no phone is flashed by CI.
No release tag, public image release or OTA channel is created here.

## Security backports

`main` imports applicable Linux 4.19.325-cip136 changes
without claiming an unmodified CIP release. The 4.19.248 version is retained
with an explicit backport-candidate suffix. Existing Actinis AppArmor, PMF and
pdx213 double-tap wake adaptations remain in-tree. The Noble config enables
ARM64 KPTI support. The inherited Sony `__kpti_forced = -1` default
forces KPTI off unless explicitly overridden; removing `kpti=0` from boot
metadata does not establish automatic CPU-based selection.

`docs/security-manual-resolutions.json` records vendor adaptations and
`docs/security-remaining-scope.json` records exclusions. NCM's upstream OS
descriptor/allocation refactor is excluded to preserve Android configfs/uevent
ownership. This is not an exhaustive CVE assessment or an independent audit of
all later Android/Qualcomm/Sony driver fixes. On XQ-BT52, a clean build
with the early boot RNG API adaptation and SDHCI host-lock fix booted both
a RAM-only recovery and the installed Ubuntu Touch system. USB SSH, LightDM,
oFono and the Android HAL container started. The installed-system test then
stalled at the Ubuntu Touch loading screen, lost USB/Wi-Fi connectivity and
rebooted without a host command. The working boot and DTBO were restored.
RAM boot is confirmed; the candidate remains unqualified for installation
until this later failure and complete hardware/suspend testing are resolved.

Audio and WireGuard compatibility commits are published in Actinis forks and
pinned by exact commit in `.gitmodules` and `docs/UPSTREAM.json`. Upstream
history and licences are preserved; no submodule is flattened.

Run `python3 ci/check_repository.py` for the 80 PMF and 25 RNDIS host cases.
Build normally using `pdx213_noble.config`; no patch is applied during a build.
