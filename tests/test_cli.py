import io
import sys
import unittest
from unittest.mock import patch

from elf_dep_parser.cli.cli import main


class TestCLIIntegration(unittest.TestCase):
    @patch("elf_dep_parser.cli.cli.get_elf_dependencies")
    def test_success_cli(self, mock_parser):
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

    @patch("elf_dep_parser.cli.cli.get_elf_dependencies")
    def test_cli_invalid_elf(self, mock_parser):
        mock_parser.side_effect = ValueError("Not an ELF file")
        test_args = ["prog", "/not/an/elf"]

        with patch("sys.argv", test_args), patch(
            "sys.stderr", new_callable=io.StringIO
        ) as mock_stderr:
            with self.assertRaises(SystemExit) as cm:
                main()

            self.assertEqual(cm.exception.code, 1)
            error_output = mock_stderr.getvalue()
            self.assertIn("Not an ELF file", error_output)
            mock_parser.assert_called_once()


if __name__ == "__main__":
    unittest.main()
