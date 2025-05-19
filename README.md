# ELF Dependency Parser

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Утилита для анализа зависимостей ELF-файлов. Разработана в рамках тестового задания.

## Особенности

- Определяет все динамические зависимости ELF-файла
- Автоматически разрешает пути к библиотекам
- Поддерживает мультиархитектурные системы (x86-64, ARM, etc.)
- Кэширование результатов для ускорения работы

## Установка 

```bash
git clone https://github.com/JosephShouen/elf-dep-parser.git
cd elf-dep-parser
pip install -e .
```

## CLI
```bash
elf_dep_parser /path/to/elf
```

## Библиотека
```python
from elf_dep_parser.parser import get_elf_dependencies

deps = get_elf_dependencies("/path/to/elf")
print(f"Dependencies: {deps}")
```

## Пример вывода

```console
Найдены зависимости:
- libc.so.6
- libpthread.so.0
- libdl.so.2
```
