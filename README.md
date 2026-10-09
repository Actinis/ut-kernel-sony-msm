# Sony MSM kernel for Ubuntu Touch Noble

Experimental Actinis community source for Sony Xperia 10 III `pdx213` / `lena`,
Halium 11, **Ubuntu Touch 24.04 Noble**. XQ-BT52 is the prototype target.

**Buildable source:** [pdx213-halium11-noble](https://github.com/Actinis/ut-kernel-sony-msm/tree/pdx213-halium11-noble).
This default main branch preserves repository infrastructure; kernel sources and
full Sony/mer-hybris upstream history are on the linked hardware branch.

The source branch has in-tree AppArmor Unix peer mediation, the Linux 4.19 inode
API adaptation, Noble config and PMF/IGTK validation repair. Do not reapply
backports at build time. Original upstream authorship and licences are retained.
[Provenance](https://github.com/Actinis/ut-kernel-sony-msm/blob/pdx213-halium11-noble/docs/UPSTREAM.json)
records exact base, donor and submodule commits.

The [device repository](https://github.com/Actinis/ut-device-sony-pdx213) pins the
kernel by full commit and owns the real kernel/boot build workflow and hardware
matrix. Build success is not phone qualification. No image release, tag or OTA
is published by this source import; other device variants remain unqualified.
