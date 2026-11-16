#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NoAutoLoot 地圖標記回歸測試。

提取正式 mob_item_drop 的 NoAutoLoot 條件，分別編譯啟用與停用功能巨集的版本。
執行：python tools/integration/test_noautoloot_mapflag.py
"""

from __future__ import annotations

import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
MACRO = "Pandas_MapFlag_NoAutoLoot"


def production_condition() -> str:
    source = (ROOT / "src/map/mob.cpp").read_text(encoding="utf-8-sig")
    marker = f"#ifdef {MACRO}"
    start = source.index(marker)
    end_marker = f"#endif // {MACRO}"
    end = source.index(end_marker, start)
    block = source[start : end + len(end_marker)]
    expected = (
        "test_autoloot = test_autoloot && "
        "(sd && sd->bl.m >= 0 && !map_getmapflag(sd->bl.m, MF_NOAUTOLOOT));"
    )
    if expected not in block:
        raise AssertionError("mob_item_drop 的 NoAutoLoot 正式判斷式不存在")
    return block


def source_contract() -> None:
    header = (ROOT / "src/map/map.hpp").read_text(encoding="utf-8-sig")
    enum_start = header.index("enum e_mapflag")
    enum_end = header.index("MF_MAX", enum_start)
    enum_body = header[enum_start:enum_end]
    if enum_body.count("MF_NOAUTOLOOT") != 1:
        raise AssertionError("MF_NOAUTOLOOT 必須在 e_mapflag 中、MF_MAX 之前且只出現一次")

    config = (ROOT / "src/config/pandas.hpp").read_text(encoding="utf-8-sig")
    if f"#define {MACRO}" not in config:
        raise AssertionError("Pandas 設定檔未啟用 NoAutoLoot")

    constants = (ROOT / "src/map/script_constants.hpp").read_text(encoding="utf-8-sig")
    start = constants.find(f"#ifdef {MACRO}")
    if start < 0 or "export_constant(MF_NOAUTOLOOT);" not in constants[start : start + 160]:
        raise AssertionError("MF_NOAUTOLOOT 腳本常量匯出缺失")


HARNESS = r'''#include <iostream>

struct block_list {
    int m;
};
struct map_session_data {
    block_list bl;
};

constexpr int MF_NOAUTOLOOT = 77;

int map_getmapflag(int map_id, int flag) {
    if (flag != MF_NOAUTOLOOT)
        return 0;
    if (map_id == 2)
        return 1;
    if (map_id < 0)
        return -1;
    return 0;
}

bool should_autoloot(map_session_data* sd, bool test_autoloot) {
@@PRODUCTION_CONDITION@@
    return test_autoloot;
}

int main() {
    map_session_data normal_map{{1}};
    map_session_data blocked_map{{2}};
    map_session_data invalid_map{{-1}};

    if (!should_autoloot(&normal_map, true)) return 1;
#ifdef Pandas_MapFlag_NoAutoLoot
    if (should_autoloot(&blocked_map, true)) return 2;
    if (should_autoloot(&invalid_map, true)) return 3;
#else
    if (!should_autoloot(&blocked_map, true)) return 4;
    if (!should_autoloot(&invalid_map, true)) return 5;
#endif
    if (should_autoloot(nullptr, false)) return 6;

    std::cout << "NoAutoLoot mapflag checks passed\n";
    return 0;
}
'''


class NoAutoLootMapFlagTest(unittest.TestCase):
    def test_source_contract(self) -> None:
        source_contract()
        self.assertIn("MF_NOAUTOLOOT", production_condition())

    def test_enabled_and_disabled_builds(self) -> None:
        condition = production_condition()
        harness = HARNESS.replace("@@PRODUCTION_CONDITION@@", condition)
        with tempfile.TemporaryDirectory(prefix="noautoloot-mapflag-") as temp:
            source = Path(temp) / "noautoloot.cpp"
            source.write_text(harness, encoding="utf-8")
            compiler = shlex.split(os.environ.get("CXX", "c++"))

            for enabled in (True, False):
                name = "enabled" if enabled else "disabled"
                binary = Path(temp) / name
                command = compiler + ["-std=c++17", str(source), "-o", str(binary)]
                if enabled:
                    command.insert(-4, f"-D{MACRO}")
                result = subprocess.run(command, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)

                executed = subprocess.run([str(binary)], capture_output=True, text=True)
                self.assertEqual(executed.returncode, 0, executed.stdout + executed.stderr)
                self.assertIn("NoAutoLoot mapflag checks passed", executed.stdout)


if __name__ == "__main__":
    unittest.main()
