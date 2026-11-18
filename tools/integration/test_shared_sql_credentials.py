"""Regression checks for shared MySQL connection settings."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> None:
    failures: list[str] = []

    sql_hpp = read("src/common/sql.hpp")
    sql_cpp = read("src/common/sql.cpp")
    require("bool Sql_ConfigRead(const char* key, const char* value);" in sql_hpp,
            "shared SQL parser declaration is missing", failures)
    require("void Sql_ConfigApply(std::string& host, uint16& port" in sql_hpp,
            "uint16 shared SQL apply declaration is missing", failures)
    require("void Sql_ConfigApply(std::string& host, int32& port" in sql_hpp,
            "int32 shared SQL apply declaration is missing", failures)
    for key in ("sql_host", "sql_port", "sql_user", "sql_password", "sql_codepage"):
        require(f'"{key}"' in sql_cpp, f"common SQL parser does not recognize {key}", failures)
    for legacy_key in ("default_codepage", "login_codepage", "ipban_codepage", "log_codepage"):
        require(f'"{legacy_key}"' in sql_cpp,
                f"legacy {legacy_key} configuration is not mapped to the shared codepage", failures)

    # MySQL error 1045 is the authentication-rejection signal. Keep its warning
    # explicit, avoid printing the password, and still fail the connection.
    try:
        connect_start = sql_cpp.index("int32 Sql_Connect(")
        connect_section = sql_cpp[connect_start:sql_cpp.index("/// Retrieves the timeout", connect_start)]
    except ValueError:
        connect_section = ""
        failures.append("could not isolate Sql_Connect authentication handling")
    require("error_code == 1045" in connect_section,
            "Sql_Connect does not detect MySQL access-denied error 1045", failures)
    require("database username or password is incorrect" in connect_section,
            "Sql_Connect does not show a clear incorrect-credentials warning", failures)
    require("sql_user and sql_password" in connect_section,
            "authentication warning does not point to the shared credential settings", failures)
    require("return SQL_ERROR;" in connect_section,
            "Sql_Connect must reject the connection after authentication failure", failures)
    require("mysql_error(&self->handle)" in connect_section,
            "Sql_Connect must preserve the original diagnostic for other connection errors", failures)
    require("sql_config_codepage_set && !sql_config_codepage.empty()" in connect_section,
            "Sql_Connect does not apply the configured shared codepage", failures)
    require("Sql_SetEncoding(self, sql_config_codepage.c_str())" in connect_section,
            "shared codepage is not applied centrally to each SQL connection", failures)

    parser_files = (
        "src/login/login.cpp",
        "src/char/inter.cpp",
        "src/map/map.cpp",
        "src/web/web.cpp",
    )
    for path in parser_files:
        require("Sql_ConfigRead(w1, w2)" in read(path),
                f"{path} does not read shared SQL settings", failures)

    connection_modules = (
        "src/login/account.cpp",
        "src/login/ipban.cpp",
        "src/login/loginlog.cpp",
        "src/char/inter.cpp",
        "src/map/map.cpp",
        "src/web/web.cpp",
    )
    for path in connection_modules:
        source = read(path)
        require("Sql_SetEncoding(" not in source,
                f"{path} still applies a service-specific codepage instead of the shared setting", failures)
        require("default_codepage" not in source and "ipban_codepage" not in source and "log_codepage" not in source,
                f"{path} still stores a separate codepage value", failures)

    # Verify every distinct SQL connection initializer applies the shared
    # settings before opening the connection, including the Web server's four DBs.
    connection_functions = (
        ("src/login/account.cpp", "static bool account_db_sql_init(AccountDB* self) {", "static void account_db_sql_destroy(AccountDB* self){", 1),
        ("src/login/ipban.cpp", "void ipban_init(void)", "void ipban_final(void)", 1),
        ("src/login/loginlog.cpp", "bool loginlog_init(void)", "bool loginlog_final(void)", 1),
        ("src/char/inter.cpp", "int32 inter_init_sql(", "void inter_final(", 1),
        ("src/map/map.cpp", "int32 map_sql_init(void)", "int32 map_sql_close(void)", 1),
        ("src/map/map.cpp", "int32 log_sql_init(void)", "void map_remove_questinfo(", 1),
        ("src/web/web.cpp", "int32 web_sql_init(void)", "int32 web_sql_close(void)", 4),
    )
    for path, start, end, expected in connection_functions:
        source = read(path)
        try:
            section = source[source.index(start):source.index(end, source.index(start))]
        except ValueError:
            failures.append(f"could not isolate SQL initializer in {path}: {start}")
            continue
        apply_positions = [m.start() for m in re.finditer(r"Sql_ConfigApply\(", section)]
        connect_positions = [m.start() for m in re.finditer(r"Sql_Connect\(", section)]
        require(len(apply_positions) == expected,
                f"{path} {start}: expected {expected} shared-credential apply call(s), got {len(apply_positions)}",
                failures)
        require(len(connect_positions) == expected if path != "src/map/map.cpp" or start != "int32 map_sql_init(void)" else len(connect_positions) == 2,
                f"{path} {start}: unexpected number of SQL connections ({len(connect_positions)})",
                failures)
        if expected == 1:
            require(bool(apply_positions) and bool(connect_positions) and apply_positions[0] < connect_positions[0],
                    f"{path} {start}: shared credentials are not applied before Sql_Connect", failures)
        elif path == "src/web/web.cpp":
            require(len(apply_positions) == len(connect_positions) and
                    all(a < c for a, c in zip(apply_positions, connect_positions)),
                    "Web DB connections must each apply the shared credentials before connecting", failures)
        require("return false" in section or "exit(EXIT_FAILURE)" in section,
                f"{path} {start}: failed SQL authentication must block service initialization", failures)

    config = read("conf/inter_athena.conf")
    configured_keys = re.findall(r"^\s*(sql_(?:host|port|user|password|codepage))\s*:", config, re.MULTILINE)
    require(sorted(configured_keys) == sorted(["sql_host", "sql_port", "sql_user", "sql_password", "sql_codepage"]),
            "inter_athena.conf must define each shared SQL setting exactly once", failures)
    codepage_keys = re.findall(r"^\s*([a-z_]*codepage)\s*:", config, re.MULTILINE)
    require(codepage_keys == ["sql_codepage"],
            f"database codepage must be configured once, found {codepage_keys}", failures)
    legacy_active = re.findall(
        r"^(?!\s*//)\s*(?:login_server|ipban_db|char_server|map_server|web_server|log_db)_(?:ip|port|id|pw)\s*:",
        config,
        re.MULTILINE,
    )
    require(not legacy_active,
            "inter_athena.conf still contains duplicated active per-service credentials", failures)

    for key in ("login_server_db:", "ipban_db_db:", "char_server_db:", "map_server_db:",
                "web_server_db:", "log_db_db:", "log_login_db:"):
        require(key in config, f"per-service database/schema setting {key} was lost", failures)

    for path in ("conf/char_athena.conf", "conf/map_athena.conf"):
        conf = read(path)
        require(re.search(r"^userid:\s*s1\s*$", conf, re.MULTILINE) is not None,
                f"{path} must preserve inter-server userid s1", failures)
        require(re.search(r"^passwd:\s*p1\s*$", conf, re.MULTILINE) is not None,
                f"{path} must preserve inter-server password p1", failures)

    if failures:
        raise SystemExit("\n".join(failures))

    print("PASS: shared MySQL credentials and codepage, connection coverage, schema separation and legacy compatibility")


if __name__ == "__main__":
    main()
