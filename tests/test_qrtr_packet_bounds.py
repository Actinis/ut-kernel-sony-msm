"""Exercise the actual QRTR packet-size predicate with native C semantics.

This is a bounds regression check, not an end-to-end transport test.
"""
import pathlib
import re
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROGRAM = r"""
#include <stdint.h>
#include <stddef.h>
#define ALIGN(x, a) (((x) + ((a) - 1)) & ~((a) - 1))
int main(void)
{
    for (size_t hdrlen = 16; hdrlen <= 32; hdrlen += 16) {
        for (uint32_t size = 1; size <= 4096; size++) {
            size_t len = hdrlen + ((size + 3) / 4) * 4;
            if (PREDICATE) return 1; /* valid payload and alignment */
            len--;
            if (!(PREDICATE)) return 2; /* truncated packet */
            len += 2;
            if (!(PREDICATE)) return 3; /* trailing bytes */
            len = size - 1;
            if (!(PREDICATE)) return 4; /* payload exceeds packet */
        }
    }
    uint32_t size = 0;
    size_t len = 32, hdrlen = 32;
    if (!(PREDICATE)) return 5; /* empty payload */
    return 0;
}
"""


class PacketBounds(unittest.TestCase):
    def predicate(self):
        source = (ROOT / "net/qrtr/qrtr.c").read_text()
        function = source.split("int qrtr_endpoint_post(", 1)[1]
        match = re.search(r"if \((!size \|\| size > len[^\n]+)\)", function)
        self.assertIsNotNone(match, "QRTR size guard was not found")
        return match.group(1)

    def run_predicate(self, predicate):
        with tempfile.TemporaryDirectory() as directory:
            source = pathlib.Path(directory) / "bounds.c"
            binary = pathlib.Path(directory) / "bounds"
            source.write_text(PROGRAM.replace("PREDICATE", predicate))
            subprocess.run(["cc", "-Wall", "-Wextra", str(source), "-o", str(binary)],
                           check=True, capture_output=True)
            return subprocess.run([str(binary)], check=False).returncode

    def test_valid_and_malformed_lengths(self):
        self.assertEqual(self.run_predicate(self.predicate()), 0)

    def test_regression_check_detects_the_chained_comparison(self):
        self.assertNotEqual(self.run_predicate(
            "!size || size > len != ALIGN(size, 4) + hdrlen"), 0)


if __name__ == "__main__":
    unittest.main()
