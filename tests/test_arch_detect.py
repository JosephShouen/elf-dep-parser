from elf_dep_parser.parser import get_arch_specific_paths
import unittest


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


if __name__ == "__main__":
    unittest.main()
