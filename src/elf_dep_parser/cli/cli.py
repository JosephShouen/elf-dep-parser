import argparse
import os

from elf_dep_parser.parser import get_elf_dependencies


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("elf_file", help="Путь к анализируемому ELF-файлу")
    args = parser.parse_args()

    if not os.path.exists(args.elf_file):
        print(f"Файл не найден: {args.elf_file}")
        return

    deps = get_elf_dependencies(args.elf_file)
    print("Библиотеки в порядке загрузки:")
    for lib in reversed(deps):
        print(f"- {lib}")


if __name__ == "__main__":
    main()
