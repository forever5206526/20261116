from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> None:
    failures: list[str] = []
    config = read("src/config/pandas.hpp")
    clif = read("src/map/clif.cpp")
    enum = read("src/map/map.hpp")
    constants = read("src/map/script_constants.hpp")
    readme = read("README.md")
    workflow = read(".github/workflows/windows-cloud-validation.yml")

    require(config.count("#define Pandas_MapFlag_NoBank") == 1,
            "Pandas_MapFlag_NoBank must be enabled exactly once", failures)
    require("MF_NOBANK," in enum and "export_constant(MF_NOBANK);" in constants,
            "NoBank must continue to use the native mapflag enum and script constant", failures)

    start = clif.find("void clif_parse_BankOpen")
    end = clif.find("// 09B9", start)
    require(start >= 0 and end > start,
            "BankOpen packet handler boundary must be present", failures)
    handler = clif[start:end] if start >= 0 and end > start else ""
    expected = """if( map_getmapflag( sd->bl.m, MF_NOBANK ) ){
#ifdef Pandas_MapFlag_NoBank
\t\tclif_messagecolor( &sd->bl, color_table[COLOR_RED], msg_txt( sd, 831 ), false, SELF ); // You cannot use the Bank on this map.
#else
\t\tclif_displaymessage( sd->fd, msg_txt( sd, 831 ) );
#endif // Pandas_MapFlag_NoBank
\t\treturn;
\t}"""
    require(expected in handler,
            "NoBank must show the native map restriction message using the red message color when the Pandas switch is enabled, preserving the legacy fallback", failures)
    require(handler.find("MF_NOBANK") < handler.find("sd->state.banking = 1") and
            handler.find("return;") < handler.find("sd->state.banking = 1"),
            "A map restricted by MF_NOBANK must return before enabling banking", failures)
    require("run: python tools/integration/test_nobank_mapflag.py" in workflow,
            "Windows cloud validation must execute the NoBank regression test", failures)
    require("### NoBank 地圖標記提示" in readme and
            "紅色訊息框" in readme and
            'setmapflag "prontera", MF_NOBANK;' in readme and
            'removemapflag "prontera", MF_NOBANK;' in readme,
            "README must explain the native restriction and provide set/remove examples", failures)

    if failures:
        raise SystemExit("\n".join(failures))
    print("PASS: NoBank native restriction, red-message UX, fallback branch, banking early return, docs, and workflow")


if __name__ == "__main__":
    main()
