# import elf_dep_parser.elf_dep_parser as parser
from elf_dep_parser.parser import get_elf_dependencies

def main():
    print("Hello Parser")
    deps = get_elf_dependencies('/bin/ls')
    print("Зависимости:", deps)

if __name__ == "__main__":
    main()