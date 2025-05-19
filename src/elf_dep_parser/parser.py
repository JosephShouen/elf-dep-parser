import glob
import logging
import os
import subprocess
from functools import lru_cache
from typing import List, Optional

from elftools.elf.dynamic import DynamicSection
from elftools.elf.elffile import ELFFile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_elf_dependencies(elf_path):
    def collect_deps(filename, is_root=True):
        # print("Filename: " + filename)
        if filename in unique_deps:
            return
        unique_deps.add(filename)

        with open(filename, "rb") as f:
            elf = ELFFile(f)
            deps = set()

            for section in elf.iter_sections():
                if isinstance(section, DynamicSection):
                    for tag in section.iter_tags():
                        if tag.entry.d_tag == "DT_NEEDED":
                            deps.add(tag.needed)
            # print("Deps: " + str(deps))
            for dep in deps:
                dep_path = resolve_library_path(dep, filename)
                if dep_path:
                    collect_deps(dep_path, is_root=False)
            if not is_root:
                result.append(os.path.basename(filename))

    unique_deps = set()
    result = []
    collect_deps(elf_path)

    return result


# только распространенные архитектуры
def detect_elf_architecture(elf_path: str) -> str:
    ARCH_MAP = {
        "EM_X86_64": "x86-64",
        "EM_386": "x86",
        "EM_ARM": "arm",
        "EM_AARCH64": "arm64",
    }

    with open(elf_path, "rb") as f:
        elf = ELFFile(f)
        machine = elf.header["e_machine"]
        return ARCH_MAP.get(machine, "unknown")


def get_arch_specific_paths(arch: str) -> List[str]:
    base_paths = {
        "x86-64": [
            "/lib/x86_64-linux-gnu",
            "/usr/lib/x86_64-linux-gnu",
            "/lib64",
            "/usr/lib64",
        ],
        "x86": ["/lib/i386-linux-gnu", "/usr/lib/i386-linux-gnu"],
        "arm": ["/lib/arm-linux-gnueabi", "/usr/lib/arm-linux-gnueabi"],
        "arm64": ["/lib/aarch64-linux-gnu", "/usr/lib/aarch64-linux-gnu"],
        "default": ["/lib", "/usr/lib", "/lib64", "/usr/lib64"],
    }
    return base_paths.get(arch, base_paths["default"])


def get_ld_config_libs() -> Optional[dict]:
    try:
        result = subprocess.run(
            ["ldconfig", "-p"], capture_output=True, text=True, check=True
        )
        libs = {}
        for line in result.stdout.splitlines():
            if "=>" in line:
                name, path = line.split("=>", 1)
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
                    if line.strip() and not line.startswith("#")
                ]
        except OSError as e:
            logger.debug(f"Can't read {filepath}: {e}")
            return []

    paths.extend(read_conf("/etc/ld.so.conf"))

    for config in glob.glob("/etc/ld.so.conf.d/*.conf"):
        paths.extend(read_conf(config))

    return paths


@lru_cache(maxsize=1024)
def resolve_library_path(libname: str, elf_path: str) -> Optional[str]:
    # check arch
    arch = detect_elf_architecture(elf_path)

    # check standard paths
    for path in filter(None, get_arch_specific_paths(arch)):
        full_path = os.path.join(path, libname)
        if os.path.exists(full_path):
            return os.path.realpath(full_path)

    # check ldconfig cache
    ldconfig_libs = get_ld_config_libs()
    if ldconfig_libs and f"{libname} " in ldconfig_libs:
        return ldconfig_libs[f"{libname} "]

    # check ld.so.conf paths
    for path in parse_ld_so_conf():
        full_path = os.path.join(path, libname)
        if os.path.exists(full_path):
            return full_path

    logger.debug(f"Library {libname} not found in any location")
    return None
