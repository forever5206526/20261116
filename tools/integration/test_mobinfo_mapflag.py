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
    ("ordinary drop-rate feature switch", "src/config/pandas.hpp", "#define Pandas_MapFlag_MobDroprate"),
    ("MVP drop-rate feature switch", "src/config/pandas.hpp", "#define Pandas_MapFlag_MvpDroprate"),
    ("ordinary drop-rate mapflag enum", "src/map/map.hpp", "MF_MOBDROPRATE,"),
    ("MVP drop-rate mapflag enum", "src/map/map.hpp", "MF_MVPDROPRATE,"),
    ("ordinary drop-rate script constant", "src/map/script_constants.hpp", "export_constant(MF_MOBDROPRATE);"),
    ("MVP drop-rate script constant", "src/map/script_constants.hpp", "export_constant(MF_MVPDROPRATE);"),
    ("ordinary drop-rate mapflag configuration", "src/map/map.cpp", '"MobDroprate"'),
    ("MVP drop-rate mapflag configuration", "src/map/map.cpp", '"MvpDroprate"'),
    ("drop-rate mapflag default/range/unit", "src/map/map.cpp", '{{100, 0, INT_MAX, "%"}}'),
    ("ordinary mob map-specific rate application", "src/map/mob.cpp", "map_getmapflag_param(md->bl.m, MF_MOBDROPRATE, 1)"),
    ("MVP map-specific rate application", "src/map/mob.cpp", "map_getmapflag_param(md->bl.m, MF_MVPDROPRATE, 1)"),
)


def check_drop_rate_behavior(failures: list[str]) -> None:
    mob_source = (ROOT / "src/map/mob.cpp").read_text(encoding="utf-8")
    start = mob_source.find("int32 mob_getdroprate(")
    end = mob_source.find("\n}\n", start)
    if start < 0 or end < 0:
        failures.append("mob_getdroprate function: not found")
        return
    function = mob_source[start:end]

    cases = (
        (
            "Pandas_MapFlag_MobDroprate",
            "if (md && !status_has_mode(&md->status, MD_MVP))",
            "MF_MOBDROPRATE",
        ),
        (
            "Pandas_MapFlag_MvpDroprate",
            "if (md && status_has_mode(&md->status, MD_MVP))",
            "MF_MVPDROPRATE",
        ),
    )
    for macro, condition, mapflag in cases:
        marker = f"#ifdef {macro}"
        block_start = function.find(marker)
        block_end = function.find("#endif", block_start)
        if block_start < 0 or block_end < 0:
            failures.append(f"{macro}: conditional block missing in mob_getdroprate")
            continue
        block = function[block_start:block_end]
        for label, expected in (
            ("monster type guard", condition),
            ("matching mapflag", mapflag),
            ("rate application", "apply_rate(drop_rate, map_getmapflag_param"),
        ):
            if expected not in block:
                failures.append(f"{macro}: missing {label} ({expected!r})")

    ordered_markers = (
        "#ifdef Pandas_MapFlag_MobDroprate",
        "#ifdef Pandas_MapFlag_MvpDroprate",
        "#ifdef RENEWAL_DROP",
        "// Cap it to 100%",
    )
    positions = [function.find(marker) for marker in ordered_markers]
    if any(position < 0 for position in positions) or positions != sorted(positions):
        failures.append("drop-rate order: ordinary/MVP map modifiers must precede RENEWAL_DROP and the 100% cap")


def main() -> None:
    failures = []
    for label, relative_path, expected in CHECKS:
        content = (ROOT / relative_path).read_text(encoding="utf-8")
        if expected not in content:
            failures.append(f"{label}: missing {expected!r} in {relative_path}")

    check_drop_rate_behavior(failures)

    if failures:
        raise SystemExit("\n".join(failures))

    print(f"PASS: {len(CHECKS) + 7} generic mapflag parameter, MobInfo, and MobDroprate/MvpDroprate source-contract checks")


if __name__ == "__main__":
    main()
