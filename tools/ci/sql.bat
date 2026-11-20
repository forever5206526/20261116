@echo off
setlocal EnableExtensions DisableDelayedExpansion

rem MySQL database setup
if not defined MYSQL set "MYSQL=mysql"
for %%V in (DB_ROOT DB_NAME DB_USER DB_HOST DB_USERPW) do (
    if not defined %%V (
        echo ERROR: Required environment variable %%V is not set.
        endlocal & exit /b 1
    )
)
rem Use the MYSQL_PWD environment variable to avoid exposing the root password in arguments.
set "MYSQL_PWD=%DB_ROOTPW%"
%MYSQL% -u "%DB_ROOT%" -e "CREATE DATABASE IF NOT EXISTS `%DB_NAME%`;"
if errorlevel 1 goto :sql_error
%MYSQL% -u "%DB_ROOT%" "%DB_NAME%" -e "source sql-files\main.sql"
if errorlevel 1 goto :sql_error
%MYSQL% -u "%DB_ROOT%" "%DB_NAME%" -e "source sql-files\logs.sql"
if errorlevel 1 goto :sql_error
%MYSQL% -u "%DB_ROOT%" "%DB_NAME%" -e "source sql-files\item_db.sql"
if errorlevel 1 goto :sql_error
%MYSQL% -u "%DB_ROOT%" "%DB_NAME%" -e "source sql-files\item_db_usable.sql"
if errorlevel 1 goto :sql_error
%MYSQL% -u "%DB_ROOT%" "%DB_NAME%" -e "source sql-files\item_db_equip.sql"
if errorlevel 1 goto :sql_error
%MYSQL% -u "%DB_ROOT%" "%DB_NAME%" -e "source sql-files\item_db_etc.sql"
if errorlevel 1 goto :sql_error
%MYSQL% -u "%DB_ROOT%" "%DB_NAME%" -e "source sql-files\item_db2.sql"
if errorlevel 1 goto :sql_error
%MYSQL% -u "%DB_ROOT%" "%DB_NAME%" -e "source sql-files\item_db_re.sql"
if errorlevel 1 goto :sql_error
%MYSQL% -u "%DB_ROOT%" "%DB_NAME%" -e "source sql-files\item_db_re_usable.sql"
if errorlevel 1 goto :sql_error
%MYSQL% -u "%DB_ROOT%" "%DB_NAME%" -e "source sql-files\item_db_re_equip.sql"
if errorlevel 1 goto :sql_error
%MYSQL% -u "%DB_ROOT%" "%DB_NAME%" -e "source sql-files\item_db_re_etc.sql"
if errorlevel 1 goto :sql_error
%MYSQL% -u "%DB_ROOT%" "%DB_NAME%" -e "source sql-files\item_db2_re.sql"
if errorlevel 1 goto :sql_error
%MYSQL% -u "%DB_ROOT%" "%DB_NAME%" -e "source sql-files\mob_db.sql"
if errorlevel 1 goto :sql_error
%MYSQL% -u "%DB_ROOT%" "%DB_NAME%" -e "source sql-files\mob_db2.sql"
if errorlevel 1 goto :sql_error
%MYSQL% -u "%DB_ROOT%" "%DB_NAME%" -e "source sql-files\mob_db_re.sql"
if errorlevel 1 goto :sql_error
%MYSQL% -u "%DB_ROOT%" "%DB_NAME%" -e "source sql-files\mob_db2_re.sql"
if errorlevel 1 goto :sql_error
%MYSQL% -u "%DB_ROOT%" "%DB_NAME%" -e "source sql-files\mob_skill_db.sql"
if errorlevel 1 goto :sql_error
%MYSQL% -u "%DB_ROOT%" "%DB_NAME%" -e "source sql-files\mob_skill_db2.sql"
if errorlevel 1 goto :sql_error
%MYSQL% -u "%DB_ROOT%" "%DB_NAME%" -e "source sql-files\mob_skill_db_re.sql"
if errorlevel 1 goto :sql_error
%MYSQL% -u "%DB_ROOT%" "%DB_NAME%" -e "source sql-files\mob_skill_db2_re.sql"
if errorlevel 1 goto :sql_error
%MYSQL% -u "%DB_ROOT%" "%DB_NAME%" -e "source sql-files\roulette_default_data.sql"
if errorlevel 1 goto :sql_error

rem Detect the database server so MariaDB and MySQL use their supported account syntax.
for /f "delims=" %%V in ('%MYSQL% -N -s -u "%DB_ROOT%" -e "SELECT VERSION();" 2^>NUL') do set "DB_VERSION=%%V"
if not defined DB_VERSION goto :sql_error
echo(%DB_VERSION%| findstr /I "MariaDB" >nul
if not errorlevel 1 (
    %MYSQL% -u "%DB_ROOT%" -e "SET old_passwords=0; CREATE USER IF NOT EXISTS '%DB_USER%'@'%DB_HOST%' IDENTIFIED BY '%DB_USERPW%';"
    if errorlevel 1 goto :sql_error
    %MYSQL% -u "%DB_ROOT%" -e "ALTER USER '%DB_USER%'@'%DB_HOST%' IDENTIFIED BY '%DB_USERPW%';"
) else (
    %MYSQL% -u "%DB_ROOT%" -e "CREATE USER IF NOT EXISTS '%DB_USER%'@'%DB_HOST%' IDENTIFIED WITH mysql_native_password BY '%DB_USERPW%';"
    if errorlevel 1 goto :sql_error
    %MYSQL% -u "%DB_ROOT%" -e "ALTER USER '%DB_USER%'@'%DB_HOST%' IDENTIFIED WITH mysql_native_password BY '%DB_USERPW%';"
)
if errorlevel 1 goto :sql_error

rem Create the account separately; GRANT only assigns privileges on the game database.
%MYSQL% -u "%DB_ROOT%" -e "GRANT SELECT,INSERT,UPDATE,DELETE ON `%DB_NAME%`.* TO '%DB_USER%'@'%DB_HOST%';"
if errorlevel 1 goto :sql_error

echo MySQL database import and account setup completed successfully.
set "MYSQL_PWD="
endlocal & exit /b 0

:sql_error
set "MYSQL_PWD="
echo ERROR: MySQL database import or account setup failed. See the MySQL diagnostic above.
endlocal & exit /b 1
