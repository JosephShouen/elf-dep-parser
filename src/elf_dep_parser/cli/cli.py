# from src.elf_dep_parser.parser import get_elf_dependencies
from elf_dep_parser.parser import get_elf_dependencies
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('elf_file', help='Путь к анализируемому ELF-файлу')

    args = parser.parse_args()
    deps = get_elf_dependencies(args.elf_file)
    print("Библиотеки в порядке загрузки:")
    for lib in reversed(deps[:-1]):
        print(f"- {lib}")

if __name__ == "__main__":
    main()
