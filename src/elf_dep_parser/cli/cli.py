import argparse
import sys

from elf_dep_parser.parser import get_elf_dependencies


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("elf_file", help="Путь к анализируемому ELF-файлу")
    args = parser.parse_args()

    try:
        deps = get_elf_dependencies(args.elf_file)
        if not deps:
            print("Не найдено внешних зависимостей")
            return

        print("Библиотеки в порядке загрузки:")
        for lib in reversed(deps):
            print(f"- {lib}")

    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
