# Pandas develop 功能盤點 — 地圖標記批次

盤點日期：2026-11-18  
Pandas 基準：`PandasWS/Pandas@0aefda40dc55e7cc1f6f9174f96b2314b0de7899`  
核心基準：`AoShinRO/brHades@cffe264644a32e059a505d744587c1e696c67ac0`

## 盤點原則

- 以 Pandas `src/config/pandas.hpp` 的功能開關與對應實作為來源，不以檔案路徑差異直接判斷功能缺失。
- 同名功能可能已由 brHades 原生實作；必須比對行為、腳本常量、地圖旗標、資料結構及相依呼叫，不能重複造輪子。
- 標記為「已移植」只代表程式碼與回歸測試已納入目前整合版本，不代表已完成線上遊戲客戶端實測。
- 所有未核對項目保持待辦，不得因編譯成功而標記完成。

## Pandas MapFlag 完整清單

Pandas 基準中的 `Pandas_MapFlag_*` 開關共 24 項。已完成程式碼移植或確認原生等價實作 19 項；其餘 5 項仍待逐項比對及移植。

| Pandas 功能開關 | 功能 | 目前狀態 |
|---|---|---|
| `Pandas_MapFlag_MobInfo` | mobinfo 地圖魔物資訊顯示 | 已整合共用多參數 MapFlag 框架、地圖參數設定／查詢、NPC mapflag、腳本 setmapflag/removemapflag 與 @mapinfo/@mapflag；仍待實際遊戲客戶端驗收 |
| `Pandas_MapFlag_NoAutoLoot` | 禁止地圖自動拾取 | 已移植／回歸測試通過 |
| `Pandas_MapFlag_NoToken` | 禁止原地復活之證 | 已移植／回歸測試通過 |
| `Pandas_MapFlag_NoCapture` | 禁止寵物捕捉 | 已移植相容別名；轉接 brHades 原生 MF_NOPETCAPTURE |
| `Pandas_MapFlag_HideGuildInfo` | 隱藏其他玩家公會資訊 | 已移植／PR #8 合併；16 組 VS 建置、PRE/RE NPC/DB、回歸測試及 CodeQL 通過 |
| `Pandas_MapFlag_HidePartyInfo` | 隱藏其他玩家隊伍名稱 | 已移植／PR #8 合併；16 組 VS 建置、PRE/RE NPC/DB、回歸測試及 CodeQL 通過 |
| `Pandas_MapFlag_NoMail` | 禁止郵件／RODEX 操作 | 已移植／回歸測試通過 |
| `Pandas_MapFlag_NoPet` | 禁止地圖使用寵物（啟用時退回寵物蛋） | 已移植／PR #5 的 35 項 CI checks 全部成功 |
| `Pandas_MapFlag_NoHomun` | 禁止召喚人工生命體 | brHades 原生等價實作；PR #5 的 NoHomun 回歸測試隨 CI 通過 |
| `Pandas_MapFlag_NoMerc` | 禁止召喚佣兵 | 已移植並合併至 main；39 項 CI checks 全部成功（含 VS Debug/Release、Win32/x64、PRE/RE、NPC/DB、CodeQL） |
| `Pandas_MapFlag_MobDroprate` | 地圖普通魔物掉落倍率 | 已移植／PR #21 已合併；已加入地圖參數設定及魔物掉落倍率套用 |
| `Pandas_MapFlag_MvpDroprate` | 地圖 MVP 掉落倍率 | 已移植／PR #21 已合併；已加入地圖參數設定及 MVP 掉落倍率套用 |
| `Pandas_MapFlag_MaxHeal` | 限制地圖最大治癒量 | 已移植／PR #27 已合併；26 項 CI checks 全部成功，僅限制治療分支，不影響傷害計算 |
| `Pandas_MapFlag_MaxDmg_Skill` | 限制地圖最大技能傷害 | 已移植／PR #40 已合併；20 組 VS2019／VS2022／VS2026 × Debug／Release × Win32／x64 × PRE／RE 全數成功，PRE／RE NPC／DB、CodeQL 與回歸測試通過 |
| `Pandas_MapFlag_MaxDmg_Normal` | 限制地圖最大普通攻擊傷害 | 已移植／PR #40 已合併；技能與普通攻擊分流，主副手合計限傷，20 組 VS 建置、PRE／RE NPC／DB、CodeQL 與回歸測試通過 |
| `Pandas_MapFlag_NoSkill2` | 依單位類型禁止技能 | 待核對及移植 |
| `Pandas_MapFlag_NoAura` | 禁用地圖光環效果 | 待核對；依賴 Aura 機制 |
| `Pandas_MapFlag_MaxASPD` | 限制地圖最大攻速 | 待核對及移植 |
| `Pandas_MapFlag_NoSlave` | 禁止魔物召喚隨從 | 已移植／回歸測試通過 |
| `Pandas_MapFlag_NoBank` | 禁止銀行操作體驗調整 | 已確認原生 MF_NOBANK 等價；Pandas 唯一差異為禁止銀行時顯示紅色訊息框，PR #41 補齊此體驗，待 CI 驗收 |
| `Pandas_MapFlag_NoUseItem` | 禁止使用消耗型道具 | 已移植／回歸測試通過 |
| `Pandas_MapFlag_HideDamage` | 隱藏地圖傷害數值 | 已移植／PR #9 合併；合併後 VS、PRE/RE NPC/DB、回歸測試及 CodeQL 全部通過 |
| `Pandas_MapFlag_NoAttack` | 禁止普通攻擊 | 已移植／回歸測試通過 |
| `Pandas_MapFlag_NoAttack2` | 依單位類型禁止普通攻擊 | 待核對及移植 |

