import unittest
from unittest.mock import MagicMock, mock_open, patch

from elf_dep_parser.parser import get_ld_config_libs, parse_ld_so_conf


class TestLdConfig(unittest.TestCase):
    def test_get_ld_config_libs_empty_output(self):
        mock_result = MagicMock()
        mock_result.stdout = ""

        with patch("subprocess.run", return_value=mock_result):
            result = get_ld_config_libs()
            self.assertEqual(result, {})


class TestParseLdSoConf(unittest.TestCase):
    @patch("glob.glob")
    @patch("builtins.open", mock_open(read_data=""))
    def test_empty_configs(self, mock_glob):
        mock_glob.return_value = []

        result = parse_ld_so_conf()
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
