# ELF Dependency Parser

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Утилита для анализа зависимостей ELF-файлов. Разработана в рамках тестового задания.

## Особенности

- Определяет все динамические зависимости ELF-файла
- Автоматически разрешает пути к библиотекам
- Зависимости формируются в порядке от зависящего к зависимости
- Поддерживает мультиархитектурные системы (x86-64, ARM, etc.)
- Кэширование результатов для ускорения работы

## Ограничения

- Поддерживаются только ELF-файлы Linux
- Не анализирует статические зависимости
- Требует Python 3.8+

## Установка 

```bash
git clone https://github.com/JosephShouen/elf-dep-parser.git
cd elf-dep-parser
pip install .
```

## CLI
```bash
elf_dep_parser /path/to/elf
```

## Пример вывода CLI

```console
Найдены зависимости:
- libc.so.6
- libpthread.so.0
- libdl.so.2
```

## Библиотека

```python
from elf_dep_parser.parser import get_elf_dependencies

deps = get_elf_dependencies("/path/to/elf")
print(f"Dependencies: {deps}")
```

## Пример использования

Готовый минимальный пример расположен в example/lib_usage.py. Запуск:  
```bash
python3 example/lib_usage.py
```

## Вывод

```console
Анализируемый Elf: /bin/ls

Зависимости от верхнего уровня в нижнему:
1. libselinux.so.1
2. libpcre2-8.so.0.11.2
3. libc.so.6
4. ld-linux-x86-64.so.2

Всего зависимостей: 4

```
