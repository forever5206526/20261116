#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NoSkill2 and NoAttack2 mapflag regression tests."""

from __future__ import annotations

import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]

HARNESS = r'''#include <cstddef>
#include <iostream>

constexpr int MF_NOSKILL2 = 101;
constexpr int MF_NOATTACK2 = 102;

constexpr int BL_PC = 0x001;
constexpr int BL_MOB = 0x002;
constexpr int BL_PET = 0x004;
constexpr int BL_HOM = 0x008;
constexpr int BL_MER = 0x010;
constexpr int BL_ITEM = 0x020;
constexpr int BL_SKILL = 0x040;
constexpr int BL_NPC = 0x080;
constexpr int BL_CHAT = 0x100;
constexpr int BL_ELEM = 0x200;
constexpr int BL_ALL = 0xFFF;

struct block_list { int m; int type; };
struct mob_data { block_list bl; };
struct pet_data { block_list bl; };
struct s_elemental_data { block_list bl; void* master; };

int no_skill_mask = 0;
int no_attack_mask = 0;

int map_getmapflag(int map_id, int mapflag) {
    return map_id == 1 && (mapflag == MF_NOSKILL2 || mapflag == MF_NOATTACK2);
}

int map_getmapflag_param(int map_id, int mapflag, std::size_t index) {
    if (map_id != 1 || index != 1) return 0;
    if (mapflag == MF_NOSKILL2) return no_skill_mask;
    if (mapflag == MF_NOATTACK2) return no_attack_mask;
    return 0;
}

int unit_skilluse_id2(block_list* src) {
    if (src == nullptr) return 0;
    if (src->m < 0) return 0;
@@NPC_GUARD@@
    return 1;
}

int mobskill_use(mob_data* md) {
    if (md == nullptr) return 0;
@@MOB_GUARD@@
    return 1;
}

int pet_attackskill(pet_data* pd) {
    if (pd == nullptr) return 0;
@@PET_GUARD@@
    return 1;
}

bool elemental_skillnotok(s_elemental_data& ed) {
    const unsigned int idx = 1;
    if (idx == 0) return false;
@@ELEM_GUARD@@
    return false;
}

int unit_attack(block_list* src) {
    if (src == nullptr) return 1;
@@NOATTACK_GUARD@@
    return 0;
}

int main() {
    int master = 1;
    block_list npc{1, BL_NPC}, npc_other_map{2, BL_NPC}, player{1, BL_PC};
    mob_data mob{{1, BL_MOB}}, mob_other_map{{2, BL_MOB}};
    pet_data pet{{1, BL_PET}}, pet_other_map{{2, BL_PET}};
    s_elemental_data elem{{1, BL_ELEM}, &master}, elem_other_map{{2, BL_ELEM}, &master};
    block_list mob_attack{1, BL_MOB}, hom_attack{1, BL_HOM}, player_attack{1, BL_PC}, mob_other_attack_map{2, BL_MOB};

#ifdef Pandas_MapFlag_NoSkill2
    no_skill_mask = BL_NPC | BL_MOB | BL_PET | BL_ELEM;
    if (unit_skilluse_id2(&npc) != 0) return 1;
    if (unit_skilluse_id2(&npc_other_map) != 1) return 2;
    if (unit_skilluse_id2(&player) != 1) return 3;
    if (mobskill_use(&mob) != 0 || mobskill_use(&mob_other_map) != 1) return 4;
    if (pet_attackskill(&pet) != 0 || pet_attackskill(&pet_other_map) != 1) return 5;
    if (!elemental_skillnotok(elem) || elemental_skillnotok(elem_other_map)) return 6;
    no_skill_mask = BL_MOB;
    if (elemental_skillnotok(elem)) return 7;
#else
    if (unit_skilluse_id2(&npc) != 1 || mobskill_use(&mob) != 1 ||
        pet_attackskill(&pet) != 1 || elemental_skillnotok(elem)) return 8;
#endif

#ifdef Pandas_MapFlag_NoAttack2
    no_attack_mask = BL_MOB | BL_HOM;
    if (unit_attack(&mob_attack) != 1) return 9;
    if (unit_attack(&hom_attack) != 1) return 10;
    if (unit_attack(&player_attack) != 0) return 11;
    if (unit_attack(&mob_other_attack_map) != 0) return 12;
    no_attack_mask = 0;
    if (unit_attack(&mob_attack) != 0) return 13;
#else
    if (unit_attack(&mob_attack) != 0) return 14;
#endif

    std::cout << "NoSkill2 and NoAttack2 mask checks passed\n";
    return 0;
}
'''


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig")


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def production_guard(path: str, signature: str, macro: str) -> str:
    source = read(path)
    function_start = source.index(signature)
    start = source.index(f"#ifdef {macro}", function_start)
    marker = f"#endif // {macro}"
    end = source.index(marker, start) + len(marker)
    return source[start:end]


