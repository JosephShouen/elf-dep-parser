"""
Basic usage example for elf_dep_parser
"""

from elf_dep_parser.parser import get_elf_dependencies


def main():
    binary_path = "/bin/ls"

    try:
        print(f"Анализируемый Elf: {binary_path}")
        dependencies = get_elf_dependencies(binary_path)

        print("\nЗависимости от верхнего уровня в нижнему:")
        for i, lib in enumerate(dependencies, 1):
            print(f"{i}. {lib}")

        print(f"\nВсего зависимостей: {len(dependencies)}")

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
