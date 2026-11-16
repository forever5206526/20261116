#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NoCapture mapflag alias regression tests."""

from __future__ import annotations

import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
MACRO = "Pandas_MapFlag_NoCapture"

HARNESS = r'''#include <iostream>

constexpr int MF_NOPETCAPTURE = 81;
#ifdef Pandas_MapFlag_NoCapture
constexpr int MF_NOCAPTURE = 82;
#endif

struct map_data {
    bool no_pet_capture = false;

    bool getMapFlag(int flag) const {
        if (flag == MF_NOPETCAPTURE) return no_pet_capture;
        return false;
    }

    void setMapFlag(int flag, bool status) {
        if (flag == MF_NOPETCAPTURE) no_pet_capture = status;
    }
};

int get_flag(map_data* mapdata, int mapflag) {
    switch (mapflag) {
#ifdef Pandas_MapFlag_NoCapture
@@GET_CASE@@
#endif
        default:
            return mapdata->getMapFlag(mapflag);
    }
}

void set_flag(map_data* mapdata, int mapflag, bool status) {
    switch (mapflag) {
#ifdef Pandas_MapFlag_NoCapture
@@SET_CASE@@
#endif
        default:
            mapdata->setMapFlag(mapflag, status);
            break;
    }
}

int main() {
    map_data map;
#ifdef Pandas_MapFlag_NoCapture
    if (get_flag(&map, MF_NOCAPTURE)) return 1;

    set_flag(&map, MF_NOCAPTURE, true);
    if (!map.no_pet_capture || !get_flag(&map, MF_NOCAPTURE)) return 2;

    set_flag(&map, MF_NOCAPTURE, false);
    if (map.no_pet_capture || get_flag(&map, MF_NOCAPTURE)) return 3;

    map.setMapFlag(MF_NOPETCAPTURE, true);
    if (!get_flag(&map, MF_NOCAPTURE)) return 4;
#else
    set_flag(&map, MF_NOPETCAPTURE, true);
    if (!map.no_pet_capture) return 5;
#endif
    std::cout << "NoCapture alias checks passed\n";
    return 0;
}
'''


def extract_production_cases() -> tuple[str, str]:
    source = (ROOT / "src/map/map.cpp").read_text(encoding="utf-8-sig")
    positions = []
    cursor = 0
    while True:
        pos = source.find("case MF_NOCAPTURE:", cursor)
        if pos < 0:
            break
        positions.append(pos)
        cursor = pos + 1

    if len(positions) != 2:
        raise AssertionError(
            f"map.cpp 應有兩個 MF_NOCAPTURE switch case，實際為 {len(positions)}"
        )

    get_case = source[positions[0]:source.index("case MF_SKILL_DAMAGE:", positions[0])]
    set_case = source[positions[1]:source.index("case MF_SKILL_DAMAGE:", positions[1])]

    if "return mapdata->getMapFlag(MF_NOPETCAPTURE);" not in get_case:
        raise AssertionError("NoCapture getter 未轉接 MF_NOPETCAPTURE")
    if "mapdata->setMapFlag(MF_NOPETCAPTURE, status);" not in set_case:
        raise AssertionError("NoCapture setter 未轉接 MF_NOPETCAPTURE")
    return get_case, set_case


class NoCaptureAliasTest(unittest.TestCase):
    def test_source_contract(self) -> None:
        config = (ROOT / "src/config/pandas.hpp").read_text(encoding="utf-8-sig")
        self.assertIn(f"#define {MACRO}", config)

        map_header = (ROOT / "src/map/map.hpp").read_text(encoding="utf-8-sig")
        self.assertIn("#ifdef Pandas_MapFlag_NoCapture\n\tMF_NOCAPTURE,", map_header)

        constants = (ROOT / "src/map/script_constants.hpp").read_text(encoding="utf-8-sig")
        self.assertIn("export_constant(MF_NOCAPTURE);", constants)

        get_case, set_case = extract_production_cases()
        self.assertIn("MF_NOPETCAPTURE", get_case)
        self.assertIn("MF_NOPETCAPTURE", set_case)

    def test_enabled_and_disabled_builds(self) -> None:
        get_case, set_case = extract_production_cases()
        source = HARNESS.replace("@@GET_CASE@@", get_case).replace("@@SET_CASE@@", set_case)

        with tempfile.TemporaryDirectory(prefix="nocapture-mapflag-") as temp:
            source_path = Path(temp) / "nocapture.cpp"
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
                self.assertIn("NoCapture alias checks passed", executed.stdout)


if __name__ == "__main__":
    unittest.main()
