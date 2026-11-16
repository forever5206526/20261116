#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NoSlave mapflag regression tests."""

from __future__ import annotations

import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
MACRO = "Pandas_MapFlag_NoSlave"

HARNESS = r'''#include <cstdint>
#include <iostream>

constexpr int MF_NOSLAVE = 91;

struct block_list {
    int m;
};

struct mob_data {
    block_list bl;
};

int map_getmapflag(int map_id, int mapflag) {
    return mapflag == MF_NOSLAVE && map_id == 1;
}

int summon_attempts = 0;

int mob_summonslave(mob_data* md2, int32_t mob_id) {
    if (md2 == nullptr || mob_id <= 0)
        return 0;

@@GUARD_BLOCK@@

    ++summon_attempts;
    return 1;
}

int main() {
    mob_data blocked_map{{1}};
    mob_data normal_map{{2}};

#ifdef Pandas_MapFlag_NoSlave
    if (mob_summonslave(&blocked_map, 100) != 0) return 1;
    if (summon_attempts != 0) return 2;
    if (mob_summonslave(&normal_map, 100) != 1) return 3;
    if (summon_attempts != 1) return 4;
#else
    if (mob_summonslave(&blocked_map, 100) != 1) return 5;
    if (summon_attempts != 1) return 6;
#endif

    std::cout << "NoSlave mapflag checks passed\n";
    return 0;
}
'''


def production_guard_block() -> str:
    source = (ROOT / "src/map/mob.cpp").read_text(encoding="utf-8-sig")
    function_start = source.index("int32 mob_summonslave(")
    start = source.index(f"#ifdef {MACRO}", function_start)
    marker = f"#endif // {MACRO}"
    end = source.index(marker, start) + len(marker)
    block = source[start:end]

    if "map_getmapflag(md2->bl.m, MF_NOSLAVE)" not in block:
        raise AssertionError("NoSlave 沒有檢查召喚者所在地圖標記")
    if "return 0;" not in block:
        raise AssertionError("NoSlave 啟用時沒有中止隨從召喚")
    return block


class NoSlaveMapFlagTest(unittest.TestCase):
    def test_source_contract(self) -> None:
        config = (ROOT / "src/config/pandas.hpp").read_text(encoding="utf-8-sig")
        self.assertIn(f"#define {MACRO}", config)

        map_header = (ROOT / "src/map/map.hpp").read_text(encoding="utf-8-sig")
        self.assertIn("#ifdef Pandas_MapFlag_NoSlave\n\tMF_NOSLAVE,", map_header)

        constants = (ROOT / "src/map/script_constants.hpp").read_text(encoding="utf-8-sig")
        self.assertIn("export_constant(MF_NOSLAVE);", constants)

        self.assertIn(
            "void",
            production_guard_block()
        )

    def test_enabled_and_disabled_builds(self) -> None:
        guard = production_guard_block()
        source = HARNESS.replace("@@GUARD_BLOCK@@", guard)

        with tempfile.TemporaryDirectory(prefix="noslave-mapflag-") as temp:
            source_path = Path(temp) / "noslave.cpp"
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
                self.assertIn("NoSlave mapflag checks passed", executed.stdout)


if __name__ == "__main__":
    unittest.main()
