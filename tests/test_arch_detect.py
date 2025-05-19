import unittest
from unittest.mock import mock_open, patch

from elftools.elf.elffile import ELFError

from elf_dep_parser.parser import (detect_elf_architecture,
                                   get_arch_specific_paths)


class TestArchPaths(unittest.TestCase):
    def test_x86_64_paths(self):
        paths = get_arch_specific_paths("x86-64")
        self.assertIn("/lib/x86_64-linux-gnu", paths)
        self.assertIn("/lib64", paths)

    def test_unknown_arch(self):
        paths = get_arch_specific_paths("unknown_arch")
        self.assertEqual(paths, ["/lib", "/usr/lib", "/lib64", "/usr/lib64"])

    def test_arm64_paths(self):
        paths = get_arch_specific_paths("arm64")
        self.assertIn("/lib/aarch64-linux-gnu", paths)

    def test_detect_elf_architecture_invalid_file(self):
        with patch("builtins.open", mock_open(read_data=b"NOT_ELF")):
            with self.assertRaises(ELFError):
                detect_elf_architecture("invalid_path")


if __name__ == "__main__":
    unittest.main()
