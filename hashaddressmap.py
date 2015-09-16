import re


_hash_re = re.compile(r"(.*)[#](.*)(@.*)")


def hash_address_map(addr):
    m = _hash_re.match(addr)
    if m is not None:
        g = m.groups()
        return g[0] + g[2]
    else:
        return addr
