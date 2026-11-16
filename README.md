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
