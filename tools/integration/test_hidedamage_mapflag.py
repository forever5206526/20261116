"""Source-contract regression checks for the Pandas HideDamage mapflag."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CHECKS = (
    ("feature switch", "src/config/pandas.hpp", "#define Pandas_MapFlag_HideDamage"),
    ("mapflag enum", "src/map/map.hpp", "MF_HIDEDAMAGE,"),
    ("script constant export", "src/map/script_constants.hpp", "export_constant(MF_HIDEDAMAGE);"),
    ("normal damage packet hides both damage values", "src/map/clif.cpp", "p.damage = -div;\n\t\t\tp.damage2 = -div;"),
    ("legacy skill packet hides damage", "src/map/clif.cpp", "WBUFW(buf,28) = static_cast<uint16>(-div);"),
    ("modern skill packet hides damage", "src/map/clif.cpp", "WBUFW(buf,30) = static_cast<uint16>(-div);"),
    ("Windows CI step", ".github/workflows/windows-cloud-validation.yml", "test_hidedamage_mapflag.py"),
)


def main() -> None:
    failures = []
    for label, relative_path, expected in CHECKS:
        content = (ROOT / relative_path).read_text(encoding="utf-8")
        if expected not in content:
            failures.append(f"{label}: missing {expected!r} in {relative_path}")

    if failures:
        raise SystemExit("\n".join(failures))

    print(f"PASS: {len(CHECKS)} HideDamage source-contract checks")


if __name__ == "__main__":
    main()
