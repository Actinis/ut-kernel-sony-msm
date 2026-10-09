# Source provenance and build contract

The buildable Noble adaptation and repository infrastructure are on `main`.
The upstream baseline is on `upstream/sony-halium-11`. Sony/mer-hybris upstream
base, AppArmor donor and submodule inputs are pinned in `UPSTREAM.json`.
Upstream authorship and file licences are retained.

AppArmor consists of the donor subtree and a Linux 4.19 inode API adaptation.
Original code authors retain attribution in their source files; the import
committer does not claim authorship of that subtree.

The kernel has nine gitlink inputs, including WLAN, Sony techpacks and
WireGuard. Initialize them at the recorded commits, not their branch tips.

Only Ubuntu Touch 24.04 Noble is supported. The device build consumes this
committed tree directly; no backport or hidden modification is applied before
compilation. See the device repository for build and qualification instructions.
