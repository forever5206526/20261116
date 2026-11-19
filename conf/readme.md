# 匯入設定目錄

## import 目錄的用途是什麼？

`import/` 目錄可讓您修改設定，而不必直接變更主要的 `/conf/` 與 `/db/` 檔案。

只要將自訂設定放入這兩個位置中的 `import/` 目錄，更新伺服器時就不必處理核心檔案的衝突。您的變更會保留在匯入檔案中，其餘內容則可隨 rAthena 更新。

## 這個機制如何運作？

請將「import」理解為「覆寫」。只需將您已變更或想要覆寫的設定放入匯入檔案中。

例如，設定伺服器時，通常會有一些設定需要調整，才能符合您的需求。以下範例說明如何正確使用 `/conf/import/` 目錄。（`/db/import/` 的範例請參閱 [/db/readme.md](/db/readme.md)。）

### 登入伺服器
---
我們要使用 MD5 密碼，並停用 `_m/f` 帳號註冊方式。

#### /conf/import/login_conf.txt

	new_account: no
	use_MD5_passwords: yes


### 角色伺服器
---
我們要將伺服器名稱改為「Odin」。

#### /conf/import/char_conf.txt

	server_name: Odin


### 地圖伺服器
---
我們要隱藏所有錯誤訊息，並新增幾張自訂地圖。

#### /conf/import/map_conf.txt

	// 隱藏指定類型的訊息，讓伺服器輸出更精簡：
	//16：隱藏錯誤與 SQL 錯誤訊息。
	console_silent: 16
	map: 1@toy
	map: 1@valley
	map: shops


### 伺服器間設定
---
我們要使用 MySQL 資料表，而不是 .txt 檔案。

#### /conf/import/inter_conf.txt

	use_sql_db: yes


### 記錄設定
---
我們要記錄所有物品與所有聊天訊息。

#### /conf/import/log_conf.txt

	log_filter: 1
	// 記錄聊天訊息（全域、密語、隊伍、公會、主頻道、氏族）。（注意 3）
	// log_chat: 63 = 記錄所有聊天訊息
	log_chat: 63


### 戰鬥設定
---
我們要調整各種遊戲機制。原本應設定在 `/conf/battle/` 目錄中的項目，都可以放入 `import/battle_conf.txt`。為了方便辨識各項設定的來源，建議在每組設定前方以註解標示原始檔名。

#### /conf/import/battle_conf.txt

	// guild.conf
	guild_exp_limit: 90

	// items.conf
	vending_over_max: no
	vending_tax: 100
	weapon_produce_rate: 200
	potion_produce_rate: 200
	produce_item_name_input: 0x03

	// misc.conf
	duel_time_interval: 2
	at_mapflag: yes
	at_monsterignore: yes
	cashshop_show_points: yes
	hide_fav_sell: yes
	// 登入時是否顯示信箱狀態？
	// 預設值：0
	// 0 = 否
	// 1 = 是
	// 2 = 有未讀郵件時才顯示
	mail_show_status: 2

	// monster.conf
	show_mob_info: 3

	// party.conf
	party_hp_mode: 1
	display_party_name: yes

	// pet.conf
	pet_rename: yes

	// player.conf
	max_aspd: 196
	max_third_aspd: 196
	max_extended_aspd: 196
	vip_disp_rate: no

	// status.conf
	debuff_on_logout: 3


這個機制對所有使用者都非常有幫助。只要善用 `import/` 系統，大多數 Git 合併衝突都能避免。

## 繁體中文設定原則

本目錄中提供給管理者閱讀的說明、註解、範例與伺服器訊息統一使用繁體中文。為確保伺服器能正確讀取設定，下列內容保留程式要求的原始寫法，不翻譯其識別字或值：

- 設定鍵名、命令名稱、腳本函式、變數名稱與路徑。
- `yes/no`、`on/off`、數值、位元遮罩、IP 位址、連接埠及檔案名稱等程式接受的設定值。
- 客戶端封包名稱、技能／道具名稱及其他遊戲內固定識別字。

`msg_conf/` 中各語系檔名是相容性檔案名稱；其目前訊息內容使用相同的繁體中文訊息，不代表切換到其他語言。空白的匯入範本會保持空白，供管理者新增覆寫設定。
