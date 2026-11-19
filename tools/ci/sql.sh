#!/usr/bin/env bash

function aborterror {
	echo "$@"
	exit 1
}

# Github Actions default login data
DB_ROOT=root
DB_ROOTPW=root
# Dedicated temporary MySQL account for the CI startup test.
# Never use the public ragnarok/ragnarok defaults in automated validation.
DB_HOST=127.0.0.1
DB_NAME=ragnarok
DB_USER=brhades_ci
DB_PASS="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')" || aborterror "Unable to generate a temporary SQL password."

# Pass the generated credentials to the later server-startup step without
# printing the password into the workflow log.
if [[ -n "${GITHUB_ENV:-}" ]]; then
	{
		printf 'BRHADES_SQL_USER=%s\\n' "$DB_USER"
		printf 'BRHADES_SQL_PASSWORD=%s\\n' "$DB_PASS"
	} >> "$GITHUB_ENV" || aborterror "Unable to export temporary SQL credentials to GitHub Actions."
fi

mysql -u "$DB_ROOT" -p"$DB_ROOTPW" -e "CREATE DATABASE $DB_NAME;" || aborterror "Unable to create database."
mysql -u "$DB_ROOT" -p"$DB_ROOTPW" "$DB_NAME" < sql-files/main.sql || aborterror "Unable to import main database."
mysql -u "$DB_ROOT" -p"$DB_ROOTPW" "$DB_NAME" < sql-files/logs.sql || aborterror "Unable to import logs database."
mysql -u "$DB_ROOT" -p"$DB_ROOTPW" "$DB_NAME" < sql-files/item_db.sql || aborterror "Unable to import pre-renewal item table structure."
mysql -u "$DB_ROOT" -p"$DB_ROOTPW" "$DB_NAME" < sql-files/item_db_usable.sql || aborterror "Unable to import pre-renewal usable item table."
mysql -u "$DB_ROOT" -p"$DB_ROOTPW" "$DB_NAME" < sql-files/item_db_equip.sql || aborterror "Unable to import pre-renewal equip item table."
mysql -u "$DB_ROOT" -p"$DB_ROOTPW" "$DB_NAME" < sql-files/item_db_etc.sql || aborterror "Unable to import pre-renewal etc item table."
mysql -u "$DB_ROOT" -p"$DB_ROOTPW" "$DB_NAME" < sql-files/item_db2.sql || aborterror "Unable to import pre-renewal item 2 table."
mysql -u "$DB_ROOT" -p"$DB_ROOTPW" "$DB_NAME" < sql-files/item_db_re.sql || aborterror "Unable to import renewal item table structure."
mysql -u "$DB_ROOT" -p"$DB_ROOTPW" "$DB_NAME" < sql-files/item_db_re_usable.sql || aborterror "Unable to import renewal usable item table."
mysql -u "$DB_ROOT" -p"$DB_ROOTPW" "$DB_NAME" < sql-files/item_db_re_equip.sql || aborterror "Unable to import renewal equip item table."
mysql -u "$DB_ROOT" -p"$DB_ROOTPW" "$DB_NAME" < sql-files/item_db_re_etc.sql || aborterror "Unable to import renewal etc item table."
mysql -u "$DB_ROOT" -p"$DB_ROOTPW" "$DB_NAME" < sql-files/item_db2_re.sql || aborterror "Unable to import renewal item 2 table."
mysql -u "$DB_ROOT" -p"$DB_ROOTPW" "$DB_NAME" < sql-files/mob_db.sql || aborterror "Unable to import pre-renewal monster table."
mysql -u "$DB_ROOT" -p"$DB_ROOTPW" "$DB_NAME" < sql-files/mob_db2.sql || aborterror "Unable to import pre-renewal monster 2 table."
mysql -u "$DB_ROOT" -p"$DB_ROOTPW" "$DB_NAME" < sql-files/mob_db_re.sql || aborterror "Unable to import renewal monster table."
mysql -u "$DB_ROOT" -p"$DB_ROOTPW" "$DB_NAME" < sql-files/mob_db2_re.sql || aborterror "Unable to import renewal monster 2 table."
mysql -u "$DB_ROOT" -p"$DB_ROOTPW" "$DB_NAME" < sql-files/mob_skill_db.sql || aborterror "Unable to import pre-renewal monster skill table."
mysql -u "$DB_ROOT" -p"$DB_ROOTPW" "$DB_NAME" < sql-files/mob_skill_db2.sql || aborterror "Unable to import pre-renewal monster skill 2 table."
mysql -u "$DB_ROOT" -p"$DB_ROOTPW" "$DB_NAME" < sql-files/mob_skill_db_re.sql || aborterror "Unable to import renewal monster skill table."
mysql -u "$DB_ROOT" -p"$DB_ROOTPW" "$DB_NAME" < sql-files/mob_skill_db2_re.sql || aborterror "Unable to import renewal monster skill 2 table."
mysql -u "$DB_ROOT" -p"$DB_ROOTPW" "$DB_NAME" < sql-files/roulette_default_data.sql || aborterror "Unable to import roulette table."

# Select the account-creation syntax supported by the installed server.
DB_VERSION=$(mysql -N -s -u "$DB_ROOT" -p"$DB_ROOTPW" -e "SELECT VERSION();") || aborterror "Unable to detect database server version."
if [[ "$DB_VERSION" == *MariaDB* ]]; then
	mysql -u "$DB_ROOT" -p"$DB_ROOTPW" -e "SET old_passwords=0; CREATE USER '$DB_USER'@'$DB_HOST' IDENTIFIED BY '$DB_PASS';" || aborterror "Unable to create MariaDB database user."
else
	mysql -u "$DB_ROOT" -p"$DB_ROOTPW" -e "CREATE USER '$DB_USER'@'$DB_HOST' IDENTIFIED WITH mysql_native_password BY '$DB_PASS';" || aborterror "Unable to create MySQL database user."
fi

mysql -u "$DB_ROOT" -p"$DB_ROOTPW" -e "GRANT SELECT,INSERT,UPDATE,DELETE ON $DB_NAME.* TO '$DB_USER'@'$DB_HOST';" || aborterror "Unable to grant database privileges."
