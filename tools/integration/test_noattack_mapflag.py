#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NoAttack mapflag regression tests."""

from __future__ import annotations

import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
MACRO = "Pandas_MapFlag_NoAttack"

HARNESS = r'''#include <iostream>

constexpr int MF_NOATTACK = 92;

struct block_list {
    int m;
};

int map_getmapflag(int map_id, int mapflag) {
    return mapflag == MF_NOATTACK && map_id == 1;
}

int unit_attack(block_list* src) {
    if (src == nullptr)
        return 1;

@@GUARD_BLOCK@@

    return 0;
}

int main() {
    block_list blocked_map{1};
    block_list normal_map{2};

#ifdef Pandas_MapFlag_NoAttack
    if (unit_attack(&blocked_map) != 1) return 1;
    if (unit_attack(&normal_map) != 0) return 2;
#else
    if (unit_attack(&blocked_map) != 0) return 3;
#endif

    std::cout << "NoAttack mapflag checks passed\n";
    return 0;
}
'''


def production_guard_block() -> str:
    source = (ROOT / "src/map/unit.cpp").read_text(encoding="utf-8-sig")
    function_start = source.index("int32 unit_attack(")
    start = source.index(f"#ifdef {MACRO}", function_start)
    marker = f"#endif // {MACRO}"
    end = source.index(marker, start) + len(marker)
    block = source[start:end]

    if "map_getmapflag(src->m, MF_NOATTACK)" not in block:
        raise AssertionError("NoAttack 沒有檢查攻擊來源所在地圖")
    if "return 1;" not in block:
        raise AssertionError("NoAttack 啟用時沒有拒絕普通攻擊")
    return block


class NoAttackMapFlagTest(unittest.TestCase):
    def test_source_contract(self) -> None:
        config = (ROOT / "src/config/pandas.hpp").read_text(encoding="utf-8-sig")
        self.assertIn(f"#define {MACRO}", config)

        map_header = (ROOT / "src/map/map.hpp").read_text(encoding="utf-8-sig")
        self.assertIn("#ifdef Pandas_MapFlag_NoAttack\n\tMF_NOATTACK,", map_header)

        constants = (ROOT / "src/map/script_constants.hpp").read_text(encoding="utf-8-sig")
        self.assertIn("export_constant(MF_NOATTACK);", constants)

        guard = production_guard_block()
        self.assertTrue(guard.startswith(f"#ifdef {MACRO}"))
        self.assertTrue(guard.rstrip().endswith(f"#endif // {MACRO}"))

    def test_enabled_and_disabled_builds(self) -> None:
        guard = production_guard_block()
        source = HARNESS.replace("@@GUARD_BLOCK@@", guard)

        with tempfile.TemporaryDirectory(prefix="noattack-mapflag-") as temp:
            source_path = Path(temp) / "noattack.cpp"
            source_path.write_text(source, encoding="utf-8")
            compiler = shlex.split(os.environ.get("CXX", "c++"))

            for enabled in (True, False):
                name = "enabled" if enabled else "disabled"
                binary = Path(temp) / name
                command = compiler + ["-std=c++17", str(source_path), "-o", str(binary)]
                if enabled:
                    command.insert(1, f"-D{MACRO}")

                result = subprocess.run(command, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)

                executed = subprocess.run([str(binary)], capture_output=True, text=True)
                self.assertEqual(
                    executed.returncode, 0, executed.stdout + executed.stderr
                )
                self.assertIn("NoAttack mapflag checks passed", executed.stdout)


if __name__ == "__main__":
    unittest.main()
