"""Source-contract regression checks for the Pandas NoMerc mapflag."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CHECKS = (
    ("feature switch", "src/config/pandas.hpp", "#define Pandas_MapFlag_NoMerc"),
    ("mapflag enum", "src/map/map.hpp", "MF_NOMERC,"),
    ("script constant export", "src/map/script_constants.hpp", "export_constant(MF_NOMERC);"),
    ("mapflag activation handler", "src/map/map.cpp", "case MF_NOMERC:"),
    ("existing mercenary is hidden", "src/map/map.cpp", "unit_remove_map(&pl_sd->md->bl, CLR_OUTSIGHT);"),
    ("activation notice", "src/map/map.cpp", "msg_txt(pl_sd, 1547)"),
    ("new mercenary is blocked", "src/map/mercenary.cpp", "map_getmapflag(sd->bl.m, MF_NOMERC)"),
    ("summon denial notice", "src/map/mercenary.cpp", "msg_txt(sd, 1548)"),
    ("Traditional Chinese main message", "conf/msg_conf/map_msg.conf", "1548: 此地圖禁止召喚傭兵。"),
    ("Traditional Chinese message", "conf/msg_conf/map_msg_chn.conf", "1548: 此地圖禁止召喚傭兵。"),
    ("Windows CI step", ".github/workflows/windows-cloud-validation.yml", "test_nomerc_mapflag.py"),
)


def main() -> None:
    failures = []
    for label, relative_path, expected in CHECKS:
        content = (ROOT / relative_path).read_text(encoding="utf-8")
        if expected not in content:
            failures.append(f"{label}: missing {expected!r} in {relative_path}")

    if failures:
        raise SystemExit("\n".join(failures))

    print(f"PASS: {len(CHECKS)} NoMerc source-contract checks")


if __name__ == "__main__":
    main()
