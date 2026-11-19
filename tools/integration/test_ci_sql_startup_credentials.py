"""Regression checks for temporary database credentials used by Windows startup CI."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> None:
    failures: list[str] = []
    sql = (ROOT / "tools/ci/sql.sh").read_text(encoding="utf-8")
    workflow = (ROOT / ".github/workflows/npc_db_validation.yml").read_text(encoding="utf-8")
    config = (ROOT / "conf/inter_athena.conf").read_text(encoding="utf-8")

    require(re.search(r"^DB_HOST=127\\.0\\.0\\.1$", sql, re.MULTILINE) is not None,
            "CI database user host must match sql_host 127.0.0.1", failures)
    require(re.search(r"^DB_USER=brhades_ci$", sql, re.MULTILINE) is not None,
            "CI must use a dedicated account instead of the blocked ragnarok default", failures)
    require("DB_PASS=\"$(python -c 'import secrets; print(secrets.token_urlsafe(32))')\"" in sql,
            "CI database password must be randomly generated", failures)
    require('echo "BRHADES_SQL_USER=$DB_USER" >> "$GITHUB_ENV"' in sql or
            'echo "BRHADES_SQL_USER=$DB_USER"' in sql,
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
    require("sql_user:" in workflow and "sql_password:" in workflow and
            "[System.IO.File]::WriteAllText($configPath, $content" in workflow,
            "Startup workflow does not write both shared SQL values to the test config", failures)
    require("ragnarok/ragnarok" not in workflow,
            "The blocked public default credentials must not be used in startup CI", failures)
    require(re.search(r"^sql_user:\\s*$", config, re.MULTILINE) is not None and
            re.search(r"^sql_password:\\s*$", config, re.MULTILINE) is not None,
            "The tracked sample config must remain free of CI credentials", failures)

    if failures:
        raise SystemExit("\\n".join(failures))
    print("PASS: startup CI uses a temporary non-default MySQL account without storing credentials in the repository")


if __name__ == "__main__":
    main()
