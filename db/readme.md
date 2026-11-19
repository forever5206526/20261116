# 資料庫匯入目錄

## 匯入目錄的用途

`import/` 目錄可讓你修改伺服器設定，而不必直接更動主要的 `/conf/` 與 `/db/` 檔案。

將自訂項目放入這兩個位置中的 `import/` 目錄，更新伺服器時便能保留核心檔案不變，減少更新時需要手動處理的衝突。你只需保存自己的修改，其餘核心內容即可隨 rAthena 更新。

## 運作方式

可以把「import」理解為「覆寫」。只需將已修改或要覆寫的設定放進匯入檔案。

例如，架設伺服器時，使用者通常會調整部分設定，讓 rAthena 符合自己的需求。以下範例說明如何正確使用 `/db/import/` 目錄。（`/conf/import/` 的範例請參閱 [/conf/readme.md](/conf/readme.md)。）

### 成就

---

假設我們要新增自訂成就，讓玩家可透過 NPC 腳本取得，並另外新增一個可授予管理員的成就。

#### /db/import/achievement_db.yml

```yml
    - Id: 280000
      Group: None
      Name: Emperio
      Reward:
        TitleId: 1035
      Score: 50
    - Id: 280001
      Group: None
      Name: Staff
      Reward:
        TitleId: 1036
      Score: 50
```

### 副本

---

假設我們要新增自訂的住宅副本。

#### /db/import/instance_db.yml

```yml
    - Id: 35
      Name: Home
      IdleTimeOut: 900
      Enter:
        Map: 1@home
        X: 24
        Y: 6
      AdditionalMaps:
        - Map: 2@home
        - Map: 3@home
```

### 魔物外觀別名

---

假設我們要讓波利顯示為巴風特的外觀。

#### /db/import/mob_avail.yml

```yml
    - Mob: PORING
      Sprite: BAPHOMET
```

### 自訂地圖

---

若要新增自訂地圖，必須先將地圖名稱加入 `import/map_index.txt`，再將地圖資料加入 `import/map_cache.dat`，讓 Map Server 能夠載入。

#### /db/import/map_index.txt

```
    1@home\t1250
    2@home
    3@home
    ev_has
    shops
    prt_pvp
```

### 道具交易限制

---

假設我們要限制特定道具，禁止玩家交易、販售、丟棄、存入倉庫等。

#### /db/import/item_db.yml

```yml
    - Id: 34000 # 舊綠色寶箱
      Trade:
        NoDrop: true
        NoTrade: true
        TradePartner: true
        NoSell: true
        NoCart: true
        NoStorage: true
        NoGuildStorage: true
        NoMail: true
        NoAuction: true
    - Id: 34001 # 房屋鑰匙
      Trade:
        NoDrop: true
        NoTrade: true
        TradePartner: true
        NoSell: true
        NoCart: true
        NoStorage: true
        NoGuildStorage: true
        NoMail: true
        NoAuction: true
    - Id: 34002 # 聲望日誌
      Trade:
        NoDrop: true
        NoTrade: true
        TradePartner: true
        NoSell: true
        NoCart: true
        NoStorage: true
        NoGuildStorage: true
        NoMail: true
        NoAuction: true
```

### 自訂任務

---

假設我們要在 quest_db 中新增自訂任務。

#### /db/import/quest_db.yml

```yml
    - Id: 89001
      Title: "聲望任務"
    - Id: 89002
      Title: "聲望任務"
```

我們再次強調，善用匯入系統對所有使用者都很有幫助。大多數 Git 更新衝突都能透過使用 `import/` 目錄來避免。

## 繁體中文與資料相容性原則

本目錄中可供管理者閱讀的說明、註解及範例說明統一使用繁體中文。為避免伺服器資料載入、腳本及客戶端資料對照發生錯誤，下列內容必須保留原始值，不可直接翻譯：

- YAML／TXT 欄位鍵名、資料表欄位、常數、指令名稱及設定識別字。
- 道具、魔物、技能、職業、地圖的 ID、AegisName、索引與內部代碼。
- 程式解析使用的枚舉值、布林值、路徑、檔名及腳本內容。
- 地圖快取等二進位資料（例如 `map_cache.dat`）。

`db/translated/` 是獨立的多語系翻譯素材區，包含其他語系的外部翻譯資料，並非伺服器啟動時載入的主要資料庫設定。本次保留其原始語系資料，避免把第三方翻譯素材改寫成不相符的內容；若日後要改用繁體中文客戶端資料，應另行建立並驗證對應的 zh-TW 資料集。
