#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NoToken 地圖標記回歸測試。

提取正式 pc_revive_item 的 NoToken 判斷，分別編譯啟用與停用功能巨集的版本。
執行：python tools/integration/test_notoken_mapflag.py
"""

from __future__ import annotations

import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
MACRO = "Pandas_MapFlag_NoToken"
MESSAGE_ID = 1541


def production_condition() -> str:
    source = (ROOT / "src/map/pc.cpp").read_text(encoding="utf-8-sig")
    marker = f"#ifdef {MACRO}"
    start = source.index(marker)
    end_marker = f"#endif // {MACRO}"
    end = source.index(end_marker, start)
    block = source[start : end + len(end_marker)]
    expected = (
        "if (sd->bl.m >= 0 && map_getmapflag(sd->bl.m, MF_NOTOKEN))"
    )
    if expected not in block or f"msg_txt(sd, {MESSAGE_ID})" not in block:
        raise AssertionError("pc_revive_item 的 NoToken 正式阻止判斷或訊息編號缺失")
    return block


def source_contract() -> None:
    header = (ROOT / "src/map/map.hpp").read_text(encoding="utf-8-sig")
    enum_start = header.index("enum e_mapflag")
    enum_end = header.index("MF_MAX", enum_start)
    if header[enum_start:enum_end].count("MF_NOTOKEN") != 1:
        raise AssertionError("MF_NOTOKEN 必須在 e_mapflag 中、MF_MAX 之前且只出現一次")

    config = (ROOT / "src/config/pandas.hpp").read_text(encoding="utf-8-sig")
    if f"#define {MACRO}" not in config:
        raise AssertionError("Pandas 設定檔未啟用 NoToken")

    constants = (ROOT / "src/map/script_constants.hpp").read_text(encoding="utf-8-sig")
    start = constants.find(f"#ifdef {MACRO}")
    if start < 0 or "export_constant(MF_NOTOKEN);" not in constants[start : start + 160]:
        raise AssertionError("MF_NOTOKEN 腳本常量匯出缺失")

    messages = (ROOT / "conf/msg_conf/map_msg.conf").read_text(encoding="utf-8-sig")
    if f"{MESSAGE_ID}: 此地圖已停用使用齊格弗裡德之證復活的功能。" not in messages:
        raise AssertionError("NoToken 地圖提示訊息缺失")


HARNESS = r'''#include <iostream>

struct block_list {
    int m;
};
struct map_session_data {
    block_list bl;
    int fd;
};

constexpr int MF_NOTOKEN = 78;
constexpr int EXPECTED_MESSAGE = 1541;
int displayed_message_id = -1;

int map_getmapflag(int map_id, int flag) {
    if (flag != MF_NOTOKEN)
        return 0;
    if (map_id == 2)
        return 1;
    if (map_id < 0)
        return -1;
    return 0;
}

const char* msg_txt(map_session_data*, int id) {
    displayed_message_id = id;
    return "NoToken mapflag message";
}
void clif_displaymessage(int, const char*) {}

bool can_revive(map_session_data* sd) {
    if (sd == nullptr)
        return false;
@@PRODUCTION_CONDITION@@
    return true;
}

int main() {
    map_session_data normal_map{{1}, 10};
    map_session_data blocked_map{{2}, 11};
    map_session_data invalid_map{{-1}, 12};

    if (!can_revive(&normal_map)) return 1;
    if (displayed_message_id != -1) return 2;
#ifdef Pandas_MapFlag_NoToken
    if (can_revive(&blocked_map)) return 3;
    if (displayed_message_id != EXPECTED_MESSAGE) return 4;
    if (!can_revive(&invalid_map)) return 5;
#else
    if (!can_revive(&blocked_map)) return 6;
#endif
    if (can_revive(nullptr)) return 7;

    std::cout << "NoToken mapflag checks passed\n";
    return 0;
}
'''


class NoTokenMapFlagTest(unittest.TestCase):
    def test_source_contract(self) -> None:
        source_contract()
        self.assertIn("MF_NOTOKEN", production_condition())

    def test_enabled_and_disabled_builds(self) -> None:
        condition = production_condition()
        harness = HARNESS.replace("@@PRODUCTION_CONDITION@@", condition)
        with tempfile.TemporaryDirectory(prefix="notoken-mapflag-") as temp:
            source = Path(temp) / "notoken.cpp"
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
                self.assertIn("NoToken mapflag checks passed", executed.stdout)


if __name__ == "__main__":
    unittest.main()
