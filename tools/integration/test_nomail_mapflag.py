#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NoMail 地圖標記回歸測試。"""

from __future__ import annotations
import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
MACRO = "Pandas_MapFlag_NoMail"
MESSAGE_ID = 1542


def production_condition() -> str:
    source = (ROOT / "src/map/mail.cpp").read_text(encoding="utf-8-sig")
    marker = f"#ifdef {MACRO}"
    start = source.index(marker, source.index("bool mail_invalid_operation("))
    end_marker = f"#endif // {MACRO}"
    end = source.index(end_marker, start)
    block = source[start : end + len(end_marker)]
    expected = "if (map_getmapflag(sd->bl.m, MF_NOMAIL))"
    if expected not in block or f"msg_txt(sd, {MESSAGE_ID})" not in block:
        raise AssertionError("mail_invalid_operation 的 NoMail 判斷或提示訊息缺失")
    return block


def source_contract() -> None:
    header = (ROOT / "src/map/map.hpp").read_text(encoding="utf-8-sig")
    enum_start = header.index("enum e_mapflag")
    enum_end = header.index("MF_MAX", enum_start)
    if header[enum_start:enum_end].count("MF_NOMAIL") != 1:
        raise AssertionError("MF_NOMAIL 列舉值缺失或重複")

    config = (ROOT / "src/config/pandas.hpp").read_text(encoding="utf-8-sig")
    if f"#define {MACRO}" not in config:
        raise AssertionError("Pandas 設定檔未啟用 NoMail")

    constants = (ROOT / "src/map/script_constants.hpp").read_text(encoding="utf-8-sig")
    start = constants.find(f"#ifdef {MACRO}")
    if start < 0 or "export_constant(MF_NOMAIL);" not in constants[start : start + 160]:
        raise AssertionError("MF_NOMAIL 腳本常量匯出缺失")

    message_file = (ROOT / "conf/msg_conf/map_msg.conf").read_text(encoding="utf-8-sig")
    if f"{MESSAGE_ID}: Mailbox and RODEX are disabled on this map." not in message_file:
        raise AssertionError("NoMail 地圖提示訊息缺失")

    mail = (ROOT / "src/map/mail.cpp").read_text(encoding="utf-8-sig")
    open_start = mail.index("int32 mail_openmail(")
    open_end = mail.index("void mail_deliveryfail(", open_start)
    open_body = mail[open_start:open_end]
    if f"#ifdef {MACRO}" not in open_body or "mail_invalid_operation(sd)" not in open_body:
        raise AssertionError("mail_openmail 未在開啟視窗前呼叫共用阻擋函式")

    clif = (ROOT / "src/map/clif.cpp").read_text(encoding="utf-8-sig")
    if clif.count("mail_invalid_operation(") < 8:
        raise AssertionError("郵件封包處理入口未完整沿用共用阻擋函式")


HARNESS = r'''#include <iostream>
struct block_list { int m; };
struct map_session_data { block_list bl; int fd; };
constexpr int MF_NOMAIL = 79;
constexpr int EXPECTED_MESSAGE = 1542;
int displayed_message_id = -1;

int map_getmapflag(int map_id, int flag) {
    if (flag != MF_NOMAIL) return 0;
    if (map_id == 2) return 1;
    if (map_id < 0) return -1;
    return 0;
}
const char* msg_txt(map_session_data*, int id) {
    displayed_message_id = id;
    return "NoMail mapflag message";
}
void clif_displaymessage(int, const char*) {}

bool mail_invalid_operation(map_session_data* sd) {
#ifdef Pandas_MapFlag_NoMail
@@PRODUCTION_CONDITION@@
#endif
    return false;
}
int main() {
    map_session_data normal_map{{1}, 10};
    map_session_data blocked_map{{2}, 11};
    map_session_data invalid_map{{-1}, 12};
    if (mail_invalid_operation(&normal_map)) return 1;
    if (displayed_message_id != -1) return 2;
#ifdef Pandas_MapFlag_NoMail
    if (!mail_invalid_operation(&blocked_map)) return 3;
    if (displayed_message_id != EXPECTED_MESSAGE) return 4;
    if (mail_invalid_operation(&invalid_map)) return 5;
#else
    if (mail_invalid_operation(&blocked_map)) return 6;
#endif
    std::cout << "NoMail mapflag checks passed\n";
    return 0;
}
'''


class NoMailMapFlagTest(unittest.TestCase):
    def test_source_contract(self) -> None:
        source_contract()
        self.assertIn("MF_NOMAIL", production_condition())

    def test_enabled_and_disabled_builds(self) -> None:
        condition = production_condition()
        harness = HARNESS.replace("@@PRODUCTION_CONDITION@@", condition)
        with tempfile.TemporaryDirectory(prefix="nomail-mapflag-") as temp:
            source = Path(temp) / "nomail.cpp"
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
                self.assertIn("NoMail mapflag checks passed", executed.stdout)


if __name__ == "__main__":
    unittest.main()
