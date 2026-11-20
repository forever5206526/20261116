@echo off
setlocal EnableExtensions DisableDelayedExpansion

set "SERVER_DIR=%~dp0"
if not exist "%SERVER_DIR%map-server.exe" (
    for %%I in ("%~dp0..") do set "SERVER_DIR=%%~fI"
)
if not exist "%SERVER_DIR%\map-server.exe" (
    echo ERROR: map-server.exe was not found beside this launcher or in its parent directory.
    endlocal & exit /b 1
)

set "SERV_BAT=%~dp0serv.bat"
if not exist "%SERV_BAT%" set "SERV_BAT=%~dp0tools\serv.bat"
if not exist "%SERV_BAT%" (
    echo ERROR: serv.bat was not found beside this launcher or in the tools directory.
    endlocal & exit /b 1
)

pushd "%SERVER_DIR%" >nul
if errorlevel 1 (
    echo ERROR: Unable to enter "%SERVER_DIR%".
    endlocal & exit /b 1
)
call "%SERV_BAT%" map-server.exe Map-Server %*
set "RUN_RESULT=%ERRORLEVEL%"
popd
endlocal & exit /b %RUN_RESULT%
