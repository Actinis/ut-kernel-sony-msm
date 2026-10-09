#!/usr/bin/env python3
import json
from pathlib import Path
import subprocess
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'docs/UPSTREAM.json').read_text())
assert len(data['base'])==40
for path, source in data['submodules'].items():
    assert len(source['commit'])==40 and source['url'].startswith('https://')
assert 'aafs_destroy_inode' in (root/'security/apparmor/apparmorfs.c').read_text()
assert (root/'security/apparmor/af_unix.c').is_file()
subprocess.run(['python3',str(root/'ci/test_cfg80211_pmf.py'),str(root)],check=True)
print('Kernel source metadata and PMF matrix passed; no kernel build performed')
