"""Source-contract regression checks for Pandas HideGuildInfo and HidePartyInfo mapflags."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CHECKS = (
    ("guild feature switch", "src/config/pandas.hpp", "#define Pandas_MapFlag_HideGuildInfo"),
    ("party feature switch", "src/config/pandas.hpp", "#define Pandas_MapFlag_HidePartyInfo"),
    ("guild mapflag enum", "src/map/map.hpp", "MF_HIDEGUILDINFO,"),
    ("party mapflag enum", "src/map/map.hpp", "MF_HIDEPARTYINFO,"),
    ("guild script constant", "src/map/script_constants.hpp", "export_constant(MF_HIDEGUILDINFO);"),
    ("party script constant", "src/map/script_constants.hpp", "export_constant(MF_HIDEPARTYINFO);"),
    ("mapflag refresh sends targeted name packets", "src/map/map.cpp", "clif_name(&observer->bl, &target->bl, SELF);"),
    ("mapflag refresh avoids full player reset", "src/map/map.cpp", "A full clif_refresh() also cancels chat, vending and trading states."),
    ("guild name hidden from others", "src/map/clif.cpp", "map_getmapflag(sd->bl.m, MF_HIDEGUILDINFO) && src->id != bl->id"),
    ("guild and position names cleared", "src/map/clif.cpp", 'safestrncpy(packet.guild_name, "", NAME_LENGTH);'),
    ("party name hidden from others", "src/map/clif.cpp", "map_getmapflag(sd->bl.m, MF_HIDEPARTYINFO) && src->id != bl->id"),
    ("party name cleared", "src/map/clif.cpp", 'safestrncpy(packet.party_name, "", NAME_LENGTH);'),
    ("Windows CI step", ".github/workflows/windows-cloud-validation.yml", "test_hide_info_mapflags.py"),
)


def main() -> None:
    failures = []
    for label, relative_path, expected in CHECKS:
        content = (ROOT / relative_path).read_text(encoding="utf-8")
        if expected not in content:
            failures.append(f"{label}: missing {expected!r} in {relative_path}")

    if failures:
        raise SystemExit("\n".join(failures))

    print(f"PASS: {len(CHECKS)} HideInfo mapflag source-contract checks")


if __name__ == "__main__":
    main()
