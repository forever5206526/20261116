"""Regression checks for Windows server launcher path resolution."""

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
        require(f'"%server_dir%\\{executable}"' in script,
                f"{filename} must check for {executable} beside the launcher", failures)
        require('for %%i in ("%~dp0..") do set "server_dir=%%~fi"' in script,
                f"{filename} must also resolve binaries in the parent solution directory", failures)
        require('set "serv_bat=%~dp0serv.bat"' in script and
                'set "serv_bat=%~dp0tools\\serv.bat"' in script,
                f"{filename} must resolve serv.bat both from tools and from a copied root launcher", failures)
        require('pushd "%server_dir%"' in script and 'call "%serv_bat%"' in script and
                f" {executable} {title}".casefold() in script,
                f"{filename} must run its service helper from the binary directory", failures)

    if failures:
        raise SystemExit("\n".join(failures))
    print("PASS: both root and tools launchers resolve helpers and server directories")


if __name__ == "__main__":
    main()
