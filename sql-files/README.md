# SQL Imports

## 資料庫帳號安全設定（必讀）

本專案不再提供可直接登入的 MySQL 預設帳密。請勿使用遊戲玩家帳號作為資料庫帳號，也不要使用 MySQL 管理員帳號（例如 root）執行遊戲伺服器。

- `conf/inter_athena.conf` 的 `sql_user` 與 `sql_password` 預設留白，必須自行設定。
- 伺服器會拒絕空白帳密，以及公開的預設密碼 `ragnarok`；舊設定檔即使仍保留該密碼也無法通過連線檢查。
- 請使用專用資料庫帳號、唯一且足夠長的隨機密碼，並限制帳號只能從資料庫主機本機或指定的應用程式主機連線。
- 不要將真實密碼提交到 Git，也不要將 MySQL 帳號授權給任意來源主機（例如 `%`）。

### 建立專用資料庫帳號

以下範例假設遊戲資料庫名稱為 `ragnarok`，資料庫與遊戲伺服器位於同一台主機。請先以 MySQL 管理員執行，並將範例密碼換成自行產生的唯一隨機密碼（不可直接使用範例字串）：

```sql
CREATE USER 'brhades_srv'@'127.0.0.1'
  IDENTIFIED BY 'REPLACE_WITH_A_UNIQUE_RANDOM_PASSWORD';

GRANT SELECT, INSERT, UPDATE, DELETE
  ON `ragnarok`.*
  TO 'brhades_srv'@'127.0.0.1';
```

若 `log_db_db` 使用另一個資料庫（例如 `log`），也只對該資料庫授予伺服器實際需要的權限：

```sql
GRANT SELECT, INSERT, UPDATE, DELETE
  ON `log`.*
  TO 'brhades_srv'@'127.0.0.1';
```

接著將 `conf/inter_athena.conf` 設定為：

```ini
sql_user: brhades_srv
sql_password: 你自行產生的唯一隨機密碼
```

如果資料庫位於另一台主機，請將 MySQL 帳號的 Host 限制為該應用程式主機的固定 IP，並同步調整 `sql_host`；不要使用萬用 Host。資料表初次建立與升級需要的 DDL 權限，應由管理員另行執行，不應長期授予遊戲伺服器帳號。

### 處理舊的公開預設帳號

若曾經使用 `ragnarok/ragnarok`，請先查看資料庫實際存在的帳號與 Host：

```sql
SELECT User, Host
FROM mysql.user
WHERE User = 'ragnarok';
```

將查出的每個相關帳號逐一確認。若仍有服務使用，先替該帳號更換唯一密碼並收回不必要的全域權限；若已無服務使用，應在確認無相依服務後刪除該帳號。不要假設 Host 一定是 `localhost` 或 `127.0.0.1`，也不要在未檢查授權前直接刪除共用帳號。

## Explanation of SQL import files

The files in this directory are basic SQL table building scripts. The contained scripts are needed for initial installs as well as subsequent updates.

### New Install
---
For a new install, the following needs to be imported into the main schema:
Note: The schema name is defined in `conf/inter_athena.conf::map_server_db`.

* main.sql - Contains tables for normal server usage.
* web.sql - Contains tables for the web service
* roulette_default_data.sql - Contains data for the client's roulette game.

For a new install, the following can be imported into the main schema but is highly suggested to be imported into a separate schema for logs:
Note: The schema name is defined in `conf/inter_athena.conf::log_db_db`.

* logs.sql - Contains tables for logging of server events.

If your server is setup to read SQL database data, import the following into the main schema:
Note: If `conf/inter_athena.conf::use_sql_db` is set to yes continue with these imports else these can be skipped. Not all files have to be imported, only the ones that apply to the same mode as the server being ran.

* item_db.sql - Contains __pre-renewal__ item data table structure.
* item_db_equip.sql - Contains __pre-renewal__ equipment item data.
* item_db_etc.sql - Contains __pre-renewal__ etcetera item data.
* item_db2.sql - Contains __pre-renewal__ item data (import).
* item_db_re.sql - Contains __renewal__ item data table structure.
* item_db_re_equip.sql - Contains __renewal__ equipment item data.
* item_db_re_etc.sql - Contains __renewal__ etcetera item data.
* item_db_re_usable.sql - Contains __renewal__ usable item data.
* item_db_usable.sql - Contains __pre-renewal__ usable item data.
* item_db2_re.sql - Contains __renewal__ item data (import).
* mob_db.sql - Contains __pre-renewal__ mob data.
* mob_db2.sql - Contains __pre-renewal__ mob data (import).
* mob_db_re.sql - Contains __renewal__ mob data.
* mob_db2_re.sql - Contains __renewal__ mob data (import).
* mob_skill_db.sql - Contains __pre-renewal__ mob skill data.
* mob_skill_db2.sql - Contains __pre-renewal__ mob skill data (import).
* mob_skill_db_re.sql - Contains __renewal__ mob skill data.
* mob_skill_db2_re.sql - Contains __renewal__ mob skill data (import).

### Updates
---
Over the course of time new features and optimizations will take place. This may require SQL changes to happen. In the `upgrades` folder will be SQL files with an attached date.
These only have to executed one time if an update has occurred after the initial installation. It's possible to see when an update may be required when a SQL error will be displayed on the server console stating the format differs from what is required.

### Compatibility
---
The `compatibility` folder contains SQL views which are used with helping control panels or websites grab prevalent data for a table that may have changed structure.

These are optional imports but website data such as item databases will not work properly when using the new YAML format without these views:

* item_db_compat.sql - Creates a view for the item_db.
* item_db2_compat.sql - Creates a view for the item_db2 (import).
* item_db_re_compat.sql - Creates a view for the item_db_re.
* item_db2_re_compat.sql - Creates a view for the item_db2_re (import).

### Tools
---
The `tools` folder contains some simple adjustments if needed for an administrator's personal preferences.

* convert_engine_innodb.sql - Converts the SQL table engine setting to InnoDB.
* convert_engine_myiasm.sql - Converts the SQL table engine setting to MyISAM.
* convert_passwords.sql - Converts the login table's password value to MD5.

Useful tools for converting custom SQL items to TXT and then YAML. Please adjust the `INTO OUTFILE` in the query to a desired location.
To run these queries the user requires the [FILE](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_file) permission. It's also required to either [set or disable](https://computingforgeeks.com/how-to-solve-mysql-server-is-running-with-the-secure-file-priv-error/) the `secure-file-priv`. 

* item_db_re_to_txt.sql - Dumps the __renewal__ item data table to TXT format.
* item_db_to_txt.sql - Dumps the __pre-renewal__ item data table to TXT format.
* item_db2_re_to_txt.sql - Dumps the __renewal__ item data table (import) to TXT format.
* item_db2_to_txt.sql - Dumps the __pre-renewal__ item data table (import) to TXT format.

### Notes
---
The `web-server` must be able to read the `login` and `guild` tables from the `login-server` and `char-server`, respectively.