def main() -> None:
    failures: list[str] = []
    config = read("src/config/pandas.hpp")
    map_header = read("src/map/map.hpp")
    map_source = read("src/map/map.cpp")
    constants = read("src/map/script_constants.hpp")
    README = read("README.md")
    workflow = read(".github/workflows/windows-cloud-validation.yml")

    switches = (
        ("Pandas_MapFlag_NoSkill2", "MF_NOSKILL2"),
        ("Pandas_MapFlag_NoAttack2", "MF_NOATTACK2"),
    )
    for macro, flag in switches:
        require(config.count(f"#define {macro}") == 1,
                f"{macro} must be enabled exactly once", failures)
        require(map_header.count(f"{flag},") == 1,
                f"{flag} enum must exist exactly once", failures)
        require(constants.count(f"export_constant({flag});") == 1,
                f"{flag} must be exported to NPC scripts", failures)

    no_skill_config = """#ifdef Pandas_MapFlag_NoSkill2
\tmapflag_config.emplace(MF_NOSKILL2, s_mapflag_item{
\t\t"NoSkill2",
\t\ttrue,
\t\ttrue,
\t\t{{0, 0, BL_ALL, nullptr}}
\t});
#endif // Pandas_MapFlag_NoSkill2"""
    no_attack_config = """#ifdef Pandas_MapFlag_NoAttack2
\tmapflag_config.emplace(MF_NOATTACK2, s_mapflag_item{
\t\t"NoAttack2",
\t\tfalse,
\t\tfalse,
\t\t{{0, 0, BL_ALL, nullptr}}
\t});
#endif // Pandas_MapFlag_NoAttack2"""
    require(no_skill_config in map_source,
            "NoSkill2 must use zero default, BL_ALL range, auto-disable-default and block direct @mapflag activation", failures)
    require(no_attack_config in map_source,
            "NoAttack2 must preserve zero default, BL_ALL range, and the upstream non-blocking @mapflag setting", failures)

    npc = production_guard("src/map/unit.cpp", "int32 unit_skilluse_id2(", "Pandas_MapFlag_NoSkill2")
    mob = production_guard("src/map/mob.cpp", "int32 mobskill_use(", "Pandas_MapFlag_NoSkill2")
    pet = production_guard("src/map/pet.cpp", "int32 pet_attackskill(", "Pandas_MapFlag_NoSkill2")
    elemental = production_guard("src/map/elemental.cpp", "bool elemental_skillnotok(", "Pandas_MapFlag_NoSkill2")
    attack = production_guard("src/map/unit.cpp", "int32 unit_attack(", "Pandas_MapFlag_NoAttack2")

    for label, block, unit_type, source_expr in (
        ("NPC", npc, "BL_NPC", "src->type == BL_NPC"),
        ("MOB", mob, "BL_MOB", "md->bl.m"),
        ("PET", pet, "BL_PET", "pd->bl.m"),
        ("ELEM", elemental, "BL_ELEM", "ed.bl.m"),
    ):
        require(unit_type in block and source_expr in block and
                f"map_getmapflag_param" in block and "return 0;" in block if label != "ELEM" else
                (unit_type in block and source_expr in block and "map_getmapflag_param" in block and "return true;" in block),
                f"NoSkill2 must enforce the {label} unit mask at its upstream skill entry point", failures)
    require("src->type" in attack and "map_getmapflag_param" in attack and
            "return 1;" in attack and "MF_NOATTACK2" in attack,
            "NoAttack2 must reject normal attacks for matching source unit types", failures)

    # The upstream develop elemental branch returns false here, which bypasses the
    # function's normal 'not OK' return path. Use true so BL_ELEM is actually blocked.
    require("return true; // This function returns true when the elemental skill is not allowed." in elemental,
            "Elemental NoSkill2 must report masked skills as not allowed (avoid the upstream inverted return)", failures)

    require("### NoSkill2／NoAttack2 地圖標記" in README and
            "BL_NPC|BL_MOB|BL_PET|BL_ELEM" in README and
            "BL_MOB|BL_HOM" in README and
            'removemapflag "prontera", MF_NOSKILL2;' in README and
            'removemapflag "prontera", MF_NOATTACK2;' in README,
            "README must document bitmask set/remove examples for both flags", failures)
    require("run: python tools/integration/test_no_skill_attack2_mapflags.py" in workflow,
            "Windows workflow must run the NoSkill2/NoAttack2 regression test", failures)

    if failures:
        raise SystemExit("\n".join(failures))

    guards = {
        "@@NPC_GUARD@@": npc,
        "@@MOB_GUARD@@": mob,
        "@@PET_GUARD@@": pet,
        "@@ELEM_GUARD@@": elemental,
        "@@NOATTACK_GUARD@@": attack,
    }
    harness = HARNESS
    for token, block in guards.items():
        harness = harness.replace(token, block)

    with tempfile.TemporaryDirectory(prefix="noskill-noattack2-mapflag-") as temp:
        source_path = Path(temp) / "mapflags.cpp"
        source_path.write_text(harness, encoding="utf-8")
        compiler = shlex.split(os.environ.get("CXX", "c++"))

        for enabled in (True, False):
            label = "enabled" if enabled else "disabled"
            binary = Path(temp) / label
            command = compiler + ["-std=c++17", str(source_path), "-o", str(binary)]
            if enabled:
                command.insert(1, "-DPandas_MapFlag_NoSkill2")
                command.insert(2, "-DPandas_MapFlag_NoAttack2")

            compiled = subprocess.run(command, capture_output=True, text=True)
            require(compiled.returncode == 0,
                    f"{label} C++ harness build failed: {compiled.stderr}", failures)
            if compiled.returncode == 0:
                executed = subprocess.run([str(binary)], capture_output=True, text=True)
                require(executed.returncode == 0,
                        f"{label} mask behavior failed ({executed.returncode}): {executed.stdout}{executed.stderr}", failures)
                require("NoSkill2 and NoAttack2 mask checks passed" in executed.stdout,
                        f"{label} harness did not complete successfully", failures)

    if failures:
        raise SystemExit("\n".join(failures))
    print("PASS: NoSkill2 NPC/MOB/PET/ELEM masks, NoAttack2 unit-type masks, enabled/disabled builds, config metadata, constants, docs")


if __name__ == "__main__":
    main()
