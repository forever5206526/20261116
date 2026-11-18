"""Source-contract regression checks for the Pandas MobInfo mapflag."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CHECKS = (
    ("MobInfo feature switch", "src/config/pandas.hpp", "#define Pandas_MapFlag_MobInfo"),
    ("parameter framework switch", "src/config/pandas.hpp", "#define Pandas_Mapflags"),
    ("MobInfo mapflag enum", "src/map/map.hpp", "MF_MOBINFO,"),
    ("MobInfo script constant", "src/map/script_constants.hpp", "export_constant(MF_MOBINFO);"),
    ("per-map parameter storage", "src/map/map.hpp", "std::unordered_map<e_mapflag, std::vector<int32>> mapflag_values;"),
    ("parameter validation API", "src/map/map.hpp", "bool map_mapflag_valid_index(e_mapflag mapflag, size_t index);"),
    ("parameter getter API", "src/map/map.hpp", "int32 map_getmapflag_param(int16 m, enum e_mapflag mapflag, size_t index);"),
    ("parameter setter API", "src/map/map.hpp", "void map_setmapflag_param(int16 m, enum e_mapflag mapflag, size_t index, int32 value);"),
    ("MobInfo option range", "src/map/map.cpp", '{{0, 0, 127, nullptr}}'),
    ("parameter range validation", "src/map/map.cpp", "value < arg.min || value > arg.max"),
    ("map instance initializes parameter storage", "src/map/map.cpp", "mapflag_values.clear();"),
    ("map instance copies parameter storage", "src/map/map.cpp", "mapflag_values = other.mapflag_values;"),
    ("NPC mapflag parser reads MobInfo option", "src/map/npc.cpp", "map_setmapflag_param(m, MF_MOBINFO, 1, mob_info_option);"),
    ("setmapflag script reads MobInfo option", "src/map/script.cpp", "map_setmapflag_param(m, MF_MOBINFO, 1, mob_info_option);"),
    ("removemapflag script resets MobInfo option", "src/map/script.cpp", "map_setmapflag_param(m, MF_MOBINFO, 1, 0);"),
    ("per-map mob info overrides global setting", "src/map/clif.cpp", "mob_info_option = map_getmapflag_param(md->bl.m, MF_MOBINFO, 1);"),
    ("@mapinfo reports the configured MobInfo option", "src/map/atcommand.cpp", 'map_getmapflag_param(m_id, MF_MOBINFO, 1)'),
    ("map-specific MobInfo can enable display", "src/map/clif.cpp", "|| (md->bl.m >= 0 && map_getmapflag(md->bl.m, MF_MOBINFO))"),
)


def main() -> None:
    failures = []
    for label, relative_path, expected in CHECKS:
        content = (ROOT / relative_path).read_text(encoding="utf-8")
        if expected not in content:
            failures.append(f"{label}: missing {expected!r} in {relative_path}")

    if failures:
        raise SystemExit("\n".join(failures))

    print(f"PASS: {len(CHECKS)} MobInfo mapflag source-contract checks")


if __name__ == "__main__":
    main()
