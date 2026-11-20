"""Regression checks for Windows server launcher and service supervision."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> None:
    failures: list[str] = []
    launcher = (ROOT / "tools/runserver.bat").read_text(encoding="utf-8").casefold()

    require('if exist "%~dp0tools\\serv.bat" (' in launcher,
            "runserver.bat must detect the copied root launcher using tools\\serv.bat", failures)
    require('for %%i in ("%~dp0.") do set "server_dir=%%~fi"' in launcher,
            "runserver.bat must resolve the solution root when copied into that root", failures)
    require('for %%i in ("%~dp0..") do set "server_dir=%%~fi"' in launcher,
            "runserver.bat must resolve the solution root when run from tools", failures)
    require('for %%i in ("%~dp0.") do set "tools_dir=%%~fi"' in launcher,
            "runserver.bat must normalize its helper directory", failures)
    require('for %%i in ("%~dp0tools") do set "tools_dir=%%~fi"' in launcher,
            "runserver.bat must resolve tools when copied into the solution root", failures)
    require('pushd "%server_dir%"' in launcher and "popd" in launcher,
            "runserver.bat must enter the solution root and restore the caller directory", failures)
    require('echo server directory=%server_dir%' in launcher,
            "runserver.bat must report the resolved directory for diagnostics", failures)

    for service, filename in (
        ("login", "logserv.bat"),
        ("char", "charserv.bat"),
        ("web", "webserv.bat"),
        ("map", "mapserv.bat"),
    ):
        expected = f'start "{service} server" /d "%server_dir%" "%comspec%" /d /k call "%tools_dir%\\{filename}"'
        require(expected in launcher,
                f"{service}-server must start with a quoted helper path and solution-root working directory", failures)

    require("cd %source_dir%" not in launcher and "start cmd /k logserv.bat" not in launcher,
            "The old unquoted relative-path launcher commands must not return", failures)

    services = {
        "logserv.bat": ("login-server.exe", "Login-Server"),
        "charserv.bat": ("char-server.exe", "Char-Server"),
        "webserv.bat": ("web-server.exe", "Web-Server"),
        "mapserv.bat": ("map-server.exe", "Map-Server"),
    }
    for filename, (executable, title) in services.items():
        script = (ROOT / "tools" / filename).read_text(encoding="utf-8").casefold()
        require('set "server_dir=%~dp0"' in script,
                f"{filename} must support execution beside the binaries", failures)
        require(f'"%server_dir%\\{executable}' in script,
                f"{filename} must check for {executable} beside the launcher", failures)
        require('for %%i in ("%~dp0..") do set "server_dir=%%~fi"' in script,
                f"{filename} must also resolve binaries in the parent solution directory", failures)
        require('set "serv_bat=%~dp0serv.bat"' in script and
                'set "serv_bat=%~dp0tools\\serv.bat"' in script,
                f"{filename} must resolve serv.bat both from tools and from a copied root launcher", failures)
        require('pushd "%server_dir%"' in script and 'call "%serv_bat%"' in script and
                f" {executable} {title}".casefold() in script,
                f"{filename} must run its service helper from the binary directory", failures)

    workflow = (ROOT / ".github/workflows/windows-server-launcher.yml").read_text(encoding="utf-8").casefold()
    require("stop retry loop after normal startup failure" in workflow and
            "waitforexit(5000)" in workflow and
            "(echo exit 1& echo.)|call serv.bat cmd.exe fakeserver on" in workflow,
            "Windows CI must execute and time-limit the EXIT_FAILURE restart-loop regression test", failures)

    # Batch IF ERRORLEVEL checks are ranges, not exact equality checks.
    # Capture the process code and distinguish EXIT_FAILURE from crashes.
    supervisor = (ROOT / "tools/serv.bat").read_text(encoding="utf-8").casefold()
    require('set "server_exit_code=%errorlevel%"' in supervisor,
            "serv.bat must capture the service exit code before branching", failures)
    require('if "%server_exit_code%"=="1" goto exit1' in supervisor and
            'if not "%server_exit_code%"=="0" goto crashed' in supervisor,
            "serv.bat must distinguish EXIT_FAILURE from unexpected non-zero crash codes", failures)
    exit1_section = supervisor.split(":exit1", 1)[1].split(":crashed", 1)[0]
    crashed_section = supervisor.split(":crashed", 1)[1].split(":direct", 1)[0]
    require("goto end" in exit1_section and "goto restart_nt" not in exit1_section,
            "A normal EXIT_FAILURE must stop instead of entering the automatic restart loop", failures)
    require("goto restart_nt" in crashed_section,
            "Unexpected crashes must retain the configured automatic restart behavior", failures)

    if failures:
        raise SystemExit("\n".join(failures))
    print("PASS: Windows launchers resolve paths; normal startup failures stop; unexpected crashes may restart")


if __name__ == "__main__":
    main()
