"""Source-contract regression checks for generic Pandas mapflag parameters and MobInfo."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CHECKS = (
    ("generic mapflag feature switch", "src/config/pandas.hpp", "#define Pandas_Mapflags"),
    ("MobInfo feature switch", "src/config/pandas.hpp", "#define Pandas_MapFlag_MobInfo"),
    ("MobInfo mapflag enum", "src/map/map.hpp", "MF_MOBINFO,"),
    ("MobInfo script constant", "src/map/script_constants.hpp", "export_constant(MF_MOBINFO);"),
    ("parameterized mapflag configuration", "src/map/map.hpp", "struct s_mapflag_item_args"),
    ("mapflag argument storage uses struct when enabled", "src/map/map.hpp", "struct u_mapflag_args"),
    ("generic mapflag argument vector", "src/map/map.hpp", "std::vector<int32> input;"),
    ("per-map parameter storage", "src/map/map.hpp", "std::unordered_map<e_mapflag, std::vector<int32>> mapflag_values;"),
    ("parameter validation API", "src/map/map.hpp", "bool map_mapflag_valid_index(e_mapflag mapflag, size_t index);"),
    ("parameter getter API", "src/map/map.hpp", "int32 map_getmapflag_param(int16 m, enum e_mapflag mapflag, size_t index);"),
    ("single parameter setter API", "src/map/map.hpp", "void map_setmapflag_param(int16 m, enum e_mapflag mapflag, size_t index, int32 value);"),
    ("bulk parameter setter API", "src/map/map.hpp", "const std::vector<int32>& values"),
    ("parameter reset API", "src/map/map.hpp", "void map_setmapflag_param_reset(int16 m, enum e_mapflag mapflag);"),
    ("MobInfo option range", "src/map/map.cpp", "{{0, 0, 127, nullptr}}"),
    ("parameter range validation", "src/map/map.cpp", "value < arg.min || value > arg.max"),
    ("bulk parameter assignment", "src/map/map.cpp", "map_setmapflag_param(m, mapflag, args->input);"),
    ("parameter reset when removing a mapflag", "src/map/map.cpp", "map_setmapflag_param_reset(m, mapflag);"),
    ("map instance initializes parameter storage", "src/map/map.cpp", "mapflag_values.clear();"),
    ("map instance copies parameter storage", "src/map/map.cpp", "mapflag_values = other.mapflag_values;"),
    ("NPC mapflag parser uses generic argument vector", "src/map/npc.cpp", "args.input.resize(args_count);"),
    ("NPC mapflag parser calls shared mapflag handler", "src/map/npc.cpp", "map_setmapflag_sub(m, mapflag, state, &args);"),
    ("setmapflag script uses generic argument vector", "src/map/script.cpp", "args.input[i] = conf->args[i].def_val;"),
    ("removemapflag script uses shared reset handler", "src/map/script.cpp", "map_setmapflag_sub(m, static_cast<e_mapflag>(mf), false, &args);"),
    ("per-map MobInfo overrides global setting", "src/map/clif.cpp", "mob_info_option = map_getmapflag_param(md->bl.m, MF_MOBINFO, 1);"),
    ("@mapinfo lists configured mapflag parameters", "src/map/atcommand.cpp", "Pandas MapFlags:"),
    ("@mapflag honors generic block_atcmd configuration", "src/map/atcommand.cpp", "if (entry.second.block_atcmd)"),
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

    print(f"PASS: {len(CHECKS)} generic mapflag parameter and MobInfo source-contract checks")


if __name__ == "__main__":
    main()
