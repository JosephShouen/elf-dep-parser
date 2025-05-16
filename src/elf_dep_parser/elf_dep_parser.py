from elftools.elf.elffile import ELFFile
from elftools.elf.dynamic import DynamicSection

def get_elf_dependencies(filename):
    deps = []
    with open(filename, 'rb') as f:
        elf = ELFFile(f)

        for section in elf.iter_sections():
            if isinstance(section, DynamicSection):
                for tag in section.iter_tags():
                    if tag.entry.d_tag == 'DT_NEEDED':
                        deps.append(tag.needed)
    return deps
