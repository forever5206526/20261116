# Pandas develop 功能盤點 — 地圖標記批次

盤點日期：2026-11-17  
Pandas 基準：`PandasWS/Pandas@0aefda40dc55e7cc1f6f9174f96b2314b0de7899`  
核心基準：`AoShinRO/brHades@cffe264644a32e059a505d744587c1e696c67ac0`

## 盤點原則

- 以 Pandas `src/config/pandas.hpp` 的功能開關與對應實作為來源，不以檔案路徑差異直接判斷功能缺失。
- 同名功能可能已由 brHades 原生實作；必須比對行為、腳本常量、地圖旗標、資料結構及相依呼叫，不能重複造輪子。
- 標記為「已移植」只代表程式碼與回歸測試已納入目前整合版本，不代表已完成線上遊戲客戶端實測。
- 所有未核對項目保持待辦，不得因編譯成功而標記完成。

## Pandas MapFlag 完整清單

Pandas 基準中的 `Pandas_MapFlag_*` 開關共 24 項。已完成程式碼移植或確認原生等價實作 10 項；其餘 14 項仍待逐項比對及移植。

| Pandas 功能開關 | 功能 | 目前狀態 |
|---|---|---|
| `Pandas_MapFlag_MobInfo` | mobinfo 地圖魔物資訊顯示 | 待核對；依賴 MobInfomation 拓展 |
| `Pandas_MapFlag_NoAutoLoot` | 禁止地圖自動拾取 | 已移植／回歸測試通過 |
| `Pandas_MapFlag_NoToken` | 禁止原地復活之證 | 已移植／回歸測試通過 |
| `Pandas_MapFlag_NoCapture` | 禁止寵物捕捉 | 已移植相容別名；轉接 brHades 原生 MF_NOPETCAPTURE |
| `Pandas_MapFlag_HideGuildInfo` | 隱藏其他玩家公會資訊 | 待核對及移植 |
| `Pandas_MapFlag_HidePartyInfo` | 隱藏其他玩家隊伍名稱 | 待核對及移植 |
| `Pandas_MapFlag_NoMail` | 禁止郵件／RODEX 操作 | 已移植／回歸測試通過 |
| `Pandas_MapFlag_NoPet` | 禁止地圖使用寵物（啟用時退回寵物蛋） | 已移植／PR #5 的 35 項 CI checks 全部成功 |
| `Pandas_MapFlag_NoHomun` | 禁止召喚人工生命體 | brHades 原生等價實作；PR #5 的 NoHomun 回歸測試隨 CI 通過 |
| `Pandas_MapFlag_NoMerc` | 禁止召喚佣兵 | 已新增旗標、阻止召喚、隱藏既有佣兵及雙語訊息；等待 CI |
| `Pandas_MapFlag_MobDroprate` | 地圖普通魔物掉落倍率 | 待核對及移植 |
| `Pandas_MapFlag_MvpDroprate` | 地圖 MVP 掉落倍率 | 待核對及移植 |
| `Pandas_MapFlag_MaxHeal` | 限制地圖最大治癒量 | 待核對及移植 |
| `Pandas_MapFlag_MaxDmg_Skill` | 限制地圖最大技能傷害 | 待核對及移植 |
| `Pandas_MapFlag_MaxDmg_Normal` | 限制地圖最大普通攻擊傷害 | 待核對及移植 |
| `Pandas_MapFlag_NoSkill2` | 依單位類型禁止技能 | 待核對及移植 |
| `Pandas_MapFlag_NoAura` | 禁用地圖光環效果 | 待核對；依賴 Aura 機制 |
| `Pandas_MapFlag_MaxASPD` | 限制地圖最大攻速 | 待核對及移植 |
| `Pandas_MapFlag_NoSlave` | 禁止魔物召喚隨從 | 已移植／回歸測試通過 |
| `Pandas_MapFlag_NoBank` | 禁止銀行操作體驗調整 | 待核對 brHades 原生實作與體驗差異 |
| `Pandas_MapFlag_NoUseItem` | 禁止使用消耗型道具 | 已移植／回歸測試通過 |
| `Pandas_MapFlag_HideDamage` | 隱藏地圖傷害數值 | 待核對及移植 |
| `Pandas_MapFlag_NoAttack` | 禁止普通攻擊 | 已移植／回歸測試通過 |
| `Pandas_MapFlag_NoAttack2` | 依單位類型禁止普通攻擊 | 待核對及移植 |

## 下一批執行順序

1. 先對 17 項待辦逐項搜尋 brHades 原生同等功能，確認是否已存在及行為差異。
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
