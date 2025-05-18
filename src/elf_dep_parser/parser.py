from elftools.elf.elffile import ELFFile
from elftools.elf.dynamic import DynamicSection

import os
import subprocess
from functools import lru_cache
import logging
from typing import Optional, List
import glob

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            print("Deps: " + str(deps))
            for dep in deps:
                dep_path = resolve_library_path(dep, filename)
                if dep_path:
                    collect_deps(dep_path)
            result.append(os.path.basename(filename))

    unique_deps = set()
    result = []
    collect_deps(elf_path)
    return result


def get_standard_search_paths(elf_path: Optional[str] = None) -> List[str]:
    return [
        *(os.path.dirname(elf_path) if elf_path else []),
        '/lib/x86_64-linux-gnu', '/usr/lib/x86_64-linux-gnu',
        '/lib64', '/usr/lib64',
        '/lib', '/usr/lib',
        '/lib/i386-linux-gnu', '/usr/lib/i386-linux-gnu',
        *os.getenv('LD_LIBRARY_PATH', '').split(':')
    ]

def get_ld_config_libs() -> Optional[dict]:
    try:
        result = subprocess.run(
            ['ldconfig', '-p'],
            capture_output=True,
            text=True,
            check=True
        )
        libs = {}
        for line in result.stdout.splitlines():
            if '=>' in line:
                name, path = line.split('=>', 1)
                libs[name.strip()] = path.strip()
        return libs
    except (subprocess.SubprocessError, FileNotFoundError) as e:
        logger.debug(f"Failed to run ldconfig: {e}")
        return None


def parse_ld_so_conf() -> List[str]:
    paths = []

    def read_conf(filepath: str):
        try:
            with open(filepath) as f:
                return [
                    line.strip()
                    for line in f
                    if line.strip() and not line.startswith('#')
                ]
        except OSError as e:
            logger.debug(f"Can't read {filepath}: {e}")
            return []

    paths.extend(read_conf('/etc/ld.so.conf'))

    for config in glob.glob('/etc/ld.so.conf.d/*.conf'):
        paths.extend(read_conf(config))

    return paths


@lru_cache(maxsize=1024)
def resolve_library_path(libname: str, elf_path: Optional[str] = None) -> Optional[str]:
    # Check standard paths
    for path in filter(None, get_standard_search_paths(elf_path)):
        full_path = os.path.join(path, libname)
        if os.path.exists(full_path):
            return os.path.realpath(full_path)

    # Check ldconfig cache
    ldconfig_libs = get_ld_config_libs()
    if ldconfig_libs and f"{libname} " in ldconfig_libs:
        return ldconfig_libs[f"{libname} "]

    # Check ld.so.conf paths
    for path in parse_ld_so_conf():
        full_path = os.path.join(path, libname)
        if os.path.exists(full_path):
            return full_path

    logger.debug(f"Library {libname} not found in any location")
    return None