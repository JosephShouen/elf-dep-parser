from elftools.elf.elffile import ELFFile
from elftools.elf.dynamic import DynamicSection

import os
import subprocess
from functools import lru_cache
# from ctypes.util import find_library

# def get_elf_dependencies(filename):
#     deps = []
#     with open(filename, 'rb') as f:
#         elf = ELFFile(f)
#
#         for section in elf.iter_sections():
#             if isinstance(section, DynamicSection):
#                 for tag in section.iter_tags():
#                     if tag.entry.d_tag == 'DT_NEEDED':
#                         deps.append(tag.needed)
#     return deps

def get_elf_dependencies(elf_path):
    def collect_deps(filename):
        print("Filename: " + filename)
        if filename in unique_deps:
            return
        unique_deps.add(filename)

        with open(filename, 'rb') as f:
            elf = ELFFile(f)
            deps = set()

            for section in elf.iter_sections():
                if isinstance(section, DynamicSection):
                    for tag in section.iter_tags():
                        if tag.entry.d_tag == 'DT_NEEDED':
                            deps.add(tag.needed)

            for dep in deps:
                print(dep)
                dep_path = resolve_library_path(dep, filename)
                if dep_path:
                    collect_deps(dep_path)
            result.append(os.path.basename(filename))

            # for dep in deps:
            #     print(dep)
            #     dep_path = find_library(dep)
            #     print("Dep path: " + str(dep_path))
            #     if dep_path:
            #         collect_deps(dep_path)
            # result.append(os.path.basename(filename))

    unique_deps = set()
    result = []
    collect_deps(elf_path)
    return result


# def resolve_library_path(libname, elf_path):
#     search_paths = [
#         os.path.dirname(elf_path),
#         '/lib',
#         '/usr/lib',
#         '/usr/local/lib',
#         '/lib32',
#         os.path.expanduser('~/.local/lib')
#     ]
#
#     for path in search_paths:
#         full_path = os.path.join(path, libname)
#         print("Full path: " + str(full_path))
#         if os.path.exists(full_path):
#             return full_path
#     return None

@lru_cache(maxsize=1024)
def resolve_library_path(libname, elf_path=None):

    search_paths = [
        *(os.path.dirname(elf_path) if elf_path else []),  # Рядом с ELF
        '/lib', '/lib32', '/lib64',
        '/usr/lib', '/usr/lib32', '/usr/lib64',
        '/usr/local/lib',
        *os.getenv('LD_LIBRARY_PATH', '').split(':')
    ]

    for path in filter(None, search_paths):
        full_path = os.path.join(path, libname)
        print("full_path: " + full_path)
        if os.path.exists(full_path):
            return os.path.realpath(full_path)

    try:
        result = subprocess.run(
            ['ldconfig', '-p'],
            capture_output=True,
            text=True,
            check=True
        )
        for line in result.stdout.splitlines():
            if f"{libname} " in line:
                return line.split('=>')[-1].strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    try:
        with open('/etc/ld.so.conf') as f:
            paths = [line.strip() for line in f if line.strip() and not line.startswith('#')]

        for config in glob.glob('/etc/ld.so.conf.d/*.conf'):
            with open(config) as f:
                paths.extend(line.strip() for line in f if line.strip() and not line.startswith('#'))

        for path in paths:
            full_path = os.path.join(path, libname)
            if os.path.exists(full_path):
                return full_path
    except Exception:
        pass

    return None