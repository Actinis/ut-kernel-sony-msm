# Source provenance and build contract

Sony/mer-hybris upstream base and AppArmor donor are pinned in UPSTREAM.json.
All original upstream commits and file licences are retained. The repository
infrastructure history is merged as a second parent; main is not replaced.
AppArmor is a verbatim donor-subtree import plus a separately reviewable inode
API adaptation. Original code authors retain attribution in their source files;
the import committer does not claim authorship of that subtree.

The kernel has nine gitlink inputs, including WLAN, Sony techpacks and
WireGuard. Initialize them at the recorded commits, not their branch tips.
Local duplicate WireGuard Kconfig/Makefile entries and an absolute symlink are
not source changes required by this port; the upstream relative link is retained.

Only Noble is supported. The device build consumes this committed tree directly;
there is no apply-backport script or hidden modification before compilation.
