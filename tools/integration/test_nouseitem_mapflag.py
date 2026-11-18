#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NoUseItem mapflag regression tests."""

from __future__ import annotations

import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
MACRO = "Pandas_MapFlag_NoUseItem"
MESSAGE_ID = 1543

HARNESS = r'''#include <iostream>

constexpr int MF_NOUSEITEM = 93;
constexpr int COLOR_RED = 1;
constexpr int SELF = 0;
const int color_table[] = {0, 1};

struct block_list { int m; };
struct map_session_data { block_list bl; };

int map_getmapflag(int map_id, int mapflag) {
    return map_id == 1 && mapflag == MF_NOUSEITEM;
}

int message_count = 0;
int last_message_id = 0;
int last_color = 0;

const char* msg_txt(map_session_data*, int id) {
    last_message_id = id;
    return "NoUseItem is enabled on this map.";
}

void clif_messagecolor(block_list*, int color, const char* message, bool, int) {
    last_color = color;
    if (message != nullptr && message[0] != '\0') ++message_count;
}

int pc_useitem(map_session_data* sd) {
    if (sd == nullptr) return 0;

@@GUARD_BLOCK@@

    return 1;
}

int main() {
    map_session_data blocked_map{{1}};
    map_session_data normal_map{{2}};

#ifdef Pandas_MapFlag_NoUseItem
    if (pc_useitem(&blocked_map) != 0) return 1;
    if (message_count != 1 || last_message_id != 1543 || last_color != COLOR_RED) return 2;
    if (pc_useitem(&normal_map) != 1) return 3;
    if (message_count != 1) return 4;
#else
    if (pc_useitem(&blocked_map) != 1) return 5;
    if (message_count != 0) return 6;
#endif

    std::cout << "NoUseItem mapflag checks passed\n";
    return 0;
}
'''


def production_guard_block() -> str:
    source = (ROOT / "src/map/pc.cpp").read_text(encoding="utf-8-sig")
    function_start = source.index("int32 pc_useitem(")
    start = source.index(f"#ifdef {MACRO}", function_start)
    marker = f"#endif // {MACRO}"
    end = source.index(marker, start) + len(marker)
    block = source[start:end]

    if "map_getmapflag(sd->bl.m, MF_NOUSEITEM)" not in block:
        raise AssertionError("NoUseItem 沒有檢查玩家所在地圖標記")
    if "msg_txt(sd, 1543)" not in block:
        raise AssertionError("NoUseItem 未使用指定訊息 ID")
    if "return 0;" not in block:
        raise AssertionError("NoUseItem 啟用時沒有拒絕道具使用")
    return block


class NoUseItemMapFlagTest(unittest.TestCase):
    def test_source_contract(self) -> None:
        config = (ROOT / "src/config/pandas.hpp").read_text(encoding="utf-8-sig")
        self.assertIn(f"#define {MACRO}", config)

        map_header = (ROOT / "src/map/map.hpp").read_text(encoding="utf-8-sig")
        self.assertIn("#ifdef Pandas_MapFlag_NoUseItem\n\tMF_NOUSEITEM,", map_header)

        constants = (ROOT / "src/map/script_constants.hpp").read_text(encoding="utf-8-sig")
        self.assertIn("export_constant(MF_NOUSEITEM);", constants)

        english = (ROOT / "conf/msg_conf/map_msg.conf").read_text(encoding="utf-8-sig")
        chinese = (ROOT / "conf/msg_conf/map_msg_chn.conf").read_text(encoding="utf-8-sig")
        self.assertIn("1543: 此地圖禁止使用消耗型道具。", english)
        self.assertIn("1543: 此地圖禁止使用消耗型道具。", chinese)

        guard = production_guard_block()
        self.assertTrue(guard.startswith(f"#ifdef {MACRO}"))
        self.assertTrue(guard.rstrip().endswith(f"#endif // {MACRO}"))

    def test_enabled_and_disabled_builds(self) -> None:
        source = HARNESS.replace("@@GUARD_BLOCK@@", production_guard_block())
        with tempfile.TemporaryDirectory(prefix="nouseitem-mapflag-") as temp:
            source_path = Path(temp) / "nouseitem.cpp"
            source_path.write_text(source, encoding="utf-8")
            compiler = shlex.split(os.environ.get("CXX", "c++"))

            for enabled in (True, False):
                binary = Path(temp) / ("enabled" if enabled else "disabled")
                command = compiler + ["-std=c++17", str(source_path), "-o", str(binary)]
                if enabled:
                    command.insert(1, f"-D{MACRO}")
                result = subprocess.run(command, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                executed = subprocess.run([str(binary)], capture_output=True, text=True)
                self.assertEqual(executed.returncode, 0, executed.stdout + executed.stderr)
                self.assertIn("NoUseItem mapflag checks passed", executed.stdout)


if __name__ == "__main__":
    unittest.main()
