from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> None:
    failures: list[str] = []
    config = read("src/config/pandas.hpp")
    enum = read("src/map/map.hpp")
    map_source = read("src/map/map.cpp")
    skill = read("src/map/skill.cpp")
    constants = read("src/map/script_constants.hpp")
    readme = read("README.md")

    require("#define Pandas_MapFlag_MaxHeal" in config,
            "MaxHeal feature switch must be enabled", failures)
    require("#ifdef Pandas_MapFlag_MaxHeal\n\tMF_MAXHEAL," in enum,
            "MF_MAXHEAL enum must be guarded by its feature switch", failures)
    require('mapflag_config.emplace(MF_MAXHEAL, s_mapflag_item{' in map_source and
            '"MaxHeal"' in map_source and '{{0, 0, INT_MAX, nullptr}}' in map_source,
            "MaxHeal must register a zero-default, non-negative mapflag parameter", failures)
    require("export_constant(MF_MAXHEAL);" in constants,
            "MF_MAXHEAL must be available to NPC scripts", failures)
    require(skill.count("#ifdef Pandas_MapFlag_MaxHeal") == 2 and
            skill.count("map_getmapflag_param(src->m, MF_MAXHEAL, 1)") == 2 and
            skill.count("cap_value(") >= 2,
            "MaxHeal must cap final healing in both Renewal and non-Renewal formulas", failures)
    require('setmapflag "prontera", MF_MAXHEAL, 5000;' in readme and
            'removemapflag "prontera", MF_MAXHEAL;' in readme,
            "README must document setting and removing MaxHeal", failures)
    if failures:
        raise SystemExit("\n".join(failures))
    print("PASS: MaxHeal mapflag configuration, script constant, Renewal/non-Renewal healing cap, and docs")


if __name__ == "__main__":
    main()
