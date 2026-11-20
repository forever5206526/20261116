from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def cap_pair(main_hand: int, off_hand: int, limit: int) -> tuple[int, int]:
    """Mirror the upstream damage-pair capping order for boundary tests."""
    if limit > 0 and main_hand + off_hand > limit:
        over = main_hand + off_hand - limit
        if off_hand >= over:
            off_hand -= over
        else:
            over -= off_hand
            off_hand = 0
            main_hand = max(0, min(main_hand - over, limit))
    return main_hand, off_hand


def main() -> None:
    failures: list[str] = []
    config = read("src/config/pandas.hpp")
    enum = read("src/map/map.hpp")
    map_source = read("src/map/map.cpp")
    battle = read("src/map/battle.cpp")
    constants = read("src/map/script_constants.hpp")
    readme = read("README.md")
    workflow = read(".github/workflows/windows-cloud-validation.yml")

    for switch, flag in (
        ("Pandas_MapFlag_MaxDmg_Skill", "MF_MAXDMG_SKILL"),
        ("Pandas_MapFlag_MaxDmg_Normal", "MF_MAXDMG_NORMAL"),
    ):
        require(config.count(f"#define {switch}") == 1,
                f"{switch} must be enabled exactly once", failures)
        require(enum.count(f"#ifdef {switch}\n\t{flag},\n#endif // {switch}") == 1,
                f"{flag} must have one guarded enum entry", failures)
        require(constants.count(f"export_constant({flag});") == 1,
                f"{flag} must be exported to NPC scripts", failures)

    for switch, flag, name in (
        ("Pandas_MapFlag_MaxDmg_Skill", "MF_MAXDMG_SKILL", "MaxDmg_Skill"),
        ("Pandas_MapFlag_MaxDmg_Normal", "MF_MAXDMG_NORMAL", "MaxDmg_Normal"),
    ):
        registration = f"""#ifdef {switch}
\tmapflag_config.emplace({flag}, s_mapflag_item{{
\t\t"{name}",
\t\ttrue,
\t\ttrue,
\t\t{{{{0, 0, INT_MAX, nullptr}}}}
\t}});
#endif // {switch}"""
        require(registration in map_source,
                f"{name} must register a zero-default, non-negative parameter and block direct @mapflag activation",
                failures)

    function_start = battle.find("struct Damage battle_calc_attack")
    function_end = battle.find("\n}\n", function_start)
    require(function_start >= 0 and function_end > function_start,
            "battle_calc_attack function boundary must be present", failures)
    function = battle[function_start:function_end + 3] if function_start >= 0 and function_end > function_start else ""

    skill_start = function.find("#ifdef Pandas_MapFlag_MaxDmg_Skill")
    skill_end = function.find("#endif // Pandas_MapFlag_MaxDmg_Skill", skill_start)
    normal_start = function.find("#ifdef Pandas_MapFlag_MaxDmg_Normal")
    normal_end = function.find("#endif // Pandas_MapFlag_MaxDmg_Normal", normal_start)
    skill_block = function[skill_start:skill_end + len("#endif // Pandas_MapFlag_MaxDmg_Skill")] if skill_start >= 0 and skill_end >= 0 else ""
    normal_block = function[normal_start:normal_end + len("#endif // Pandas_MapFlag_MaxDmg_Normal")] if normal_start >= 0 and normal_end >= 0 else ""

    require(skill_start >= 0 and normal_start > skill_start,
            "skill and normal damage caps must be separate guarded blocks", failures)
    require("if (skill_id && bl && map_getmapflag(bl->m, MF_MAXDMG_SKILL))" in skill_block and
            "map_getmapflag_param(bl->m, MF_MAXDMG_SKILL, 1)" in skill_block,
            "skill cap must be selected by non-zero skill ID on the attacker's map", failures)
    require("if (!skill_id && bl && map_getmapflag(bl->m, MF_MAXDMG_NORMAL))" in normal_block and
            "map_getmapflag_param(bl->m, MF_MAXDMG_NORMAL, 1)" in normal_block,
            "normal cap must be selected only by zero skill ID on the attacker's map", failures)
    for label, block in (("skill", skill_block), ("normal", normal_block)):
        require("if (val > 0 && d.damage + d.damage2 > val)" in block and
                "int64 overval = (d.damage + d.damage2) - val;" in block and
                "if (d.damage2 >= overval)" in block and
                "d.damage2 -= overval;" in block and
                "d.damage = cap_value(d.damage - overval, 0, val);" in block,
                f"{label} cap must limit main/off-hand damage together without negative damage", failures)

    vanish_pos = function.find("battle_vanish_damage(sd, target, d.flag)")
    require(skill_start >= 0 and normal_end >= 0 and vanish_pos > normal_end,
            "damage caps must be applied before damage-vanish side effects", failures)

    require("### MaxDmg_Skill／MaxDmg_Normal 地圖標記" in readme and
            'setmapflag "prontera", MF_MAXDMG_SKILL, 50000;' in readme and
            'setmapflag "prontera", MF_MAXDMG_NORMAL, 10000;' in readme and
            'removemapflag "prontera", MF_MAXDMG_SKILL;' in readme and
            'removemapflag "prontera", MF_MAXDMG_NORMAL;' in readme,
            "README must document both flags and their set/remove script examples", failures)
    require("run: python tools/integration/test_maxdmg_mapflags.py" in workflow,
            "Windows cloud validation must execute the MaxDmg regression test", failures)

    # Boundary cases: off-hand damage is reduced first, then main-hand damage.
    require(cap_pair(5000, 2000, 6000) == (5000, 1000),
            "cap must reduce off-hand damage first when that is sufficient", failures)
    require(cap_pair(5000, 2000, 4000) == (4000, 0),
            "cap must reduce off-hand then main-hand damage when needed", failures)
    require(cap_pair(1000, 5000, 3000) == (1000, 2000),
            "cap must handle off-hand-heavy attacks", failures)
    require(cap_pair(1000, 500, 0) == (1000, 500) and
            cap_pair(1000, 500, 2000) == (1000, 500),
            "zero or higher-than-current limits must leave damage unchanged", failures)

    if failures:
        raise SystemExit("\n".join(failures))
    print("PASS: MaxDmg_Skill/Normal switches, mapflags, script constants, attacker-map damage caps, hand-priority boundaries, docs, and workflow")


if __name__ == "__main__":
    main()
