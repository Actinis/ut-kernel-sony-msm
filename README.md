# Sony MSM kernel for Ubuntu Touch Noble

Experimental Actinis community kernel for Sony Xperia 10 III `pdx213`/`lena`,
Halium 11 and **Ubuntu Touch 24.04 Noble**. XQ-BT52 is the prototype variant;
other models and firmware revisions are not qualified.

The buildable source branch is `pdx213-halium11-noble`; `main` retains repository
infrastructure. Full Sony/mer-hybris upstream history, authorship and licences
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
