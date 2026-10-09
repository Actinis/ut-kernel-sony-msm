#!/usr/bin/env python3
"""Compile the actual kernel key-index validator and check all capability cases."""
import argparse
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('kernel', type=Path)
args = parser.parse_args()
source = (args.kernel/'net/wireless/util.c').read_text()
start = source.index('bool cfg80211_valid_key_idx(')
end = source.index('\nint cfg80211_validate_key_settings', start)
function = source[start:end]
prelude = '''#include <stdbool.h>
#include <stdio.h>
struct wiphy { bool beacon; };
struct cfg80211_registered_device { struct wiphy wiphy; bool igtk; };
#define NL80211_EXT_FEATURE_BEACON_PROTECTION 1
static bool cfg80211_igtk_cipher_supported(struct cfg80211_registered_device *r) { return r->igtk; }
static bool wiphy_ext_feature_isset(struct wiphy *w, int f) { return w->beacon; }
'''
main = '''
int main(void) {
  int count = 0;
  for (int pair = 0; pair < 2; pair++)
    for (int igtk = 0; igtk < 2; igtk++)
      for (int beacon = 0; beacon < 2; beacon++) {
        struct cfg80211_registered_device r = {{beacon}, igtk};
        int limit = pair ? 3 : beacon ? 7 : igtk ? 5 : 3;
        for (int idx = -1; idx <= 8; idx++) {
          bool actual = cfg80211_valid_key_idx(&r, idx, pair);
          if (actual != (idx >= 0 && idx <= limit)) {
            fprintf(stderr, "pair=%d igtk=%d beacon=%d idx=%d: wrong acceptance\\n", pair, igtk, beacon, idx);
            return 1;
          }
          count++;
        }
      }
  printf("%d actual kernel validator cases passed\\n", count);
  return 0;
}
'''
with tempfile.TemporaryDirectory() as directory:
    path = Path(directory)
    (path/'test.c').write_text(prelude+function+main)
    subprocess.run(['cc','-Wall','-Werror',str(path/'test.c'),'-o',str(path/'test')], check=True)
    subprocess.run([str(path/'test')], check=True)
