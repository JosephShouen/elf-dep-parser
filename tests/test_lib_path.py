import unittest
from unittest.mock import MagicMock, mock_open, patch

from elf_dep_parser.parser import resolve_library_path


class TestResolveLibraryPath(unittest.TestCase):
    @patch("os.path.exists", return_value=False)
    @patch("elf_dep_parser.parser.get_ld_config_libs", return_value=None)
    @patch("elf_dep_parser.parser.parse_ld_so_conf", return_value=[])
    def test_library_not_found_anywhere(self, mock_conf, mock_ldconfig, mock_exists):
        result = resolve_library_path("libmissing.so", "/bin/true")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