## 下一批執行順序

1. MaxDmg_Skill／MaxDmg_Normal 已由 PR #40 合併驗收。NoBank 的原生功能已存在，PR #41 補齊紅色提示樣式；其後依序處理 NoSkill2、NoAttack2、MaxASPD，最後處理依賴 Aura 機制的 NoAura。
2. 對不存在的功能追蹤 Pandas 實作、相依資料結構、封包、腳本常量、設定、訊息與資料庫。
3. 依相依關係排序，先處理可獨立驗證且不需大幅改動核心結構的功能。
4. 每個功能獨立修改、回歸測試、Debug/Release x64/Win32 雲端建置，再更新本表狀態。
5. 完成地圖標記批次後，繼續盤點管理指令、NPC 事件、效果調整、腳本指令、資料結構、資料庫、封包及 Web Server 等功能組。

## 本次基線驗收

目前工作分支最新已整合提交 `deebd3229cce0c76a79f6c1128db49f5aeab27fb` 已通過 GitHub Actions：
- Debug x64：成功
- Debug Win32：成功
- Release x64：成功
- Release Win32：成功
- 8 項功能回歸測試：成功

Release x64 編譯成品由 Actions artifact 保存；這些驗證不等同完整伺服器載入、資料庫遷移或遊戲客戶端實測。


## 2026-11-19 HideDamage 驗收紀錄

- PR #9 已合併至正式 `main`：`adb104471b2123fa44164e5afacf5c4b41458231`。
- 合併後正式 main 的 Visual Studio MSBuild（VS2019 16.11／VS2022／VS2026）、PRE／RE NPC 與資料庫驗證、功能回歸測試及 PRE／RE CodeQL 全部成功。
- HideDamage 支援普通攻擊與新舊技能傷害封包；隱藏數字不改變伺服器實際傷害。

## 2026-11-18 HideInfo 驗收紀錄

- PR #8 已合併至正式 `main`：`2b31e13ca7cf22585ecea0645a8721599e70b399`。
- 合併前最新 PR 提交的 16 組 Visual Studio Debug/Release、Win32/x64、PRE/RE 建置全部成功。
- PRE/RE NPC 與資料庫啟動驗證成功；HideInfo 與既有功能回歸測試成功；PRE/RE CodeQL 成功。
- 合併後針對 main 新提交啟動的 GitHub Actions 驗證仍需另外確認，不能以合併前結果代替。
- 13 項 HideInfo source-contract regression checks 已納入 Windows validation workflow；不等同完整遊戲客戶端實測。

## MobInfo 相依盤點（2026-11-18）

已核對 Pandas `develop` 與 brHades `main`：

- brHades 有原生全域 `show_mob_info` 設定及魔物名稱封包顯示，但沒有 `MF_MOBINFO`、`mapflag_config`、`mapflag_values`、`map_getmapflag_param()` 或 `map_setmapflag_param()`。
- Pandas 的 `MF_MOBINFO` 依賴 `Pandas_Mapflags` 共用參數框架；此框架涉及 `map_data` 參數儲存、參數範圍/預設值設定、地圖旗標解析、NPC mapflag 參數解析、腳本 `setmapflag` 參數、查詢/設定 API，以及相關管理指令與地圖資訊顯示。
- Pandas 同時預設啟用 `Pandas_MobInfomation_Extend`；其 `clif_name()` 會按地圖的 `MF_MOBINFO` 參數覆寫全域 `show_mob_info`，並將魔物等級／HP／編號、體型、種族、屬性分別放入名稱封包的多個欄位。brHades 目前未找到此擴充宏。此擴充還呼叫 `msg_txt_cn()`，依賴 Pandas `Pandas_Message_Conf`／`ALL_EXTEND_MSG` 自訂訊息偏移與翻譯設定；brHades 尚未移植該訊息框架，不能直接照搬 Pandas 的訊息 ID，否則會與既有 map message ID 衝突。
- Pandas 的參數值存放在每張地圖的 `mapflag_values`，並由 `map_data::copyFlags()` 複製到 instance map；重新載入地圖旗標時也要清除舊參數。移植時必須同步處理 map data 初始化、instance 複製及 reloadscript，不能只新增 getter/setter。
- 因此 MobInfo 不是單一 enum/handler 移植。應先設計並驗證共用 mapflag 參數框架，再移植 MobInfomation_Extend 與 MF_MOBINFO，最後驗證 mapflag/NPC/script/atcommand/封包路徑及 PRE/RE 建置。
- 本次僅完成相依盤點，未修改任何 MobInfo 程式碼，亦未將其標記為完成。


## 2026-11-20 MaxHeal 驗收紀錄

- PR #27 已合併至正式 `main`；合併後的 26 項 GitHub Actions checks 全部成功。
- Renewal 與 non-Renewal 治療計算均受 MaxHeal 上限控制；只在 `heal=true` 套用，`heal=false` 的傷害計算不受影響。
- `MF_MAXHEAL` 已匯出供 NPC 腳本使用，README 已補上設定及移除範例。
