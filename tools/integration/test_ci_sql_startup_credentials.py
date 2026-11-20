"""Regression checks for temporary database credentials used by Windows startup CI."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> None:
    failures: list[str] = []
    sql = (ROOT / "tools/ci/sql.sh").read_text(encoding="utf-8")
    workflow = (ROOT / ".github/workflows/npc_db_validation.yml").read_text(encoding="utf-8")
    config = (ROOT / "conf/inter_athena.conf").read_text(encoding="utf-8")

    sql_lines = sql.splitlines()
    config_lines = config.splitlines()
    require("DB_HOST=127.0.0.1" in sql_lines,
            "CI database user host must match sql_host 127.0.0.1", failures)
    require("DB_USER=brhades_ci" in sql_lines,
            "CI must use a dedicated account instead of the blocked ragnarok default", failures)
    require("DB_PASS=\"$(python -c 'import secrets; print(secrets.token_urlsafe(32))')\"" in sql,
            "CI database password must be randomly generated", failures)
    require('echo "BRHADES_SQL_USER=$DB_USER"' in sql and
            '>> "$GITHUB_ENV"' in sql,
            "CI SQL username is not exported to the startup job", failures)
    require('echo "BRHADES_SQL_PASSWORD=$DB_PASS"' in sql,
            "CI SQL password is not exported to the startup job", failures)
    require("CREATE USER '$DB_USER'@'$DB_HOST'" in sql and
            "GRANT SELECT,INSERT,UPDATE,DELETE ON $DB_NAME.* TO '$DB_USER'@'$DB_HOST'" in sql,
            "CI SQL account is not created and granted database access", failures)

    import_step = workflow.find("- name: Import database schema and seed data")
    configure_step = workflow.find("- name: Configure temporary SQL credentials for server startup validation")
    startup_step = workflow.find("- name: Run map-server NPC and database startup validation")
    require(-1 not in (import_step, configure_step, startup_step) and
            import_step < configure_step < startup_step,
            "Temporary credentials must be injected after DB creation and before server startup", failures)
    require("$env:BRHADES_SQL_USER" in workflow and "$env:BRHADES_SQL_PASSWORD" in workflow,
            "Startup workflow does not consume the generated CI credentials", failures)
    require("(?m)^sql_user:" in workflow and "(?m)^sql_password:" in workflow and
            "[System.IO.File]::WriteAllText($configPath, $content" in workflow,
            "Startup workflow does not write both shared SQL values to the test config", failures)
    require("ragnarok/ragnarok" not in workflow,
            "The blocked public default credentials must not be used in startup CI", failures)
    require(any(line.startswith("sql_user:") and line == "sql_user:" for line in config_lines) and
            any(line.startswith("sql_password:") and line == "sql_password:" for line in config_lines),
            "The tracked sample config must remain free of CI credentials", failures)

    # The root password is consumed through MYSQL_PWD and must never silently default to empty.
    batch = (ROOT / "tools/ci/sql.bat").read_text(encoding="utf-8")
    require("for %%V in (DB_ROOT DB_ROOTPW DB_NAME DB_USER DB_HOST DB_USERPW) do (" in batch,
            "Windows SQL helper must reject a missing DB_ROOTPW before trying root authentication", failures)
    require('set "MYSQL_PWD=%DB_ROOTPW%"' in batch,
            "Windows SQL helper must pass the required root password through MYSQL_PWD", failures)

    batch_create = batch.find("CREATE USER IF NOT EXISTS")
    batch_grant = batch.find("GRANT SELECT,INSERT,UPDATE,DELETE")
    grant_line = next((line for line in batch.splitlines() if "GRANT SELECT,INSERT,UPDATE,DELETE" in line), "")
    require(batch_create >= 0 and batch_grant > batch_create,
            "Windows SQL helper must create the account before granting privileges", failures)
    require("IDENTIFIED BY" not in grant_line,
            "Windows SQL helper must not use removed GRANT ... IDENTIFIED BY syntax", failures)
    require("ALTER USER" in batch and "IDENTIFIED WITH mysql_native_password BY" in batch and
            "SET old_passwords=0" in batch,
            "Windows SQL helper must update existing accounts with MySQL/MariaDB-compatible syntax", failures)
    require(batch.count("if errorlevel 1 goto :sql_error") >= 24 and
            ":sql_error" in batch and "endlocal & exit /b 1" in batch,
            "Windows SQL helper must stop at the first SQL error and return a failure code", failures)

    require("Validate Windows SQL batch helper against MySQL 8" in workflow and
            "call tools\\ci\\sql.bat" in workflow and
            "ragnarok_batch_test" in workflow and "SHOW GRANTS FOR" in workflow,
            "The Windows SQL batch helper must be exercised against a live MySQL instance", failures)

    if failures:
        raise SystemExit("\n".join(failures))
    print("PASS: startup CI uses a temporary non-default MySQL account without storing credentials in the repository")


if __name__ == "__main__":
    main()
