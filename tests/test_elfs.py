import os
import unittest
from pathlib import Path
from elf_dep_parser.parser import get_elf_dependencies
import tempfile

# минимальный ELF без зависимостей
MINIMAL_ELF = bytes.fromhex(
    '7f45 4c46 0201 0100 0000 0000 0000 0000'  # e_ident
    '0200 3e00 0100 0000 0000 0000 0000 0000'  # e_type, e_machine
    '4000 0000 0000 0000 0000 0000 0000 0000'  # e_entry, e_phoff
    '0000 0000 0000 0000 4000 3800 0100 0000'  # e_shoff, e_flags
    '0000 0000 0000 0000 0000 0000 0000 0000'  # e_ehsize, e_phentsize
    '0000 0000 0000 0000 0000 0000 0000 0000'  # e_phnum, e_shentsize
    '0000 0000 0000 0000 0000 0000 0000 0000'  # e_shnum, e_shstrndx
)


class TestRealElf(unittest.TestCase):
    def test_real_elf(self):
        test_file = "/bin/true"
        if not os.path.exists(test_file):
            self.skipTest(f"{test_file} не найден в системе")

        deps = get_elf_dependencies(test_file)
        self.assertIn("libc.so.6", " ".join(deps),
                      f"{test_file} должен зависеть от libc")


class TestPureElfNoDeps(unittest.TestCase):
    def test_elf_without_dependencies(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            elf_path = Path(tmpdir) / "pure_elf"

            with open(elf_path, 'wb') as f:
                f.write(MINIMAL_ELF)

            deps = get_elf_dependencies(str(elf_path))
            self.assertEqual(
                deps, [],
                f"Ожидался пустой список зависимостей, получено: {deps}")


if __name__ == "__main__":
    unittest.main()
