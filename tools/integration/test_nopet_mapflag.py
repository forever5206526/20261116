#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Source-contract regression checks for the Pandas NoPet mapflag."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig")


def require(label: str, path: str, needle: str) -> None:
    if needle not in read(path):
        raise SystemExit(f"FAIL: {label} ({path})")


checks = [
    ("feature switch", "src/config/pandas.hpp", "#define Pandas_MapFlag_NoPet"),
    ("mapflag enum guarded by feature switch", "src/map/map.hpp",
     "#ifdef Pandas_MapFlag_NoPet\n\tMF_NOPET,\n#endif // Pandas_MapFlag_NoPet"),
    ("script constant export", "src/map/script_constants.hpp",
     "#ifdef Pandas_MapFlag_NoPet\n\texport_constant(MF_NOPET);\n#endif // Pandas_MapFlag_NoPet"),
    ("mapflag handler guarded by feature switch", "src/map/map.cpp",
     "#ifdef Pandas_MapFlag_NoPet\n\t\tcase MF_NOPET:"),
    ("only players on affected map are processed", "src/map/map.cpp",
     "if (!pl_sd || pl_sd->bl.m != m)\n\t\t\t\t\t\tcontinue;"),
    ("active pet is returned to egg", "src/map/map.cpp",
     "pet_return_egg(pl_sd, pl_sd->pd);"),
    ("iterator is released", "src/map/map.cpp", "mapit_free(iter);"),
    ("English message", "conf/msg_conf/map_msg.conf",
     "1546: Pets were returned to eggs because this map does not allow pets."),
    ("Traditional Chinese message", "conf/msg_conf/map_msg_chn.conf",
     "1546: 此地圖禁止使用寵物，已將寵物退回寵物蛋。"),
]

for label, path, needle in checks:
    require(label, path, needle)

print(f"PASS: {len(checks)} NoPet source-contract checks")
