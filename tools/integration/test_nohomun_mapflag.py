#!/usr/bin/env python3
"""Static regression checks for the NoHomun mapflag integration."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")

checks = {
    "mapflag enum": ("src/map/map.hpp", "MF_NOHOMUN,"),
    "script constant export": ("src/map/script_constants.hpp", "export_constant(MF_NOHOMUN);"),
    "mapflag activation handler": ("src/map/map.cpp", "case MF_NOHOMUN:"),
    "active homunculus is rested": ("src/map/map.cpp", "hom_vaporize(pl_sd, HOM_ST_REST);"),
    "summoning is blocked": ("src/map/homunculus.cpp", "map_getmapflag(sd->bl.m, MF_NOHOMUN)"),
    "summoning message": ("src/map/homunculus.cpp", "msg_txt(sd, 1545)"),
    "activation message": ("src/map/map.cpp", "msg_txt(pl_sd, 1544)"),
    "English message": ("conf/msg_conf/map_msg.conf", "1545: You cannot summon a homunculus on this map."),
    "Traditional Chinese message": ("conf/msg_conf/map_msg_chn.conf", "1545: 此地圖禁止召喚人工生命體。"),
}
for label, (path, needle) in checks.items():
    if needle not in read(path):
        raise SystemExit(f"FAIL: {label} ({path})")
print(f"PASS: {len(checks)} NoHomun integration checks")
