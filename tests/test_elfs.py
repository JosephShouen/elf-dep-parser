"""Тест функции get_elf_dependencies"""

import os
import tempfile
import unittest
from pathlib import Path

from elf_dep_parser.parser import get_elf_dependencies

# минимальный ELF без зависимостей
minimal_elf = bytes.fromhex(
    "7f45 4c46 0201 0100 0000 0000 0000 0000"  # e_ident
    "0200 3e00 0100 0000 0000 0000 0000 0000"  # e_type, e_machine
    "4000 0000 0000 0000 0000 0000 0000 0000"  # e_entry, e_phoff
    "0000 0000 0000 0000 4000 3800 0100 0000"  # e_shoff, e_flags
    "0000 0000 0000 0000 0000 0000 0000 0000"  # e_ehsize, e_phentsize
    "0000 0000 0000 0000 0000 0000 0000 0000"  # e_phnum, e_shentsize
    "0000 0000 0000 0000 0000 0000 0000 0000"  # e_shnum, e_shstrndx
)


class TestRealElf(unittest.TestCase):
    def test_real_elf(self):
        """
        Тест для Elf файла /bin/true
        Проверяет порядок зависимостей
        Для /bin/true это должен быть libc.so.6 и ld-linux*
        ld-linux можно различаться для разных архитектур,
        поэтому проверяется отдельно
        """
        test_file = "/bin/true"
        true_deps_count = 2
        if not os.path.exists(test_file):
            self.skipTest(f"{test_file} не найден в системе")

        deps = get_elf_dependencies(test_file)
        self.assertEqual(
            deps[0],
            "libc.so.6",
            f"Первая зависимость {test_file} должна быть libc.so.6",
        )
        self.assertTrue(
            deps[1].startswith("ld-linux"),
            f"Вторая зависимость {test_file} должна быть ld-linux* (получено: {deps[1]})",
        )
        self.assertEqual(
            len(deps),
            true_deps_count,
            f"Ожидаемое количество зависимостей: {true_deps_count} (получено: {len(deps)})",
        )


class TestPureElfNoDeps(unittest.TestCase):
    def test_elf_without_dependencies(self):
        """Тест для самописного Elf файла без зависимостей"""
        with tempfile.TemporaryDirectory() as tmpdir:
            elf_path = Path(tmpdir) / "pure_elf"

            with open(elf_path, "wb") as f:
                f.write(minimal_elf)

            deps = get_elf_dependencies(str(elf_path))
            self.assertEqual(
                deps, [], f"Ожидался пустой список зависимостей, получено: {deps}"
            )


if __name__ == "__main__":
    unittest.main()
