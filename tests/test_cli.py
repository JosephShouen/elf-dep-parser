import unittest
from unittest.mock import patch, MagicMock
import io
import sys
from elf_dep_parser.cli.cli import main


class TestCLIIntegration(unittest.TestCase):
    @patch('elf_dep_parser.cli.cli.get_elf_dependencies')
    def test_cli_main(self, mock_parser):
        mock_parser.return_value = ["libc.so.6"]
        test_args = ["prog", "/bin/true"]
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            original_argv = sys.argv
            sys.argv = test_args
            main()
            output = captured_output.getvalue()
            self.assertIn("libc.so.6", output)
            mock_parser.assert_called_once_with("/bin/true")

        finally:
            sys.argv = original_argv
            sys.stdout = sys.__stdout__


if __name__ == "__main__":
    unittest.main()
