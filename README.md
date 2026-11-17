# 20261116

## 已移植的 Pandas 特色功能

### 鑑定事件與相容模式

- 新增 `OnPCIdentifyEvent`；鑑定結果送出後可觸發 NPC 事件。
- 事件腳本可使用 `@identify_idx` 取得本次鑑定的背包序號。
- `conf/battle/battle.conf` 的 `identify_event_mode` 控制觸發規則：
  - `0`：Pandas 1.2.4 相容模式，成功或失敗的鑑定結果都觸發事件。
  - `1`：rAthena 相容模式，只有鑑定成功時觸發事件。
- 新增 `OnPCIdentifyFilter` 與 `processhalt;`，可在鑑定資料變更前中斷本次鑑定。

預設設定：

```text
identify_event_mode: 0
```

修改 `conf/battle/battle.conf` 後重新啟動 map-server，使設定生效。

### NoAutoLoot 地圖標記

- 新增 `MF_NOAUTOLOOT`／`noautoloot` 地圖標記。
- 地圖啟用此標記後，該地圖的魔物掉落不會由 `@autoloot` 自動拾取。

在 NPC 腳本中設定：

```text
setmapflag "prontera", MF_NOAUTOLOOT;
```

移除標記：

```text
removemapflag "prontera", MF_NOAUTOLOOT;
```

將 `prontera` 改成要套用的地圖名稱。

### NoToken 地圖標記

- 新增 `MF_NOTOKEN`／`notoken` 地圖標記。
- 地圖啟用此標記後，玩家在該地圖使用原地復活之證時，伺服器會阻止原地復活並顯示提示訊息。

設定：

```text
setmapflag "prontera", MF_NOTOKEN;
```

移除：

```text
removemapflag "prontera", MF_NOTOKEN;
```

### NoMail 地圖標記

- 新增 `MF_NOMAIL`／`nomail` 地圖標記。
- 地圖啟用此標記後，玩家無法在該地圖開啟郵件／RODEX 視窗或進行郵件操作。

設定：

```text
setmapflag "prontera", MF_NOMAIL;
```

移除：

```text
removemapflag "prontera", MF_NOMAIL;
```

### NoCapture 寵物捕捉相容別名

- 新增 `MF_NOCAPTURE`；讀取及設定都會轉接至 brHades 已有的原生 `MF_NOPETCAPTURE`。
- 不新增第二套寵物捕捉阻擋邏輯；既有捕捉流程仍由原生標記處理。

設定：

```text
setmapflag "prontera", MF_NOCAPTURE;
```

移除：

```text
removemapflag "prontera", MF_NOCAPTURE;
```

### NoSlave 地圖標記

- 新增 `MF_NOSLAVE`／`noslave` 地圖標記。
- 地圖啟用此標記時，會阻止位於該地圖的魔物召喚隨從；不影響一般魔物刷新。

設定：

```text
setmapflag "prontera", MF_NOSLAVE;
```

移除：

```text
removemapflag "prontera", MF_NOSLAVE;
```

### NoAttack 地圖標記

- 新增 `MF_NOATTACK`／`noattack` 地圖標記。
- 啟用時，禁止位於該地圖上的單位進行普通攻擊；此標記不等同於禁止所有技能施放。

設定：

```text
setmapflag "prontera", MF_NOATTACK;
```

移除：

```text
removemapflag "prontera", MF_NOATTACK;
```

### NoUseItem 地圖標記

- 新增 `MF_NOUSEITEM`／`nouseitem` 地圖標記。
- 啟用後，玩家無法在該地圖使用消耗型道具；會顯示對應訊息並拒絕此次道具使用。
- 已補上英文及繁體中文訊息文字。

設定：

```text
setmapflag "prontera", MF_NOUSEITEM;
```

移除：

```text
removemapflag "prontera", MF_NOUSEITEM;
```


## Pandas 完整移植盤點文件

- [Pandas develop 416 項功能開關完整清冊](docs/PANDAS_FEATURE_FLAGS_CATALOG.md)：以固定上游 commit 的 `src/config/pandas.hpp` 為來源，列出全部 416 個啟用中的 `Pandas_*` 巨集，作為逐項追蹤索引；不代表這些項目已完成移植。
- [Pandas 地圖標記功能盤點](docs/PANDAS_MAPFLAG_INVENTORY.md)：列出 24 項地圖標記功能及目前已移植／待核對狀態。


### NoPet 地圖標記

- 新增 `MF_NOPET` 腳本常量及 `Pandas_MapFlag_NoPet` 功能開關。
- 啟用地圖標記時，會將目前位於該地圖的已召喚寵物退回寵物蛋。
- 保留 Pandas 原始觸發時機；此項不額外改寫寵物孵化或捕捉流程。

設定：

```text
setmapflag "prontera", MF_NOPET;
```

移除：

```text
removemapflag "prontera", MF_NOPET;
```

### NoHomun 地圖標記

- 新增 `MF_NOHOMUN` 腳本常量及地圖標記。
- 啟用時會讓目前位於該地圖的活躍人工生命體進入休息狀態，並阻止玩家在該地圖召喚人工生命體。
- 新增英文及繁體中文訊息。

設定：

```text
setmapflag "prontera", MF_NOHOMUN;
```

移除：

```text
removemapflag "prontera", MF_NOHOMUN;
```

### NoMerc 地圖標記

- 新增 `Pandas_MapFlag_NoMerc` 功能開關及 `MF_NOMERC` 腳本常量。
- 啟用時阻止玩家在該地圖召喚佣兵，並將目前位於該地圖的既有佣兵隱藏。
- 新增英文及繁體中文提示訊息。

設定：

```text
setmapflag "prontera", MF_NOMERC;
```

移除：

```text
removemapflag "prontera", MF_NOMERC;
```
