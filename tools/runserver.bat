@echo off
setlocal EnableExtensions DisableDelayedExpansion

for %%I in ("%~dp0.") do set "TOOLS_DIR=%%~fI"
if exist "%~dp0tools\serv.bat" (
    for %%I in ("%~dp0.") do set "SERVER_DIR=%%~fI"
    for %%I in ("%~dp0tools") do set "TOOLS_DIR=%%~fI"
) else (
    for %%I in ("%~dp0..") do set "SERVER_DIR=%%~fI"
)

pushd "%SERVER_DIR%" >nul
if errorlevel 1 (
    echo ERROR: Unable to enter the server directory "%SERVER_DIR%".
    endlocal & exit /b 1
)

if "%~1"=="" (set "target=watch") else set "target=%~1"
echo target=%target%
echo server directory=%SERVER_DIR%

REM Keep service state variables independent from localized tasklist output.
set "login_running=false"
set "char_running=false"
set "web_running=false"
set "map_running=false"

if "%target%"=="status" (
    call :getStatus
) else if "%target%"=="watch" (
    call :Watch
) else if "%target%"=="stop" (
    call :Stop
) else if "%target%"=="start" (
    call :Start
) else (
    echo Usage: runserver.bat [start^|watch^|stop^|status]
)

goto :cleanup

:Stop
echo Stopping all servers.
call :stopLogin
call :stopChar
call :stopWeb
call :stopMap
goto :EOF

:Watch
echo Starting all servers in restart mode.
set "restart_mode=on"
call :startLogin
call :startChar
call :startWeb
call :startMap
goto :EOF

:Start
echo Starting all servers without automatic restart.
set "restart_mode=off"
call :startLogin
call :startChar
call :startWeb
call :startMap
goto :EOF

:getStatus
echo Getting status of all servers.
call :getLoginStatus
call :getCharStatus
call :getWebStatus
call :getMapStatus

if "%login_running%"=="false" (
    echo login-server is not running.
) else (
    echo login-server is running. PID=%LoginServPID%
)
if "%char_running%"=="false" (
    echo char-server is not running.
) else (
    echo char-server is running. PID=%CharServPID%
)
if "%web_running%"=="false" (
    echo web-server is not running.
) else (
    echo web-server is running. PID=%WebServPID%
)
if "%map_running%"=="false" (
    echo map-server is not running.
) else (
    echo map-server is running. PID=%MapServPID%
)
goto :EOF

REM Stop service helpers.
:stopLogin
call :getLoginStatus
if "%login_running%"=="true" taskkill /PID %LoginServPID% /F
goto :EOF

:stopChar
call :getCharStatus
if "%char_running%"=="true" taskkill /PID %CharServPID% /F
goto :EOF

:stopWeb
call :getWebStatus
if "%web_running%"=="true" taskkill /PID %WebServPID% /F
goto :EOF

:stopMap
call :getMapStatus
if "%map_running%"=="true" taskkill /PID %MapServPID% /F
goto :EOF

REM Start helpers always use the executable directory as their working directory.
:startLogin
call :getLoginStatus
if "%login_running%"=="false" (
    start "Login Server" /D "%SERVER_DIR%" "%ComSpec%" /D /K call "%TOOLS_DIR%\logserv.bat" %restart_mode%
) else (
    echo Login server is already running. PID=%LoginServPID%
)
goto :EOF

:startChar
call :getCharStatus
if "%char_running%"=="false" (
    start "Char Server" /D "%SERVER_DIR%" "%ComSpec%" /D /K call "%TOOLS_DIR%\charserv.bat" %restart_mode%
) else (
    echo Char server is already running. PID=%CharServPID%
)
goto :EOF

:startWeb
call :getWebStatus
if "%web_running%"=="false" (
    start "Web Server" /D "%SERVER_DIR%" "%ComSpec%" /D /K call "%TOOLS_DIR%\webserv.bat" %restart_mode%
) else (
    echo Web server is already running. PID=%WebServPID%
)
goto :EOF

:startMap
call :getMapStatus
if "%map_running%"=="false" (
    start "Map Server" /D "%SERVER_DIR%" "%ComSpec%" /D /K call "%TOOLS_DIR%\mapserv.bat" %restart_mode%
) else (
    echo Map server is already running. PID=%MapServPID%
)
goto :EOF

REM Process status helpers.
:getLoginStatus
set "LoginServPID="
for /F "TOKENS=1,2,*" %%a in ('tasklist /FI "IMAGENAME eq login-server.exe"') do set "LoginServPID=%%b"
echo(%LoginServPID%|findstr "^[-][1-9][0-9]*$ ^[1-9][0-9]*$ ^0$">nul && set "login_running=true" || set "login_running=false"
goto :EOF

:getCharStatus
set "CharServPID="
for /F "TOKENS=1,2,*" %%a in ('tasklist /FI "IMAGENAME eq char-server.exe"') do set "CharServPID=%%b"
echo(%CharServPID%|findstr "^[-][1-9][0-9]*$ ^[1-9][0-9]*$ ^0$">nul && set "char_running=true" || set "char_running=false"
goto :EOF

:getWebStatus
set "WebServPID="
for /F "TOKENS=1,2,*" %%a in ('tasklist /FI "IMAGENAME eq web-server.exe"') do set "WebServPID=%%b"
echo(%WebServPID%|findstr "^[-][1-9][0-9]*$ ^[1-9][0-9]*$ ^0$">nul && set "web_running=true" || set "web_running=false"
goto :EOF

:getMapStatus
set "MapServPID="
for /F "TOKENS=1,2,*" %%a in ('tasklist /FI "IMAGENAME eq map-server.exe"') do set "MapServPID=%%b"
echo(%MapServPID%|findstr "^[-][1-9][0-9]*$ ^[1-9][0-9]*$ ^0$">nul && set "map_running=true" || set "map_running=false"
goto :EOF

:cleanup
if "%target%"=="status" (
    set "RESULT=0"
) else (
    set "RESULT=%ERRORLEVEL%"
)
popd
endlocal & exit /b %RESULT%
