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
pip install elf_dep_parser
```

## Использование

```bash
elf_dep_parser /path/to/your/executable
```

## Пример вывода

```console
Найдены зависимости:
- libc.so.6
- libpthread.so.0
- libdl.so.2
```