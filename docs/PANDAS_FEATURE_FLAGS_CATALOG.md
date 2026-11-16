# Pandas develop 功能開關完整清冊

- 上游來源：`PandasWS/Pandas`
- 分支：`develop`
- 固定盤點 Commit：`0aefda40dc55e7cc1f6f9174f96b2314b0de7899`
- 來源檔案：`src/config/pandas.hpp`
- 擷取結果：416 個啟用中的 `Pandas_*` 巨集定義（不含註解掉的定義）。
- 這份清冊是「功能入口索引」，不是已完成移植清單。每一項都必須追蹤其實作、資料結構、呼叫點、腳本/NPC/資料庫/設定及相依性，再判定 brHades 是否已有等價功能。

## 完整功能開關

| # | 功能開關 | 上游行號 | 上游註解／用途線索 |
|---:|---|---:|---|
| 1 | `Pandas_Basic` | 16 | （需回查原始碼區塊） |
| 2 | `Pandas_DatabaseIncrease` | 17 | （需回查原始碼區塊） |
| 3 | `Pandas_StructIncrease` | 18 | （需回查原始碼區塊） |
| 4 | `Pandas_BattleConfigure` | 19 | （需回查原始碼區塊） |
| 5 | `Pandas_InternalConfigure` | 20 | （需回查原始碼區塊） |
| 6 | `Pandas_FuncIncrease` | 21 | （需回查原始碼區塊） |
| 7 | `Pandas_PacketFunction` | 22 | （需回查原始碼區塊） |
| 8 | `Pandas_CreativeWork` | 23 | （需回查原始碼區塊） |
| 9 | `Pandas_Speedup` | 24 | （需回查原始碼區塊） |
| 10 | `Pandas_Bugfix` | 25 | （需回查原始碼區塊） |
| 11 | `Pandas_Crashfix` | 26 | （需回查原始碼區塊） |
| 12 | `Pandas_ScriptEngine` | 27 | （需回查原始碼區塊） |
| 13 | `Pandas_Redeclaration` | 28 | （需回查原始碼區塊） |
| 14 | `Pandas_UserExperience` | 29 | （需回查原始碼區塊） |
| 15 | `Pandas_Cleanup` | 30 | （需回查原始碼區塊） |
| 16 | `Pandas_NpcEvent` | 31 | （需回查原始碼區塊） |
| 17 | `Pandas_Mapflags` | 32 | （需回查原始碼區塊） |
| 18 | `Pandas_AtCommands` | 33 | （需回查原始碼區塊） |
| 19 | `Pandas_Bonuses` | 34 | （需回查原始碼區塊） |
| 20 | `Pandas_ScriptCommands` | 35 | （需回查原始碼區塊） |
| 21 | `Pandas_ScriptConstants` | 36 | （需回查原始碼區塊） |
| 22 | `Pandas_ScriptResults` | 37 | （需回查原始碼區塊） |
| 23 | `Pandas_ScriptParams` | 38 | （需回查原始碼區塊） |
| 24 | `Pandas_WebServer` | 39 | （需回查原始碼區塊） |
| 25 | `Pandas_Version` | 70 | 1.0.2.1 ^ 此处第四段为 1 表示这是一个 1.0.2 的开发版本 (develop) 在 Windows 环境下, 程序启动时会根据第四段的值自动携带对应的版本后缀, 以便进行版本区分 |
| 26 | `Pandas_Show_Logo` | 73 | 在启动时显示 Pandas 的 LOGO |
| 27 | `Pandas_Show_Version` | 76 | 在启动时显示 Pandas 的版本号 |
| 28 | `Pandas_Google_Breakpad` | 79 | 是否启用 Google Breakpad 用于处理程序崩溃 |
| 29 | `Pandas_Helper_Common_Function` | 82 | 是否启用一些杂乱的自定义辅助函数 |
| 30 | `Pandas_CodeAnalysis_Suggestion` | 86 | 是否启用代码分析工具所建议的处理措施以避免潜在风险 包含的工具有: LGTM, CodeQL, Microsoft Code Analysis 等 |
| 31 | `Pandas_Struct_Unit_CommonData` | 97 | 使 map_session_data, npc_data, mob_data, homun_data, mercenary_data, elemental_data, pet_data 能够有一个独立的结构体用来 存放 Pandas 针对多单位通用的拓展 [Sola丶小克] |
| 32 | `Pandas_Struct_Unit_CommonData_Aura` | 102 | 使 s_unit_common_data 可记录单位的光环信息 [Sola丶小克] |
| 33 | `Pandas_Struct_Unit_CommonData_BattleRecord` | 105 | 使 s_unit_common_data 可记录战斗记录信息 [Sola丶小克] |
| 34 | `Pandas_Struct_Map_Session_Data_Pandas` | 110 | 使 map_session_data 有一个独立的结构体用来存放 Pandas 的拓展 [Sola丶小克] 结构体修改定位 pc.hpp -> map_session_data.pandas |
| 35 | `Pandas_Struct_Map_Session_Data_WorkInEvent` | 116 | 使 map_session_data 可记录当前玩家正在处理哪一个脚本事件 [Sola丶小克] 结构体修改定位 pc.hpp -> map_session_data.pandas.workinevent |
| 36 | `Pandas_Struct_Map_Session_Data_EventHalt` | 120 | 使 map_session_data 可记录事件中断请求 [Sola丶小克] 结构体修改定位 pc.hpp -> map_session_data.pandas.eventhalt |
| 37 | `Pandas_Struct_Map_Session_Data_EventTrigger` | 124 | 使 map_session_data 可记录事件触发请求 [Sola丶小克] 结构体修改定位 pc.hpp -> map_session_data.pandas.eventtrigger |
| 38 | `Pandas_Struct_Map_Session_Data_AmuletCalculating` | 128 | 使 map_session_data 可记录当前是否正在进行护身符能力计算 [Sola丶小克] 结构体修改定位 pc.hpp -> map_session_data.pandas.amulet_calculating |
| 39 | `Pandas_Struct_Map_Session_Data_MultiCatchTargetClass` | 131 | 使 map_session_data 可记录即将支持捕捉的多个魔物编号 [Sola丶小克] |
| 40 | `Pandas_Struct_Map_Session_Data_MultiTransfer` | 135 | 使 map_session_data 可记录接下来的 pc_setpos 调用是不是一次多人传送 [Sola丶小克] 结构体修改定位 pc.hpp -> map_session_data.pandas.multitransfer |
| 41 | `Pandas_Struct_Map_Session_Data_Skip_LoadEndAck_NPC_Event_Dequeue` | 139 | 使 map_session_data 可记录是否在 LoadEndAck 调用中不弹出队列中的事件 [Sola丶小克] 结构体修改定位 pc.hpp -> map_session_data.pandas.skip_loadendack_npc_event_dequeue |
| 42 | `Pandas_Struct_Map_Session_Data_Autotrade_Configure` | 144 | 使 map_session_data 可记录离线挂店 / 挂机角色的朝向等状态数据 [Sola丶小克] rAthena 使用完成 autotrade 的朝向数据后就销毁掉了 为了能够支持离线挂店 / 挂机可以被 recall 召唤, 我们需要保留一部分数据 |
| 43 | `Pandas_Struct_Map_Session_Data_BonusScript_Counter` | 148 | 使 map_session_data 可记录玩家已经生成的 bonus_script 记录数 [Sola丶小克] 结构体修改定位 pc.hpp -> map_session_data.pandas.bonus_script_counter |
| 44 | `Pandas_Struct_Item_Data_Pandas` | 153 | 使 item_data 有一个独立的结构体用来存放 Pandas 的拓展 [Sola丶小克] 结构体修改定位 itemdb.hpp -> item_data.pandas |
| 45 | `Pandas_Struct_Item_Data_Script_Plaintext` | 159 | 使 item_data 可记录当前物品的使用、穿戴、卸装脚本的原文 [Sola丶小克] 结构体修改定位 itemdb.hpp -> item_data.pandas.script_plaintext |
| 46 | `Pandas_Struct_Item_Data_Taming_Mobid` | 163 | 使 item_data 可记录当前物品可捕捉的魔物编号 [Sola丶小克] 结构体修改定位 itemdb.hpp -> item_data.pandas.taming_mobid |
| 47 | `Pandas_Struct_Item_Data_Has_CallFunc` | 167 | 使 item_data 可记录此物品的使用脚本是否执行了 callfunc 指令 [Sola丶小克] 结构体修改定位 itemdb.hpp -> item_data.pandas.has_callfunc |
| 48 | `Pandas_Struct_Item_Data_Properties` | 172 | 使 item_data 可记录此物品的特殊属性 [Sola丶小克] 效果与 item_data.flag 类似, 只是数据源为 item_properties.yml 结构体修改定位 itemdb.hpp -> item_data.pandas.properties |
| 49 | `Pandas_Struct_Npc_Data_Pandas` | 177 | 使 npc_data 有一个独立的结构体用来存放 Pandas 的拓展 [Sola丶小克] 结构体修改定位 npc.hpp -> npc_data.pandas |
| 50 | `Pandas_Struct_Npc_Data_DestructionStrategy` | 183 | 使 npc_data 结构体可记录此 NPC 的自毁策略 [Sola丶小克] 结构体修改定位 npc.hpp -> npc_data.pandas.destruction_strategy |
| 51 | `Pandas_Struct_Mob_Data_Pandas` | 188 | 使 mob_data 有一个独立的结构体用来存放 Pandas 的拓展 [Sola丶小克] 结构体修改定位 mob.hpp -> mob_data.pandas |
| 52 | `Pandas_Struct_Mob_Data_Special_SetUnitData` | 194 | 使 mob_data 结构体可记录此魔物被 setunitdata 修改过哪些项目 [Sola丶小克] 结构体修改定位 mob.hpp -> mob_data.pandas.special_setunitdata |
| 53 | `Pandas_Struct_Mob_Data_SpecialExperience` | 198 | 使 mob_data 结构体可记录此魔物特殊的基础经验或职业经验 [Sola丶小克] 结构体修改定位 mob.hpp -> mob_data.pandas.base_exp 和 job_exp |
| 54 | `Pandas_Struct_Autotrade_Extend` | 206 | 进行拓展处理之后能够在代码改动较少的情况下, 更好的支持多种不同类型的 "离线挂店" 行为 在默认情况下 sd->state.autotrade 的值若为 0 则表示没有离线挂店 若非零的话则表示启用了离线挂店, 且 &2 表示开启的是离线摆摊挂店 &3 表示开启的是离线收购挂店 |
| 55 | `Pandas_Struct_BonusScriptData_Extend` | 211 | 对 bonus_script_data 的定义进行拓展处理 [Sola丶小克] 默认的 rAthena 中 bonus_script 机制并没有唯一编号的概念, 为了提高对 bonus_script 的控制粒度 我们需要将唯一编号引入到我们需要拓展的相关数据结构体中 |
| 56 | `Pandas_Struct_S_Mail_With_Details` | 214 | 使 s_mail.item 能有一个 details 字段用来记录附件道具更详细的信息 [Sola丶小克] |
| 57 | `Pandas_Struct_S_Random_Opt_Data_With_Plaintext` | 217 | 使 s_random_opt_data 能保存脚本的明文 [Sola丶小克] |
| 58 | `Pandas_Struct_S_Item_Combo_With_Plaintext` | 220 | 使 s_item_combo 能保存脚本的明文 [Sola丶小克] |
| 59 | `Pandas_Struct_Status_Change_Cloak_Reverting` | 223 | 使 status_change 能保存 cloak 是否正在进行中的状态 [Sola丶小克] |
| 60 | `Pandas_Struct_Map_Data_Mob_Spawns` | 226 | 使 map_data 能保存全部魔物的刷新点信息 [Sola丶小克] |
| 61 | `Pandas_Database_ItemProperties` | 238 | （需回查原始碼區塊） |
| 62 | `Pandas_Database_MobItem_FixedRatio` | 243 | 是否启用魔物道具固定掉率数据库及其功能 [Sola丶小克] 通过这个数据库可以指定某个道具的全局固定掉落概率, 且能绕过等级惩罚和VIP掉率加成等机制 |
| 63 | `Pandas_Database_Yaml_BeQuiet` | 246 | 是否拓展 Yaml 的 Database 操作类使之能抑制错误信息 [Sola丶小克] |
| 64 | `Pandas_Database_SQL_GetEncoding` | 249 | 是否支持用于读取 SQL 连接编码的 Sql_GetEncoding 函数 [Sola丶小克] |
| 65 | `Pandas_BattleConfig_Verification` | 258 | 是否支持对战斗配置选项进行完整性检查 [╰づ记忆•斑驳〤 实现] [Sola丶小克 改进] |
| 66 | `Pandas_BattleConfig_Force_LoadEvent` | 262 | 是否启用 force_loadevent 配置选项及其功能 [Sola丶小克] 此选项可以强制没有 loadevent 标记的地图也能触发 OnPCLoadMapEvent 事件 |
| 67 | `Pandas_BattleConfig_Force_Identified` | 266 | 是否启用 force_identified 配置选项及其功能 [Sola丶小克] 此选项可以强制特定渠道获得的装备自动变成已鉴定 |
| 68 | `Pandas_BattleConfig_CashMounting_UseitemLimit` | 270 | 是否启用 cashmount_useitem_limit 配置选项及其功能 [Sola丶小克] 此选项可以使乘坐“商城坐骑”时禁止使用特定类型的物品 |
| 69 | `Pandas_BattleConfig_MaxAspdForPVP` | 274 | 是否启用 max_aspd_for_pvp 配置选项及其功能 [Sola丶小克] 此选项用于限制玩家在 PVP 地图上的最大攻击速度 (以 MF_PVP 地图标记为准) |
| 70 | `Pandas_BattleConfig_MaxAspdForGVG` | 278 | 是否启用 max_aspd_for_gvg 配置选项及其功能 [Sola丶小克] 此选项用于限制玩家在 GVG 地图上的最大攻击速度 (以 MF_GVG/MF_GVG_TE 地图标记为准) |
| 71 | `Pandas_BattleConfig_AtCmd_No_Permission` | 282 | 是否启用 atcmd_no_permission 配置选项及其功能 [Sola丶小克] 此选项用于指定没有指令权限的玩家, 在执行了管理员指令时的处理策略 |
| 72 | `Pandas_BattleConfig_Suspend_MonsterIgnore` | 286 | 是否启用 suspend_monsterignore 配置选项及其功能 [Sola丶小克] 此选项用于指定当玩家使用挂机系列指令时, 哪些模式不会被魔物攻击 (掩码选项) |
| 73 | `Pandas_BattleConfig_Suspend_Whisper_Response` | 290 | 是否启用 suspend_whisper_response 配置选项及其功能 [Sola丶小克] 此选项用于指定当玩家使用挂机系列指令时, 处于哪些模式会自动回复私聊讯息 (掩码选项) |
| 74 | `Pandas_BattleConfig_Suspend_Offline_BodyDirection` | 294 | 是否启用 suspend_offline_bodydirection 配置选项及其功能 [Sola丶小克] 此选项用于指定当玩家进入离线挂机模式时, 地图服务器重启后的身体朝向哪里 |
| 75 | `Pandas_BattleConfig_Suspend_Offline_HeadDirection` | 298 | 是否启用 suspend_offline_headdirection 配置选项及其功能 [Sola丶小克] 此选项用于指定当玩家进入离线挂机模式时, 地图服务器重启后的头部朝向哪里 |
| 76 | `Pandas_BattleConfig_Suspend_Offline_Sitdown` | 302 | 是否启用 suspend_offline_sitdown 配置选项及其功能 [Sola丶小克] 此选项用于指定当玩家进入离线挂机模式时, 地图服务器重启后处于站立还是坐下状态 |
| 77 | `Pandas_BattleConfig_Suspend_AFK_BodyDirection` | 306 | 是否启用 suspend_afk_bodydirection 配置选项及其功能 [Sola丶小克] 此选项用于指定当玩家进入离开模式时, 地图服务器重启后的身体朝向哪里 |
| 78 | `Pandas_BattleConfig_Suspend_AFK_Headdirection` | 310 | 是否启用 suspend_afk_headdirection 配置选项及其功能 [Sola丶小克] 此选项用于指定当玩家进入离开模式时, 地图服务器重启后的头部朝向哪里 |
| 79 | `Pandas_BattleConfig_Suspend_AFK_Sitdown` | 314 | 是否启用 suspend_afk_sitdown 配置选项及其功能 [Sola丶小克] 此选项用于指定当玩家进入离开模式时, 地图服务器重启后处于站立还是坐下状态 |
| 80 | `Pandas_BattleConfig_Suspend_AFK_HeadTop_ViewID` | 318 | 是否启用 suspend_afk_headtop_viewid 配置选项及其功能 [Sola丶小克] 此选项用于当玩家进入离开模式时, 将头饰上的更换为哪一个指定的头饰外观编号 |
| 81 | `Pandas_BattleConfig_Suspend_Normal_BodyDirection` | 322 | 是否启用 suspend_normal_bodydirection 配置选项及其功能 [Sola丶小克] 此选项用于指定当玩家进入普通模式时, 被拉上线的角色身体朝向哪里 |
| 82 | `Pandas_BattleConfig_Suspend_Normal_HeadDirection` | 326 | 是否启用 suspend_normal_headdirection 配置选项及其功能 [Sola丶小克] 此选项用于指定当玩家进入普通模式时, 被拉上线的角色头部朝向哪里 |
| 83 | `Pandas_BattleConfig_Suspend_Normal_Sitdown` | 330 | 是否启用 suspend_normal_sitdown 配置选项及其功能 [Sola丶小克] 此选项用于指定当玩家进入普通模式时, 被拉上线的角色处于站立还是坐下状态 |
| 84 | `Pandas_BattleConfig_Multiplayer_Recall_Behavior` | 334 | 是否启用 multiplayer_recall_behavior 配置选项及其功能 [Sola丶小克] 此选项用于控制多人召唤时是否避开在线摆摊玩家 |
| 85 | `Pandas_BattleConfig_AlwaysTriggerNPCKillEvent` | 338 | 是否启用 always_trigger_npc_killevent 配置选项及其功能 [Sola丶小克] 此选项用于控制当魔物拥有且触发了自己的死亡事件标签后, 是否还会继续触发 OnNPCKillEvent 事件 |
| 86 | `Pandas_BattleConfig_AlwaysTriggerMVPKillEvent` | 342 | 是否启用 always_trigger_mvp_killevent 配置选项及其功能 [Sola丶小克] 此选项用于控制当 MVP 魔物拥有且触发了自己的死亡事件标签后, 是否还会继续触发 OnPCKillMvpEvent 事件 |
| 87 | `Pandas_BattleConfig_BattleRecord_AutoEnabled_Unit` | 346 | 是否启用 batrec_autoenabled_unit 配置选项及其功能 [Sola丶小克] 此选项用于设置默认情况下有哪些类型的单位会启用战斗记录 |
| 88 | `Pandas_BattleConfig_Repeat_ClearUnit_Interval` | 350 | 是否启用 repeat_clearunit_interval 配置选项及其功能 [Sola丶小克] 此选项用于设置重发魔物死亡封包的间隔时间 (单位为: 毫秒) |
| 89 | `Pandas_BattleConfig_Dead_Area_Size` | 354 | 是否启用 dead_area_size 配置选项及其功能 [Sola丶小克] 此选项用于设置魔物死亡封包将会发送给周围多少个格的玩家 |
| 90 | `Pandas_BattleConfig_Remove_Manhole_With_Status` | 358 | 是否启用 remove_manhole_with_status 配置选项及其功能 [Sola丶小克] 此选项用于设置当"人孔/黑洞陷阱"地面陷阱被移除的时候是否同时使被捕获的玩家脱困 |
| 91 | `Pandas_BattleConfig_Restore_Mes_Logic` | 362 | 是否启用 restore_mes_logic 配置选项及其功能 [Sola丶小克] 此选项用于设置是否使 2021-11-03 及更新版本的客户端在执行 mes 指令时使用经典换行策略 |
| 92 | `Pandas_BattleConfig_ItemDB_Warning_Policy` | 366 | 是否启用 itemdb_warning_policy 配置选项及其功能 [Sola丶小克] 此选项用于控制是否关闭加载物品数据库时的一些警告信息 |
| 93 | `Pandas_BattleConfig_MobDB_DamageMotion_Min` | 370 | 是否启用 mob_default_damagemotion 配置选项及其功能 [Renee] 此选项用于控制当魔物被攻击时受伤动画的默认播放时长, 值越小看起来越快 (单位为: 毫秒) |
| 94 | `Pandas_BattleConfig_Mob_SetUnitData_Persistence` | 374 | 是否启用 mob_setunitdata_persistence 配置选项及其功能 [Sola丶小克] 此选项用于控制是否高优先级持久化保存 setunitdata 对魔物的设置 |
| 95 | `Pandas_BattleConfig_Strict_Parameters_Of_Rand` | 378 | 是否启用 strict_parameters_of_rand 配置选项及其功能 [Sola丶小克] 此选项用于控制是否对 rand 脚本指令进行严格的参数检查, 以便兼容以前早期的脚本 |
| 96 | `Pandas_BattleConfig_Identify_Event_Mode` | 382 | 是否启用 identify_event_mode 配置选项及其功能 此选项用于选择鉴定事件遵循 Pandas 1.2.4 或 rAthena 的触发规则 |
| 97 | `Pandas_InterConfig_HideServerIpAddress` | 393 | 是否启用 hide_server_ipaddress 配置选项及其功能 [Sola丶小克] 此选项用于确保服务端不主动返回服务器的 IP 地址给到客户端, 通常用于支持代理方式登录 |
| 98 | `Pandas_FuncParams_PC_EQUIPITEM` | 403 | 在 pc.cpp 中的 pc_equipitem 增加 swapping 参数 [Sola丶小克] 新增的 swapping 用于判断当前的装备穿戴调用是否由装备切换机制引发, 默认为 false |
| 99 | `Pandas_FuncLogic_PC_EQUIPITEM_BOUND_OPPORTUNITY` | 406 | 调整 pc.cpp 中 pc_equipitem 执行道具绑定的时机 [Sola丶小克] |
| 100 | `Pandas_FuncDefine_STORAGE_ADDITEM` | 409 | 调整 storage.cpp 中 storage_additem 的函数定义, 移除 static 关键字 [Sola丶小克] |
| 101 | `Pandas_FuncDefine_Instance_Destory` | 414 | 调整 instance.cpp 中 instance_destroy 的定义 增加 skip_erase 参数用于控制成功销毁副本后不 erase 掉 instance 对象 以便交由外部来进行 erase, 这样才能获取下一个指针的正确位置 (C++11) [Sola丶小克] |
| 102 | `Pandas_FuncDefine_UnitDead_With_ExtendInfo` | 422 | 魔物单位 : mob.cpp -> mob_dead 生命体单位 : homunculus.cpp -> hom_dead 佣兵单位 : mercenary.cpp -> mercenary_dead 元素精灵 : elemental.cpp -> elemental_dead |
| 103 | `Pandas_FuncExtend_Increase_Inventory` | 429 | 以便能够支持将背包的最大上限设置成超过 128 的值 [Sola丶小克] 提示: 根据目前的 struct item 和 struct s_storage 的体积情况, 应该可支持将 MAX_INVENTORY 调整到 800 左右, 但设置越大对性能影响会越大 |
| 104 | `Pandas_FuncLogic_ATCOMMAND_RELOAD` | 433 | 调整 atcommand.cpp 中 atcommand_reload 配置重载指令的逻辑 [Sola丶小克] 我们希望在执行某些 reload 指令 (@reloadbattleconf) 时能重新计算全服玩家的属性和能力值 |
| 105 | `Pandas_FuncLogic_Instance_Destroy_Command` | 437 | 重写 instance.cpp -> instance_destroy_command 函数 因为 rAthena 官方实现的该函数在切换队长后的处理并不友好 [Sola丶小克] |
| 106 | `Pandas_FuncLogic_Whitelist_Privileges` | 446 | 虽然有提示， 但是根据白名单规则却又进行了放行操作.. 因此这个提示是很没意义的. 启用此选项将改变判断逻辑, 变成如下: 只要 IP 地址被判定为无条件放行, 那么他将不会因为高频连接而被判定为发起了 DDoS 攻击. |
| 107 | `Pandas_FuncParams_Clif_Item_Equip` | 450 | 调整 clif.cpp 中给 clif_item_equip 函数增加 caller 参数 [Sola丶小克] 新增的 caller 参数用来标记调用这个函数的调用者是谁, 以便在必要情况下能够调整返回给客户端的字段值 |
| 108 | `Pandas_FuncDefine_Mob_Once_Spawn_Sub` | 454 | 在 mob.cpp 中的 mob_once_spawn_sub 增加 spawn_flag 参数 [Sola丶小克] 新增的 spawn_flag 参数可以用来控制召唤出来的魔物是不是 BOSS (可以被 BOSS 雷达探测) |
| 109 | `Pandas_FuncDefine_Mob_Once_Spawn` | 460 | （需回查原始碼區塊） |
| 110 | `Pandas_FuncDefine_Mob_Getmob_Boss` | 465 | 在 map.cpp 中的 map_getmob_boss 增加 alive_first 参数 [Sola丶小克] 新增的 alive_first 参数可以指定优先返回存活着的 BOSS 魔物 |
| 111 | `Pandas_FuncParams_Mob_MvpTomb_Create` | 469 | 在 mob.cpp 中的 mvptomb_create 增加 killer_gid 参数 [Sola丶小克] 新增的 killer_gid 参数用于传递杀死 MVP 玩家的游戏单位编号 |
| 112 | `Pandas_Console_Translate` | 488 | 是否启用终端控制台的信息翻译机制 [Sola丶小克] |
| 113 | `Pandas_Message_Conf` | 493 | 扩展信息配置文件 (Msg_conf) 的 ID 最大上限, 同时提供 msg_txt_cn 宏定义函数, 方便在工程中使用自定义信息 [Sola丶小克] |
| 114 | `Pandas_Message_Reorganize` | 498 | 对消息文件进行清理, 移除几乎用不到的其他国家语言 同时也暂时移除掉 langtype 管理员指令, 这个指令目前不太合适熊猫模拟器 主要留下: 英文, 简体中文, 繁体中文 这三种. [Sola丶小克] |
| 115 | `Pandas_Message_Hardcode_Extract` | 502 | 将部分硬编码的字符串提取到消息文件中 [Sola丶小克] 这么做的主要目的是在有需要的时候, 可以将内容进行汉化或者其他处理 |
| 116 | `Pandas_Support_Specify_PacketKeys` | 506 | （需回查原始碼區塊） |
| 117 | `Pandas_Support_UTF8BOM_Files` | 510 | 是否支持读取 UTF8-BOM 编码的配置或者数据文件 [Sola丶小克] |
| 118 | `Pandas_Strict_Userid_Verification` | 515 | （需回查原始碼區塊） |
| 119 | `Pandas_Support_Hide_Online_Players_Count` | 519 | 是否支持隐藏角色服务器的在线人数 [Sola丶小克] |
| 120 | `Pandas_MobInfomation_Extend` | 522 | 是否扩展魔物名称能展现的信息, 比如体型、种族、属性 [Sola丶小克 改进] |
| 121 | `Pandas_Packet_Obfuscation_Keys` | 525 | 是否加强 2013-12-23 以及 2013-08-07 客户端的混淆密钥 [Sola丶小克] |
| 122 | `Pandas_Shadowgear_Support_Card` | 529 | 使影子装备可以支持插卡, 而不会被强制转换成普通道具 [Sola丶小克] 也使得卡片可以设置为可插入到影子装备, 而不会被系统判定为无效道具, 被变成杂货物品(IT_ETC) |
| 123 | `Pandas_Item_Properties` | 538 | 此选项开启后 (item_properties.yml) 数据库中以下选项才能发挥作用: Property 节点的 &1 = 避免物品被玩家主动使用而消耗 Property 节点的 &2 = 避免物品被作为发动技能的必要道具而消耗 |
| 124 | `Pandas_Item_Amulet_System` | 544 | 是否启用护身符系统 [Sola丶小克] 此选项开启后 (item_properties.yml) 数据库中以下选项才能发挥作用: Property 节点的 &4 = 该道具为护身符道具 |
| 125 | `Pandas_Item_ControlViewID` | 553 | （需回查原始碼區塊） |
| 126 | `Pandas_Item_Special_Annouce` | 562 | AnnouceRules 节点的 &1 - 打死魔物, 魔物将道具掉落到地上时公告 AnnouceRules 节点的 &2 - 打死魔物, 掉落 MVP 奖励到玩家的背包时公告 AnnouceRules 节点的 &4 - 使用"偷窃"技能, 从魔物身上偷到物品时公告 |
| 127 | `Pandas_Support_Pointshop_Variable_DisplayName` | 566 | 使 pointshop 类型的商店能支持指定变量别名, 用于展现给玩家 [Sola丶小克] |
| 128 | `Pandas_Make_Tomb_Mobname_Follow_Override_Mob_Names` | 569 | 使墓碑中的魔物名称能尊重 override_mob_names 战斗配置选项的设置 [Sola丶小克] |
| 129 | `Pandas_Deploy_Import_Directories` | 572 | 检测 import 目录是否存在, 若不存在能够从 import-tmpl 复制一份 [Sola丶小克] |
| 130 | `Pandas_SQL_Configure_Optimization` | 613 | -------------------------------------- 改动三：用 mysql_set_character_set 来设置 MySQL 的编码字符集 -------------------------------------- |
| 131 | `Pandas_Character_Title_Controller` | 616 | 是否启用一列用于控制角色称号的指令、事件等等 [Sola丶小克] |
| 132 | `Pandas_Console_Charset_SmartConvert` | 639 | 可以通过 export LANG="zh_TW.utf8" 这样的方式来临时切换编码进行测试 使用 locale -a 可以观察本机可以启用的编码, 如若类似 zh_CN.utf8 等选项不在返回值中, 那么说明你的系统没有安装中文语言包, 不同的 Linux 发行版安装中文语言包的方法各有不同, 请上网查阅 |
| 133 | `Pandas_MySQL_SSL_Mode_Disabled` | 649 | （需回查原始碼區塊） |
| 134 | `Pandas_Player_Suspend_System` | 658 | 是否启用玩家挂起子系统 (在原来离线挂店的基础上, 额外新增两种不同类型的挂起方式) 方式一: @suspend - 离线挂机, 角色在游戏内将永久在线 方式二: @afk - 离开模式, 角色头上会顶一个 AFK 帽子并坐到地上 上述这两种方式都是 autotrade 的拓展, 因此需要依赖 Pandas_Struct_Autotrade_Extend 的调整 |
| 135 | `Pandas_Guild_Extension_Configure` | 663 | 使公会的初始化人数以及“扩充组合体制”(GD_EXTENSION)每级增加人数可被宏定义 [Sola丶小克] 拓展出来两个宏: GUILD_INITIAL_MEMBER(初始化人数) 和 GUILD_EXTENSION_PERLEVEL (扩充组合体制每级增加人数) |
| 136 | `Pandas_Support_Transfer_Autotrade_Player` | 671 | 此选项依赖以下拓展, 任意一个不成立则将会 undef 此选项的定义 - Pandas_Struct_Map_Session_Data_MultiTransfer - Pandas_Struct_Map_Session_Data_Autotrade_Configure - Pandas_Struct_Map_Session_Data_Skip_LoadEndAck_NPC_Event_Dequeue |
| 137 | `Pandas_Adaptive_Importing_Message_Database` | 686 | （需回查原始碼區塊） |
| 138 | `Pandas_Setup_Console_Output_Codepage` | 694 | （需回查原始碼區塊） |
| 139 | `Pandas_Extract_SSOPacket_MacAddress` | 704 | 已知在 20180620 客户端中, 当本机有多个网络连接的时候, 只会读取第一个网络连接的 IP 地址 而第一个网络连接的 IP 不一定是真正联网通讯用的 IP 地址, 因此只能作为一个不完全可靠的特征来参考 经过简单测试, MAC 地址是可靠的, 但据 Jian916 提醒可能部分用户会无法读取到 MAC 地址 读取不到的情况暂时无法模拟出来, 等待进一步的情报 |
| 140 | `Pandas_Persistence_Itemdb_Script` | 709 | （需回查原始碼區塊） |
| 141 | `Pandas_Aura_Mechanism` | 715 | 是否启用角色光环机制 [Sola丶小克] 此选项依赖以下拓展, 任意一个不成立则将会 undef 此选项的定义 - Pandas_Struct_Unit_CommonData_Aura |
| 142 | `Pandas_Extreme_Computing` | 730 | - 将可能会导致计算时溢出的变量类型进行提升 例如: 在进行 cardfix 等 bonus 计算时由于变量类型限制带来的溢出或瓶颈 - 解除角色或其他拥有六维属性的单位的加点上限 默认的六维属性最大上限是 32767, 解除之后理论可达到 0x7FFFFFFF |
| 143 | `Pandas_BattleRecord` | 735 | （需回查原始碼區塊） |
| 144 | `Pandas_BonusScript_Unique_ID` | 742 | 是否启用 bonus_script 的唯一编号机制 [Sola丶小克] 此选项依赖以下拓展, 任意一个不成立则将会 undef 此选项的定义 - Pandas_Struct_BonusScriptData_Extend - Pandas_Struct_Map_Session_Data_BonusScript_Counter |
| 145 | `Pandas_Health_Monitors_Silent` | 759 | 以及他们频繁访问我们的游戏服务器, 导致我们将他们判定为发起了 DDoS 攻击的提示信息. 启用此选项后, 我们将支持在 packet_athena.conf 中设置这些健康检查的服务器 IP 区段 在不影响他们对我们正常服务器进行探测的情况下, 不再显示出大量无价值信息到终端干扰游戏管理员观察服务器状态. |
| 146 | `Pandas_Unlock_Storage_Capacity_Limit` | 767 | 注意事项: 如果对仓库容量有扩充需求, 应该优先考虑开设多个仓库, 而不是提高单个仓库的容量, 因为过大的容量在每次打开仓库或者背包的时候会带来客户端有些卡顿的感觉 (服务端送来超多内容然后客户端填充他们) |
| 147 | `Pandas_Persistent_SetUnitData_For_Monster_StatusData` | 772 | （需回查原始碼區塊） |
| 148 | `Pandas_Update_NPC_Identity_Information` | 777 | 是否扩展 e_job_types 枚举类型的可选值 [Sola丶小克] 此项目会影响默认可用的 NPC 外观数量, 提取自客户端 npcidentity.lub 文件 |
| 149 | `Pandas_Support_Future_Execution` | 783 | 是否支持 future 封装以便执行异步任务 [Sola丶小克] 此功能由 inhyositsu <inhyositsu@gmail.com> 实现, 后续由 Sola丶小克 进行微调并汇入熊猫模拟器 |
| 150 | `Pandas_Fix_ShadowChaser_Lose_Skill` | 803 | 实际上抄袭和复制到的技能并不需要被写入到 skill 表, 而是记录在变量中 抄袭对应的技能编号保存在变量: SKILL_VAR_PLAGIARISM 等级是 SKILL_VAR_PLAGIARISM_LV 复制对应的技能编号保存在变量: SKILL_VAR_REPRODUCE 等级是 SKILL_VAR_REPRODUCE_LV |
| 151 | `Pandas_Ease_Mob_Stuck_After_Dead` | 840 | 确定且经过验证的解决方案: 魔物只要死亡就立刻停止移动 (感谢 "Mr.Siu" 提供环境配合验证) 可能还会有其他情况导致类似的事情发生, 碰见再具体分析 |
| 152 | `Pandas_Fix_Potential_Arithmetic_Overflow` | 843 | 修正潜在可能存在算术溢出的情况 [Sola丶小克] |
| 153 | `Pandas_Fix_Ignore_sscanf_Return_Value` | 846 | 修正未判断 sscanf 返回值可能导致程序工作不符合预期的问题 [Sola丶小克] |
| 154 | `Pandas_Fix_GuildEmblem_Update` | 849 | 修正在部分情况下角色公会图标刷新不及时的问题 [Sola丶小克] |
| 155 | `Pandas_Fix_Clif_MVP_Exp_Type_Conversion` | 852 | 修正当 PACKETVER 小于 20131223 出现的 clif_mvp_exp 类型转换错误 [Sola丶小克] |
| 156 | `Pandas_Fix_Chinese_Character_Trimmed` | 856 | 修正部分简体、繁体中文字符作为角色名时, 会被变成问号的问题 [Sola丶小克] 例如: "凯撒"中的"凯"字, "聽風"中的"聽"字等 |
| 157 | `Pandas_Fix_Duplicate_Shop_With_FullyShopItemList` | 861 | 修正使用 duplicate 或 copynpc 复制商店类型的 NPC 时, 由于没有完整的复制出售的商品列表, 导致使用 npcshop* 系列指令调整复制后的商店内容时, 原商店的内容也会同步受到影响的问题. 目前根据各位脚本大神的反馈, 更希望各个商店 NPC 的商品列表内容是各自独立的 [Sola丶小克] |
| 158 | `Pandas_Fix_NPC_Filepath_WhiteSpace_Effects` | 865 | 修正 npc_unloadfile 和 npc_parsesrcfile 的行为会被空格影响的问题 [Sola丶小克] 如果 @reloadnpc 时给定的路径带空格, 系统将无法正确的 unloadnpc, 导致 npc 重复出现 |
| 159 | `Pandas_Fix_SkillDB_ItemCost_NoexistsItem_Crash` | 869 | 修正 skill_db.yml 的 ItemCost 字段指定的 Item 道具不存在时 会导致地图服务器直接崩溃的问题. 看代码应该是 rAthena 的工程师手误了 [Sola丶小克] |
| 160 | `Pandas_Fix_Autotrade_HeadView_Missing` | 872 | 修正离线挂店的角色在服务器重启自动上线后, 头饰外观会暂时丢失的问题 [Sola丶小克] |
| 161 | `Pandas_Fix_Char_FromSql_NextRow_Result_Logic` | 876 | 修正角色服务器加载不存在的角色信息时, 由于返回值判断错误而导致流程继续执行的问题 [Sola丶小克] 例如: 当离线挂店/挂机角色由于各种意外不存在于 char 表里面时, 就会触发误判 |
| 162 | `Pandas_Fix_LoadEndAck_Pet_Return_To_Egg_Missing` | 880 | 修正在 20180620 客户端中, 如果在玩家过图时将宠物变回宠物蛋, 背包中对应的宠物蛋没有出现的问题 (pet_disable_in_gvg 战斗配置选项) [Sola丶小克] |
| 163 | `Pandas_Fix_Same_Coordinate_Move_Logic` | 901 | 临时方案: 在 unit_walktoxy_sub 函数中, 如果发现当前坐标和目的地坐标一致, 那么放弃移动. 但问题更本质的原因是: 为什么会出现这样的情况... |
| 164 | `Pandas_Fix_Dungeon_Command_Status_Refresh` | 906 | （需回查原始碼區塊） |
| 165 | `Pandas_Fix_DuplicateBlock_When_Freeblock_Unlock` | 910 | 修正当 block_free 数组中存在重复指针时, 会导致的无效指针错误的问题 [Sola丶小克] |
| 166 | `Pandas_Fix_MagicalBullet_Damage_Overflow` | 915 | 修正复兴后 "魔术子弹"(GS_MAGICALBULLET) 的伤害溢出问题 [Sola丶小克] 处于该状态下若攻击者的 matk_min 小于被攻击者的 mdef 则会导致 这一次普攻出现计算溢出的情况, 可以秒杀一切 BOSS |
| 167 | `Pandas_Fix_Csv2Yaml_Extra_Slashes_In_The_Path` | 918 | 修正 csv2yaml 辅助工具可能存在的多余反斜杠问题 [Sola丶小克] |
| 168 | `Pandas_Fix_Yaml2Sql_NoBodyNode_Break` | 922 | 修正 yaml2sql 辅助工具无法生成不含 Body 节点的空 sql 问题 [Sola丶小克] 当来源文件不存在 Body 节点时, 应认为数据为空而生成空 sql 文件, 而不是直接放弃生成 |
| 169 | `Pandas_Fix_Duplicate_Channel_Name_Make_MemoryLeak` | 926 | 修正频道系统出现频道重名时, 没有进行严格校验, 导致地图服务器结束时会提示存在内存泄露的问题 [Sola丶小克] |
| 170 | `Pandas_Fix_MagicDecoy_Twice_Deduction_Of_Ore` | 929 | 修正 FAW 魔法傀儡 (技能编号: 2282) 重复扣减原石碎片的问题 [Sola丶小克] |
| 171 | `Pandas_Fix_Progressbar_Abort_Stuck` | 936 | 可能的现象: - 在 progressbar 期间使用 @load 或 @jump 会导致角色传送后无法移动 - 在 progressbar 之前使用了 menu / select 会导致打断进度条后角色无法移动 |
| 172 | `Pandas_Fix_Progressbar_Refresh_Stuck` | 939 | 修正 progressbar 期间使用 @refresh 或 @refreshall 会导致角色无法移动的问题 [Sola丶小克] |
| 173 | `Pandas_Fix_When_Relogin_Then_Clear_Autotrade_Store` | 944 | 修正挂店中的角色被临时踢下线后, 如果趁着地图服务器还未重启而直接进入游戏 并对手推车中原先离线摆摊的商品进行增删操作, 可能会导致下次地图服务器启动时出现 vending_reopen 错误 3 的情况, 更严重的甚至在下次重启地图服务器后出现离线挂店的商品与价格的错位 [Sola丶小克] |
| 174 | `Pandas_Fix_Mail_ItemAttachment_Check` | 950 | （需回查原始碼區塊） |
| 175 | `Pandas_Fix_Cloak_Status_Baffling` | 956 | （需回查原始碼區塊） |
| 176 | `Pandas_Fix_Storage_DirtyFlag_Override` | 967 | - 编写一个脚本, 调用 atcommand("@clearstorage"); 之后立刻调用 storagegetitem 501,1; - 执行上述脚本后立刻小退, 重复多次 - 观察每次角色进入地图服务器时, 角色服务器提示加载到的仓库物品数量 - 如果角色服务器在保存仓库数据时比较慢, 那么你会看到反复小退仓库的数量是: 1、0、1、0... |
| 177 | `Pandas_Fix_Guild_Storage_Log_Escape_For_CharName` | 977 | - 加入公会, 开启公会仓库, 存入物品 - 此时地图服务器在写入 guild_storage_log 的时候将抛出错误 感谢 "小林" 反馈此问题 |
| 178 | `Pandas_Fix_GainExp_Display_Overflow` | 981 | 修正使用 @showexp 指令后呈现的经验值数值会错误的问题 [Sola丶小克] 备注: 单次获得的经验超过 long 的有效阈值范围后就会溢出成负数, 但最新的有效经验值区间是 int64 |
| 179 | `Pandas_Fix_INTER_SERVER_DB_Field_Verify` | 985 | 修正 inter_server.yml 中的 Max 超大时没有妥善处理的问题 [Sola丶小克] 启用后 Max 字段的值最多不能超过 MAX_STORAGE 的值 |
| 180 | `Pandas_Fix_Bonus_Script_Effective_Timing_Exception` | 997 | 但如果在包含 BSF_REM_ON_LOGOUT 的 bonus_script 记录在数据库时强制关闭地图服务器, 那么这条 bonus_script 将会保存到下次服务器启动, 并且玩家进入游戏时还有效. 解决方案: 进入游戏加载 bonus_script 的时候抛弃拥有 BSF_REM_ON_LOGOUT 标记位的数据 |
| 181 | `Pandas_Fix_Sprintf_ScriptCommand_Unsupport_Int64` | 1001 | 修正 sprintf 脚本指令无法格式化 int64 数值的问题 [Sola丶小克] 注意: 即使启用此选项, 当你需要格式化 int64 的数值时依然需要使用 %lld 而不是 %d |
| 182 | `Pandas_Fix_SetUnitData_Forget_Reset_After_Monster_Dead` | 1016 | 已知 UMOB_MASTERAID 在 mob_spawn 中故意不重置 特别感谢 "差记性的小北" 指出此问题 |
| 183 | `Pandas_Fix_Prompt_Cancel_Combine_Close_Error` | 1022 | 修正玩家在 prompt 菜单中选择取消后, 后续脚本中若调用 close 系列指令会导致报错的问题 [Sola丶小克] 特别感谢 "差记性的小北" 指出此问题 |
| 184 | `Pandas_Fix_ScriptControl_Shop_Missing_NpcID_Error` | 1029 | 只要在 npcshopattach + callshop 之前调用了一个 mes 并且不 close 它, 那么当玩家完成商店中的交易操作后就会出现 npc_scriptcont 报错. 特别感谢 "HongShin" 指出此问题 |
| 185 | `Pandas_Fix_Use_SQL_DB_Make_Terminal_Show_Null` | 1032 | 修正启用 use_sql_db 之后终端加载信息出现来源数据表为 (null) 的问题 [Sola丶小克] |
| 186 | `Pandas_Fix_ClearArray_The_First_Element_Is_Ignored` | 1036 | 修正 script_cleararray_pc 无法清空单元素数组的问题 [Sola丶小克] 特别感谢 "最美的Secret" 指出此问题 |
| 187 | `Pandas_Fix_StealItem_Formula_Overflow` | 1043 | 只要 sd_status->dex 和 md_status->dex 的类型是无符号数值并且两者相减出现负数, 那么最终计算出来的概率值因为出现 "回绕" 而变得很大, 结果等于偷窃必定成功. 特别感谢 "最美的Secret" 指出此问题 |
| 188 | `Pandas_Crashfix_Variable_Init` | 1053 | 对部分比较关键的变量初始化时进行置空处理 [Sola丶小克] 特别针对那些单纯依赖目标是否为 Null 作为野指针判断的相关变量 |
| 189 | `Pandas_Crashfix_Use_NullptrCheck_In_ReleaseMode` | 1060 | 在 rAthena 的设计中, nullpo_ret 等指令仅在 Debug 模式会拦截空指针的情况并记录下位置信息 为了健壮性考虑, 熊猫模拟器会试图在 Release 模式下也使这些指令可以拦截空指针的情况 因为有些空指针时在运行时产生的, 日常测试非常难以覆盖到这些异常情况 若未来在生产环境执行过程中也碰到了空指针错误, 可考虑尝试上报到服务端进行统计分析 |
| 190 | `Pandas_Crashfix_FunctionParams_Verify` | 1063 | 对函数的参数进行合法性校验 [Sola丶小克] |
| 191 | `Pandas_Crashfix_Prevent_NullPointer` | 1066 | 对潜在的空指针调用崩溃情况进行校验和判断 [Sola丶小克] |
| 192 | `Pandas_Crashfix_Divide_by_Zero` | 1069 | 对除数可能为零的情况进行一些规避处理 [Sola丶小克] |
| 193 | `Pandas_Crashfix_ScriptCommand_Summon` | 1072 | 在 summon 生成魔物前校验完整编号，避免无效编号截断后变成其他魔物 |
| 194 | `Pandas_Crashfix_ScriptCommand_Getd_And_Setd` | 1079 | 若 getd 的结果直接作为参数传入其他脚本指令, 会导致地图服务器崩溃的问题 [Sola丶小克] 重现方法: 使 NPC 调用 .@result = inarray(getd(" $test"), 100); 即可触发崩溃 |
| 195 | `Pandas_Crashfix_VisualStudio_UnorderedMap_AVX512` | 1091 | 此修复只对 _MSC_VER == 1923 的 Visual Studio 编译器有效 (对应 Visual Studio 2019 16.3 版本) https://developercommunity.visualstudio.com/content/problem/787296/vs2019-163-seems-to-incorrectly-detect-avx512-on-w.html 感谢"李小狼"在阿里云服务器上暴露此问题, 并提供调试环境 |
| 196 | `Pandas_Crashfix_Unloadnpc_In_Event` | 1099 | 这会导致 npc_script_event 中提前获取的 vector 引用所指向的内容被清空, 以至于在执行下一轮循环的时候, 无法获取已经被清空的原 script_event 内容, 而触发崩溃 感谢"聽風"指出重现此问题的条件和环境 |
| 197 | `Pandas_Crashfix_ScriptCommand_Delchar` | 1103 | 修正 delchar 指令可能会导致地图服务器崩溃的问题 [Sola丶小克] 会导致崩溃的示例脚本: .@m$ = delchar("", 0); |
| 198 | `Pandas_Crashfix_BossMapinfo` | 1106 | 修正 SC_BOSSMAPINFO 会导致地图服务器崩溃的问题 [Sola丶小克] |
| 199 | `Pandas_Crashfix_UnorderedMap_Erase` | 1111 | （需回查原始碼區塊） |
| 200 | `Pandas_Crashfix_EventDatabase_Clean_Synchronize` | 1116 | 修正释放或删除 ev_db 时, 对应的 script_event 节点没清空的问题 [Sola丶小克] 在 reloadscript 时可能会因为 ev_db 被清空, 其他环节直接使用 script_event 的值而崩溃 |
| 201 | `Pandas_Crashfix_RouletteData_UnInit` | 1120 | 修正在未开启大乐透功能的情况下启动服务端, 再重新打开大乐透功能 并用 @reloadbattleconf 使之立刻生效之后, 点击大乐透按钮会导致地图服务器崩溃的问题 [Sola丶小克] |
| 202 | `Pandas_Crashfix_ScriptFreeCode_SetPointerNull` | 1137 | reloaditemdb -> item_db.reload(); -> 触发每一个 item_data 的析构函数 (destruct function) -> script_free_code 释放掉 script/equip_script/unequip_script 的 script_code 但是释放后没有将对应的指针设为 NULL. 导致上述重现步骤中 script_free_state 函数针对 st->script->local.vars 和 st->script->local.arrays 的空指针判断被绕过, 继而触发崩溃 |
| 203 | `Pandas_Crashfix_PC_Setpos_With_Invaild_Player` | 1147 | - 玩家与其对话然后立刻下线, 时间到之后会触发 warp 指令并导致崩溃 因为触发 atcommand 的时候角色已经下线, 因此 atcommand_sub 会生成一个 dummy_sd 来替代, 而 dummy_sd 并非真实存在的 sd 对象, 最后会导致地图服务器崩溃 |
| 204 | `Pandas_Crashfix_GetInstanceVar_Invaild_InstanceID` | 1150 | 修正 getinstancevar 传递无效的副本编号会导致地图服务器崩溃的问题 [Sola丶小克] |
| 205 | `Pandas_Crashfix_SetInstanceVar_Invaild_InstanceID` | 1153 | 修正 setinstancevar 传递无效的副本编号会导致地图服务器崩溃的问题 [Sola丶小克] |
| 206 | `Pandas_Crashfix_Invaild_Script_Code` | 1163 | 如果在脚本恢复执行之前, 就因为其他原因把整个脚本释放掉, 就会在恢复执行脚本的时候导致地图服务器崩溃. 具体: 从 run_script_timer 恢复进入 run_script_main 之后崩溃 至于什么地方会在脚本还没恢复执行之前就将 script_code 释放暂时还没有特别明确的线索 |
| 207 | `Pandas_Crashfix_MapBlock_Operation` | 1166 | 规避在 map_addblock 和 map_delblock 因检查不严而导致崩溃的问题 [Renee] |
| 208 | `Pandas_Crashfix_Laphine_Synthesis_Without_DelayConsume` | 1170 | 避免非 DelayConsume 类型的道具在使用脚本中调用 laphine_synthesis 脚本指令时, 当最后一个物品被消耗时会导致地图服务器崩溃的问题 [Sola丶小克] |
| 209 | `Pandas_Crashfix_Laphine_Upgrade_Without_DelayConsume` | 1174 | 避免非 DelayConsume 类型的道具在使用脚本中调用 laphine_upgrade 脚本指令时, 当最后一个物品被消耗时会导致地图服务器崩溃的问题 [Sola丶小克] |
| 210 | `Pandas_Speedup_Print_TimeConsuming_Of_KeySteps` | 1183 | 是否在一些关键耗时节点打印出耗时情况 [Sola丶小克] |
| 211 | `Pandas_Speedup_Map_Read_From_Cache` | 1193 | 优化后性能表现参考信息 (VS2019 + Win32) -------------------------------------------------------------- 在 Debug 模式下越提速约 1.79 倍 (3350ms -> 1200ms) 在 Release 模式下提速约 17.65% (1000ms -> 850ms) |
| 212 | `Pandas_Speedup_Loading_Map_Status_Restrictor` | 1205 | （需回查原始碼區塊） |
| 213 | `Pandas_Speedup_Unloadnpc_Without_Refactoring_ScriptEvent` | 1222 | （需回查原始碼區塊） |
| 214 | `Pandas_Speedup_Constant_References` | 1226 | 通过微调程序逻辑改善 C26817 这样的常量引用性能优化场景 [Sola丶小克] |
| 215 | `Pandas_ScriptEngine_Express` | 1235 | 使脚本引擎能够支持穿越事件队列机制, 直接执行某些事件 [Sola丶小克] |
| 216 | `Pandas_ScriptEngine_AddStr_Realloc_Memory` | 1244 | 性能表现参考信息 -------------------------------------------------------------- - 调整前 str_buf 需要被重新分配 1174 次, 调整后为 37 次 - 调整前 str_data 需要被重新分配 185 次, 调整后为 47 次 |
| 217 | `Pandas_ScriptEngine_MutliStackBackup` | 1248 | 使脚本引擎能够支持备份无数个脚本堆栈 [Sola丶小克] 以此避免嵌套调用超过两层的脚本会导致程序崩溃的问题 (如: script4each -> getitem -> 成就系统) |
| 218 | `Pandas_ScriptEngine_DoubleByte_UnEscape_Detection` | 1273 | 但实际上此时的反斜杠和下一个字符的 " 构成的 \" 才是真正的一组转义序列, 如果认为 p 是独立反斜杠, 那么 " 也将被独立, 不再成为转义序列的一部分. 从而提前关闭第一个双引号, 原计划输出的 "中文" 输出将变成: "中文 而最末末尾的 " 将被作为一个新的字符串起点, 导致语法检测双引号无法闭合而报错 |
| 219 | `Pandas_ScriptEngine_Relocation_Funcname_After_StrBuf_Realloc` | 1277 | 修正 add_str 触发 str_buf 的扩容分配后 st->funcname 的所指向的指令名称无效的问题, 因为 st->funcname 指针指向的内存已在扩容分配时被释放 [Sola丶小克] |
| 220 | `Pandas_Redeclaration_Struct_Event_Data` | 1286 | 将 struct event_data 的定义从 npc.cpp 移动到 npc.hpp [Sola丶小克] |
| 221 | `Pandas_UserExperience_AtCommand_Version` | 1295 | 优化使用 @version 指令的回显信息 [Sola丶小克] |
| 222 | `Pandas_UserExperience_Yaml2Sql_LoadFile_Tips` | 1299 | 使 yaml2sql 辅助工具在加载 YAML 文件时能给个提示 否则容易因加载时间过长, 给使用者造成程序已经卡死的错觉 [Sola丶小克] |
| 223 | `Pandas_UserExperience_Yaml2Sql_AskConfirmation_Order` | 1303 | 调整 yaml2sql 辅助工具的询问确认流程 [Sola丶小克] 先询问是否能覆盖目标文件, 再尝试去加载来源数据文件, 以便优化体验 |
| 224 | `Pandas_UserExperience_Yaml2Sql_SaveFile_Location` | 1306 | 调整 Yaml2sql 辅助工具在发布版本中的文件保存位置 [Sola丶小克] |
| 225 | `Pandas_UserExperience_Move_BartersYml_To_DB` | 1309 | 将 barters.yml 数据库从 npc 目录移动回 db 目录 [Sola丶小克] |
| 226 | `Pandas_UserExperience_Yaml_Error` | 1312 | 优化加载与解析 YAML 文件时出现的一些报错体验 [Sola丶小克] |
| 227 | `Pandas_UserExperience_Output_Ending_Even_Body_Node_Is_Not_Exists` | 1315 | 当 YAML 数据文件中不存在 Body 节点时也依然输出结尾信息 [Sola丶小克] |
| 228 | `Pandas_UserExperience_AutoCreate_Generated_Directory` | 1318 | 使 map-server-generator 能在运行时按需自动创建输出目录 [Sola丶小克] |
| 229 | `Pandas_UserExperience_Rewrite_MapServerGenerator_Args_Process` | 1321 | 改写 map-server-generator 的参数处理流程, 支持短参数以及输出帮助 [Sola丶小克] |
| 230 | `Pandas_UserExperience_MapServerGenerator_Output` | 1324 | 优化 map-server-generator 的输出信息 [Sola丶小克] |
| 231 | `Pandas_UserExperience_Linux_Ctrl_C_WarpLine` | 1328 | （需回查原始碼區塊） |
| 232 | `Pandas_UserExperience_Debug_Hide_SubnetInfo` | 1332 | 在 Debug 模式下隐藏玩家数据流转的子网掩码调试信息 [Sola丶小克] |
| 233 | `Pandas_Cleanup_Useless_Message` | 1341 | 清理掉一些没啥作用看着还心烦的终端提示信息 [Sola丶小克] |
| 234 | `Pandas_NpcFilter_IDENTIFY` | 1357 | 当玩家在装备鉴定列表中选择好装备, 并点击“确定”按钮时触发过滤器 [Sola丶小克] 事件类型: Filter / 事件名称: OnPCIdentifyFilter 常量名称: NPCF_IDENTIFY / 变量名称: identify_filter_name |
| 235 | `Pandas_NpcFilter_ENTERCHAT` | 1362 | 当玩家进入 NPC 开启的聊天室时触发过滤器 [Sola丶小克] 事件类型: Filter / 事件名称: OnPCInChatroomFilter 常量名称: NPCF_ENTERCHAT / 变量名称: enterchat_filter_name |
| 236 | `Pandas_NpcFilter_INSERT_CARD` | 1367 | 当玩家准备插入卡片时触发过滤器 [Sola丶小克] 事件类型: Filter / 事件名称: OnPCInsertCardFilter 常量名称: NPCF_INSERT_CARD / 变量名称: insert_card_filter_name |
| 237 | `Pandas_NpcFilter_USE_ITEM` | 1372 | 当玩家准备使用非装备类道具时触发过滤器 [Sola丶小克] 事件类型: Filter / 事件名称: OnPCUseItemFilter 常量名称: NPCF_USE_ITEM / 变量名称: use_item_filter_name |
| 238 | `Pandas_NpcFilter_USE_SKILL` | 1377 | 当玩家准备使用技能时触发过滤器 [Sola丶小克] 事件类型: Filter / 事件名称: OnPCUseSkillFilter 常量名称: NPCF_USE_SKILL / 变量名称: use_skill_filter_name |
| 239 | `Pandas_NpcFilter_ROULETTE_OPEN` | 1382 | 当玩家准备打开乐透大转盘的时候触发过滤器 [Sola丶小克] 事件类型: Filter / 事件名称: OnPCOpenRouletteFilter 常量名称: NPCF_ROULETTE_OPEN / 变量名称: roulette_open_filter_name |
| 240 | `Pandas_NpcFilter_VIEW_EQUIP` | 1387 | 当玩家准备查看某个角色的装备时触发过滤器 [Sola丶小克] 事件类型: Filter / 事件名称: OnPCViewEquipFilter 常量名称: NPCF_VIEW_EQUIP / 变量名称: view_equip_filter_name |
| 241 | `Pandas_NpcFilter_EQUIP` | 1392 | 当玩家准备穿戴装备时触发过滤器 [Sola丶小克] 事件类型: Filter / 事件名称: OnPCEquipFilter 常量名称: NPCF_EQUIP / 变量名称: equip_filter_name |
| 242 | `Pandas_NpcFilter_UNEQUIP` | 1397 | 当玩家准备脱下装备时触发过滤器 [Sola丶小克] 事件类型: Filter / 事件名称: OnPCUnequipFilter 常量名称: NPCF_UNEQUIP / 变量名称: unequip_filter_name |
| 243 | `Pandas_NpcFilter_CHANGETITLE` | 1403 | 当玩家试图变更称号时将触发过滤器 [Sola丶小克] 事件类型: Filter / 事件名称: OnPCChangeTitleFilter 常量名称: NPCF_CHANGETITLE / 变量名称: changetitle_filter_name |
| 244 | `Pandas_NpcFilter_SC_START` | 1409 | 当玩家准备获得一个状态(Buff)时触发过滤器 [Sola丶小克] 事件类型: Filter / 事件名称: OnPCBuffStartFilter 常量名称: NPCF_SC_START / 变量名称: sc_start_filter_name |
| 245 | `Pandas_NpcFilter_USE_REVIVE_TOKEN` | 1414 | 当玩家使用菜单中的原地复活之证时触发过滤器 [Sola丶小克] 事件类型: Filter / 事件名称: OnPCUseReviveTokenFilter 常量名称: NPCF_USE_REVIVE_TOKEN / 变量名称: use_revive_token_filter_name |
| 246 | `Pandas_NpcFilter_ONECLICK_IDENTIFY` | 1419 | 当玩家使用一键鉴定道具时触发过滤器 [Sola丶小克] 事件类型: Filter / 事件名称: OnPCUseOCIdentifyFilter 常量名称: NPCF_ONECLICK_IDENTIFY / 变量名称: oneclick_identify_filter_name |
| 247 | `Pandas_NpcFilter_GUILDCREATE` | 1424 | 当玩家准备创建公会时触发过滤器 [聽風] 事件类型: Filter / 事件名称: OnPCGuildCreateFilter 常量名称: NPCF_GUILDCREATE / 变量名称: guildcreate_filter_name |
| 248 | `Pandas_NpcFilter_GUILDJOIN` | 1429 | 当玩家即将加入公会时触发过滤器 [聽風] 事件类型: Filter / 事件名称: OnPCGuildJoinFilter 常量名称: NPCF_GUILDJOIN / 变量名称: guildjoin_filter_name |
| 249 | `Pandas_NpcFilter_GUILDLEAVE` | 1434 | 当玩家准备离开公会时触发过滤器 [聽風] 事件类型: Filter / 事件名称: OnPCGuildLeaveFilter 常量名称: NPCF_GUILDLEAVE / 变量名称: guildleave_filter_name |
| 250 | `Pandas_NpcFilter_PARTYCREATE` | 1439 | 当玩家准备创建队伍时触发过滤器 [聽風] 事件类型: Filter / 事件名称: OnPCPartyCreateFilter 常量名称: NPCF_PARTYCREATE / 变量名称: partycreate_filter_name |
| 251 | `Pandas_NpcFilter_PARTYJOIN` | 1444 | 当玩家即将加入队伍时触发过滤器 [聽風] 事件类型: Filter / 事件名称: OnPCPartyJoinFilter 常量名称: NPCF_PARTYJOIN / 变量名称: partyjoin_filter_name |
| 252 | `Pandas_NpcFilter_PARTYLEAVE` | 1449 | 当玩家准备离开队伍时触发过滤器 [聽風] 事件类型: Filter / 事件名称: OnPCPartyLeaveFilter 常量名称: NPCF_PARTYLEAVE / 变量名称: partyleave_filter_name |
| 253 | `Pandas_NpcFilter_DROPITEM` | 1454 | 当玩家准备丢弃或掉落道具时触发过滤器 [人鱼姬的思念] 事件类型: Filter / 事件名称: OnPCDropItemFilter 常量名称: NPCF_DROPITEM / 变量名称: dropitem_filter_name |
| 254 | `Pandas_NpcFilter_CLICKTOMB` | 1459 | 当玩家点击魔物墓碑时触发过滤器 [人鱼姬的思念] 事件类型: Filter / 事件名称: OnPCClickTombFilter 常量名称: NPCF_CLICKTOMB / 变量名称: clicktomb_filter_name |
| 255 | `Pandas_NpcFilter_STORAGE_ADD` | 1464 | 当玩家准备将道具存入仓库时触发过滤器 [香草] 事件类型: Filter / 事件名称: OnPCStorageAddFilter 常量名称: NPCF_STORAGE_ADD / 变量名称: storage_add_filter_name |
| 256 | `Pandas_NpcFilter_STORAGE_DEL` | 1469 | 当玩家准备将道具取出仓库时触发过滤器 [香草] 事件类型: Filter / 事件名称: OnPCStorageDelFilter 常量名称: NPCF_STORAGE_DEL / 变量名称: storage_del_filter_name |
| 257 | `Pandas_NpcFilter_CART_ADD` | 1474 | 当玩家准备将道具从背包存入手推车时触发过滤器 [香草] 事件类型: Filter / 事件名称: OnPCCartAddFilter 常量名称: NPCF_CART_ADD / 变量名称: cart_add_filter_name |
| 258 | `Pandas_NpcFilter_CART_DEL` | 1479 | 当玩家准备将道具从手推车取回背包时触发过滤器 [香草] 事件类型: Filter / 事件名称: OnPCCartDelFilter 常量名称: NPCF_CART_DEL / 变量名称: cart_del_filter_name |
| 259 | `Pandas_NpcFilter_FAVORITE_ADD` | 1484 | 当玩家准备将道具移入收藏栏位时触发过滤器 [香草] 事件类型: Filter / 事件名称: OnPCFavoriteAddFilter 常量名称: NPCF_FAVORITE_ADD / 变量名称: favorite_add_filter_name |
| 260 | `Pandas_NpcFilter_FAVORITE_DEL` | 1489 | 当玩家准备将道具从收藏栏位移出时触发过滤器 [香草] 事件类型: Filter / 事件名称: OnPCFavoriteDelFilter 常量名称: NPCF_FAVORITE_DEL / 变量名称: favorite_del_filter_name |
| 261 | `Pandas_NpcEvent_KILLMVP` | 1500 | 当玩家杀死 MVP 魔物后触发事件 [Sola丶小克] 事件类型: Event / 事件名称: OnPCKillMvpEvent 常量名称: NPCE_KILLMVP / 变量名称: killmvp_event_name |
| 262 | `Pandas_NpcEvent_INSERT_CARD` | 1505 | 当玩家成功插入卡片后触发事件 [Sola丶小克] 事件类型: Event / 事件名称: OnPCInsertCardEvent 常量名称: NPCE_INSERT_CARD / 变量名称: insert_card_event_name |
| 263 | `Pandas_NpcEvent_USE_ITEM` | 1510 | 当玩家成功使用非装备类道具后触发事件 [Sola丶小克] 事件类型: Event / 事件名称: OnPCUseItemEvent 常量名称: NPCE_USE_ITEM / 变量名称: use_item_event_name |
| 264 | `Pandas_NpcEvent_USE_SKILL` | 1515 | 当玩家成功使用技能后触发事件 [Sola丶小克] 事件类型: Event / 事件名称: OnPCUseSkillEvent 常量名称: NPCE_USE_SKILL / 变量名称: use_skill_event_name |
| 265 | `Pandas_NpcEvent_EQUIP` | 1520 | 当玩家成功穿戴一件装备时触发事件 [Sola丶小克] 事件类型: Event / 事件名称: OnPCEquipEvent 常量名称: NPCE_EQUIP / 变量名称: equip_event_name |
| 266 | `Pandas_NpcEvent_UNEQUIP` | 1525 | 当玩家成功脱下一件装备时触发事件 [Sola丶小克] 事件类型: Event / 事件名称: OnPCUnequipEvent 常量名称: NPCE_UNEQUIP / 变量名称: unequip_event_name |
| 267 | `Pandas_NpcExpress_STATCALC` | 1539 | 常量名称: NPCE_STATCALC / 变量名称: statcalc_express_name 正常按照命名规范这个事件应该叫 NPCX_STATCALC 和 OnPCStatCalcExpress 但这个事件比较特殊, 之前 rAthena 官方出现过. 考虑到对老脚本的兼容, 继续沿用老的事件常量和名称 |
| 268 | `Pandas_NpcExpress_SC_END` | 1544 | 当玩家成功解除一个状态(Buff)后触发实时事件 [Sola丶小克] 事件类型: Express / 事件名称: OnPCBuffEndExpress 常量名称: NPCX_SC_END / 变量名称: sc_end_express_name |
| 269 | `Pandas_NpcExpress_SC_START` | 1549 | 当玩家成功获得一个状态(Buff)后触发实时事件 [Sola丶小克] 事件类型: Express / 事件名称: OnPCBuffStartExpress 常量名称: NPCX_SC_START / 变量名称: sc_start_express_name |
| 270 | `Pandas_NpcExpress_ENTERMAP` | 1554 | 当玩家进入或者改变地图时触发实时事件 [Sola丶小克] 事件类型: Express / 事件名称: OnPCEnterMapExpress 常量名称: NPCX_ENTERMAP / 变量名称: entermap_express_name |
| 271 | `Pandas_NpcExpress_PROGRESSABORT` | 1559 | 当 progressbar 进度条被打断时触发实时事件 [Sola丶小克] 事件类型: Express / 事件名称: OnPCProgressAbortExpress 常量名称: NPCX_PROGRESSABORT / 变量名称: progressabort_express_name |
| 272 | `Pandas_NpcExpress_UNIT_KILL` | 1564 | 当某个单位被击杀时触发实时事件 [Sola丶小克] 事件类型: Express / 事件名称: OnUnitKillExpress 常量名称: NPCX_UNIT_KILL / 变量名称: unit_kill_express_name |
| 273 | `Pandas_NpcExpress_MOBDROPITEM` | 1569 | 当魔物即将掉落道具时触发实时事件 [Sola丶小克] 事件类型: Express / 事件名称: OnMobDropItemExpress 常量名称: NPCX_MOBDROPITEM / 变量名称: mobdropitem_express_name |
| 274 | `Pandas_NpcExpress_PCATTACK` | 1574 | 当玩家发起攻击并即将进行结算时触发实时事件 [聽風] 事件类型: Express / 事件名称: OnPCAttackExpress 常量名称: NPCX_PCATTACK / 变量名称: pcattack_express_name |
| 275 | `Pandas_NpcExpress_MER_CALL` | 1579 | 当玩家成功召唤出佣兵时触发实时事件 [HongShin] 事件类型: Express / 事件名称: OnPCMerCallExpress 常量名称: NPCX_MER_CALL / 变量名称: mer_call_express_name |
| 276 | `Pandas_NpcExpress_MER_LEAVE` | 1584 | 当佣兵离开玩家时触发实时事件 [HongShin] 事件类型: Express / 事件名称: OnPCMerLeaveExpress 常量名称: NPCX_MER_LEAVE / 变量名称: mer_leave_express_name |
| 277 | `Pandas_NpcExpress_PC_TALK` | 1589 | 当玩家往聊天框发送信息时触发实时事件 [人鱼姬的思念] 事件类型: Express / 事件名称: OnPCTalkExpress 常量名称: NPCX_PC_TALK / 变量名称: pc_talk_express_name |
| 278 | `Pandas_NpcExpress_PCHARMED` | 1594 | 当玩家受到伤害并即将进行结算时触发实时事件 [人鱼姬的思念] 事件类型: Express / 事件名称: OnPCHarmedExpress 常量名称: NPCX_PCHARMED / 变量名称: pcharmed_express_name |
| 279 | `Pandas_MapFlag_MobInfo` | 1609 | （需回查原始碼區塊） |
| 280 | `Pandas_MapFlag_NoAutoLoot` | 1614 | 是否启用 noautoloot 地图标记 [Sola丶小克] 该标记用于在给定此标记的地图上禁止玩家使用自动拾取功能, 或使已激活的自动拾取功能失效 |
| 281 | `Pandas_MapFlag_NoToken` | 1618 | 是否启用 notoken 地图标记 [Sola丶小克] 该标记用于禁止玩家在指定的地图上使用“原地复活之证”道具 |
| 282 | `Pandas_MapFlag_NoCapture` | 1624 | （需回查原始碼區塊） |
| 283 | `Pandas_MapFlag_HideGuildInfo` | 1629 | 是否启用 hideguildinfo 地图标记 [Sola丶小克] 使当前地图上的玩家无法见到其他人的公会图标、公会名称、职位等信息 (自己依然可见) |
| 284 | `Pandas_MapFlag_HidePartyInfo` | 1633 | 是否启用 hidepartyinfo 地图标记 [Sola丶小克] 使当前地图上的玩家无法见到其他人的队伍名称 (自己依然可见) |
| 285 | `Pandas_MapFlag_NoMail` | 1637 | 是否启用 nomail 地图标记 [Sola丶小克] 该标记用于禁止玩家在地图上打开邮件界面或进行邮件系统的相关操作 |
| 286 | `Pandas_MapFlag_NoPet` | 1641 | 是否启用 nopet 地图标记 [Sola丶小克] 该标记用于禁止玩家在地图上召唤宠物, 宠物进入该地图会自动变回宠物蛋 |
| 287 | `Pandas_MapFlag_NoHomun` | 1645 | 是否启用 nohomun 地图标记 [Sola丶小克] 该标记用于禁止玩家在地图上召唤人工生命体, 生命体进入该地图会自动安息 |
| 288 | `Pandas_MapFlag_NoMerc` | 1649 | 是否启用 nomerc 地图标记 [Sola丶小克] 该标记用于禁止玩家在地图上召唤佣兵, 佣兵进入该地图会自动隐藏 |
| 289 | `Pandas_MapFlag_MobDroprate` | 1653 | 是否启用 mobdroprate 地图标记 [Sola丶小克] 该标记用于额外调整此地图上普通魔物的物品掉落倍率 |
| 290 | `Pandas_MapFlag_MvpDroprate` | 1657 | 是否启用 mvpdroprate 地图标记 [Sola丶小克] 该标记用于额外调整此地图上 MVP 魔物的物品掉落倍率 |
| 291 | `Pandas_MapFlag_MaxHeal` | 1661 | 是否启用 maxheal 地图标记 [Sola丶小克] 该标记用于限制此地图上单位的治愈系技能最大的 HP 治愈量 |
| 292 | `Pandas_MapFlag_MaxDmg_Skill` | 1665 | 是否启用 maxdmg_skill 地图标记 [Sola丶小克] 该标记用于限制此地图上单位的最大技能伤害 (不含治愈系技能) |
| 293 | `Pandas_MapFlag_MaxDmg_Normal` | 1669 | 是否启用 maxdmg_normal 地图标记 [Sola丶小克] 该标记用于限制此地图上单位的最大平砍伤害 (包括二刀连击和刺客拳刃平砍) |
| 294 | `Pandas_MapFlag_NoSkill2` | 1673 | 是否启用 noskill2 地图标记 [Sola丶小克] 该标记用于禁止此地图上的指定单位使用技能 (支持掩码指定多种类型的单位) |
| 295 | `Pandas_MapFlag_NoAura` | 1679 | （需回查原始碼區塊） |
| 296 | `Pandas_MapFlag_MaxASPD` | 1684 | 是否启用 maxaspd 地图标记 [Sola丶小克] 该标记用于限制此地图上单位的最大攻击速度 (ASDP: 1~199) |
| 297 | `Pandas_MapFlag_NoSlave` | 1688 | 是否启用 noslave 地图标记 [HongShin] 该标记用于禁止此地图上的魔物召唤随从 |
| 298 | `Pandas_MapFlag_NoBank` | 1692 | 是否启用 nobank 地图标记 [聽風] rAthena 官方已经实现此标记, 当前宏定义所包含的代码用于处理体验细节 |
| 299 | `Pandas_MapFlag_NoUseItem` | 1696 | 是否启用 nouseitem 地图标记 [HongShin] 该标记用于禁止玩家在地图上使用消耗型物品道具 |
| 300 | `Pandas_MapFlag_HideDamage` | 1700 | 是否启用 hidedamage 地图标记 [HongShin] 该标记用于隐藏此地图上任何攻击的实际伤害数值 (无论什么单位, 无论是否 MISS) |
| 301 | `Pandas_MapFlag_NoAttack` | 1704 | 是否启用 noattack 地图标记 [HongShin] 该标记用于禁止此地图上的任何单位进行普通攻击 |
| 302 | `Pandas_MapFlag_NoAttack2` | 1708 | 是否启用 noattack2 地图标记 [HongShin] 该标记用于禁止此地图上指定单位进行普通攻击 (支持掩码指定多种类型的单位) |
| 303 | `Pandas_AtCommand_RecallMap` | 1719 | 是否启用 recallmap 管理员指令 [Sola丶小克] 召唤当前(或指定)地图的玩家来到身边 (处于离线挂店模式的角色不会被召唤) |
| 304 | `Pandas_AtCommand_Crashtest` | 1723 | 是否启用 crashtest 管理员指令 [Sola丶小克] 执行崩溃测试, 在比较严格的环境上故意触发地图服务器崩溃 |
| 305 | `Pandas_AtCommand_Title` | 1728 | 是否启用 title 管理员指令 [Sola丶小克] 给角色设置一个指定的称号ID, 客户端封包版本大于等于 20150513 才可用 |
| 306 | `Pandas_AtCommand_Suspend` | 1733 | 是否启用 suspend 管理员指令 [Sola丶小克] 使角色进入离线挂机模式, 维持当前的全部状态 (朝向, 站立与否) |
| 307 | `Pandas_AtCommand_AFK` | 1737 | 是否启用 afk 管理员指令 [Sola丶小克] 使角色进入离开模式, 角色将会坐到地上并自动使用 AFK 头饰 (表示角色暂时离开) |
| 308 | `Pandas_AtCommand_Aura` | 1743 | （需回查原始碼區塊） |
| 309 | `Pandas_AtCommand_ReloadAuraDB` | 1750 | （需回查原始碼區塊） |
| 310 | `Pandas_AtCommand_ReloadLaphineDB` | 1755 | 是否启用 reloadlaphinedb 管理员指令 [Sola丶小克] 重新加载 Laphine 数据库 (laphine_synthesis.yml 和 laphine_upgrade.yml) |
| 311 | `Pandas_Bonus_bNoFieldGemStone` | 1769 | 使火, 水, 风, 地四大元素领域技能无需消耗魔力矿石 常量名称: SP_PANDAS_NOFIELDGEMSTONE / 调整器名称: bNoFieldGemStone 变量位置: map_session_data.special_state / 变量名称: nofieldgemstone 使用原型: bonus bNoFieldGemStone; |
| 312 | `Pandas_Bonus3_bRebirthWithHeal` | 1776 | 当玩家死亡时有 r/100% 的机率复活并恢复 h% 的 HP 和 s% 的 SP 常量名称: SP_PANDAS_REBIRTHWITHHEAL / 调整器名称: bRebirthWithHeal 变量位置: map_session_data.bonus / 变量名称: rebirth_rate, rebirth_heal_percent_hp, rebirth_heal_percent_sp 使用原型: bonus3 bRebirthWithHeal,r,h,s; |
| 313 | `Pandas_Bonus2_bAddSkillRange` | 1783 | 增加 sk 技能 n 格攻击距离 常量名称: SP_PANDAS_ADDSKILLRANGE / 调整器名称: bAddSkillRange 变量位置: map_session_data / 变量名称: addskillrange 使用原型: bonus2 bAddSkillRange,sk,n; |
| 314 | `Pandas_Bonus2_bSkillNoRequire` | 1790 | 解除 sk 技能中由 n 指定的前置施法条件限制 常量名称: SP_PANDAS_SKILLNOREQUIRE / 调整器名称: bSkillNoRequire 变量位置: map_session_data / 变量名称: skillnorequire 使用原型: bonus2 bSkillNoRequire,sk,n; |
| 315 | `Pandas_Bonus4_bStatusAddDamage` | 1797 | 攻击拥有 sc 状态的目标时, 使用 bf 攻击有 r/100% 的概率使伤害增加 n 常量名称: SP_PANDAS_STATUSADDDAMAGE / 调整器名称: bStatusAddDamage 变量位置: map_session_data / 变量名称: status_damage_adjust 使用原型: bonus4 bStatusAddDamage,sc,n,r,bf; |
| 316 | `Pandas_Bonus4_bStatusAddDamageRate` | 1804 | 攻击拥有 sc 状态的目标时, 使用 bf 攻击有 r/100% 的概率使伤害增加 n% 常量名称: SP_PANDAS_STATUSADDDAMAGERATE / 调整器名称: bStatusAddDamageRate 变量位置: map_session_data / 变量名称: status_damagerate_adjust 使用原型: bonus4 bStatusAddDamageRate,sc,n,r,bf; |
| 317 | `Pandas_Bonus3_bFinalAddRace` | 1811 | 使用 bf 攻击 r 种族的目标时增加 x% 的伤害 (在最终伤害上全段修正) 常量名称: SP_PANDAS_FINALADDRACE / 调整器名称: bFinalAddRace 变量位置: map_session_data / 变量名称: finaladd_race 使用原型: bonus3 bFinalAddRace,r,x,bf; |
| 318 | `Pandas_Bonus3_bFinalAddClass` | 1818 | 使用 bf 攻击时 c 类型目标时增加 x% 的伤害 (在最终伤害上全段修正) 常量名称: SP_PANDAS_FINALADDCLASS / 调整器名称: bFinalAddClass 变量位置: map_session_data / 变量名称: finaladd_class 使用原型: bonus3 bFinalAddClass,c,x,bf; |
| 319 | `Pandas_Bonus2_bAbsorbDmgMaxHP` | 1825 | 受到超过自己总血量 n% 的伤害时只会受到总血量 x% 的伤害 常量名称: SP_ABSORB_DMG_MAXHP / 调整器名称: bAbsorbDmgMaxHP 变量位置: map_session_data.bonus / 变量名称: absorb_dmg_trigger_hpratio, absorb_dmg_cap_ratio 使用原型: bonus2 bAbsorbDmgMaxHP,n,x; |
| 320 | `Pandas_ScriptCommand_Announce` | 1840 | 携带此标记位的公告能够在双击公告时将发布者角色名称填写到聊天窗口 备注: 自己发送的公告自己双击则无效 提示: 使用 20130807 客户端测试通过, 更早之前的客户端没有测试过 |
| 321 | `Pandas_ScriptCommand_UnitExists` | 1844 | 是否拓展 unitexists 脚本指令 [Sola丶小克] 添加一个可选参数, 用于强调单位必须存在且活着才返回 true |
| 322 | `Pandas_ScriptCommand_SetHeadDir` | 1848 | 是否启用 setheaddir 脚本指令 [Sola丶小克] 用于调整角色纸娃娃脑袋的朝向 (0 - 正前方; 1 - 向右看; 2 - 向左看) |
| 323 | `Pandas_ScriptCommand_SetBodyDir` | 1852 | 是否启用 setbodydir 脚本指令 [Sola丶小克] 用于调整角色纸娃娃身体的朝向 (与 NPC 一致, 从 0 到 7 共 8 个方位可选择) |
| 324 | `Pandas_ScriptCommand_OpenBank` | 1858 | 是否启用 openbank 脚本指令 [Sola丶小克] 2022-4-20 修订备注: 由于 rAthena 官方已经实现了 openbank 指令且重名, 因此这里的开关只控制 openbank 指令是否如以前版本一样给予返回值 |
| 325 | `Pandas_ScriptCommand_InstanceUsers` | 1862 | 是否启用 instance_users 脚本指令 [Sola丶小克] 获取指定的副本实例中已经进入副本地图的人数 |
| 326 | `Pandas_ScriptCommand_CapValue` | 1866 | 是否启用 cap 脚本指令 [Sola丶小克] 由于 rAthena 已经实现 cap_value 指令, 这里兼容老版本 cap 指令 |
| 327 | `Pandas_ScriptCommand_MobRemove` | 1870 | 是否启用 mobremove 脚本指令 [Sola丶小克] 根据 GID 移除一个魔物单位 (只是移除, 不会让魔物死亡) |
| 328 | `Pandas_ScriptCommand_MesClear` | 1874 | 是否启用 mesclear 脚本指令 [Sola丶小克] 由于 rAthena 已经实现 clear 指令, 这里兼容老版本 mesclear 指令 |
| 329 | `Pandas_ScriptCommand_BattleIgnore` | 1878 | 是否启用 battleignore 脚本指令 [Sola丶小克] 将角色设置为魔物免战状态, 避免被魔物攻击 (与 GM 指令的 monsterignore 效果一致) |
| 330 | `Pandas_ScriptCommand_GetHotkey` | 1882 | 是否启用 gethotkey 脚本指令 [Sola丶小克] 获取指定快捷键位置当前的信息 (该指令有一个用于兼容的别名: get_hotkey) |
| 331 | `Pandas_ScriptCommand_SetHotkey` | 1886 | 是否启用 sethotkey 脚本指令 [Sola丶小克] 设置指定快捷键位置的信息 (该指令有一个用于兼容的别名: set_hotkey) |
| 332 | `Pandas_ScriptCommand_ShowVend` | 1890 | 是否启用 showvend 脚本指令 [Jian916] 使指定的 NPC 头上可以显示露天商店的招牌, 点击招牌可触发与 NPC 的对话 |
| 333 | `Pandas_ScriptCommand_ViewEquip` | 1894 | 是否启用 viewequip 脚本指令 [Sola丶小克] 使用该指令可以查看指定在线角色的装备面板信息 (注意: v2.0.0 以前是通过账号编号) |
| 334 | `Pandas_ScriptCommand_CountItemIdx` | 1898 | 是否启用 countitemidx 脚本指令 [Sola丶小克] 获取指定背包序号的道具在背包中的数量 (该指令有一个用于兼容的别名: countinventory) |
| 335 | `Pandas_ScriptCommand_DelItemIdx` | 1903 | 是否启用 delitemidx 脚本指令的别名 delinventory [Sola丶小克] https://github.com/rathena/rathena/commit/c18707bb6dd2bd6068bc0d3708401871a2d7270c 由于 rAthena 官方实现了 delitemidx, 因此使用它来接替原先熊猫模拟器的自定义实现 |
| 336 | `Pandas_ScriptCommand_IdentifyIdx` | 1907 | 是否启用 identifyidx 脚本指令 [Sola丶小克] 鉴定指定背包序号的道具 (该指令有一个用于兼容的别名: identifybyidx) |
| 337 | `Pandas_ScriptCommand_UnEquipIdx` | 1911 | 是否启用 unequipidx 脚本指令 [Sola丶小克] 脱下指定背包序号的道具 (该指令有一个用于兼容的别名: unequipinventory) |
| 338 | `Pandas_ScriptCommand_EquipIdx` | 1915 | 是否启用 equipidx 脚本指令 [Sola丶小克] 穿戴指定背包序号的道具 (该指令有一个用于兼容的别名: equipinventory) |
| 339 | `Pandas_ScriptCommand_ItemExists` | 1919 | 是否启用 itemexists 脚本指令 [Sola丶小克] 确认物品数据库中是否存在指定物品 (该指令有一个用于兼容的别名: existitem) |
| 340 | `Pandas_ScriptCommand_RentTime` | 1923 | 是否启用 renttime 脚本指令 [Sola丶小克] 增加/减少指定位置装备的租赁时间 (该指令有一个用于兼容的别名: resume) |
| 341 | `Pandas_ScriptCommand_GetEquipIdx` | 1927 | 是否启用 getequipidx 脚本指令 [Sola丶小克] 获取指定位置装备的背包序号 |
| 342 | `Pandas_ScriptCommand_StatusCalc` | 1931 | 是否启用 statuscalc 脚本指令 [Sola丶小克] 由于 rAthena 已经实现 recalculatestat 指令, 这里兼容老版本 statuscalc 指令 |
| 343 | `Pandas_ScriptCommand_GetEquipExpireTick` | 1935 | 是否启用 getequipexpiretick 脚本指令 [Sola丶小克] 获取指定位置装备的租赁到期剩余秒数 (该指令有一个用于兼容的别名: isrental) |
| 344 | `Pandas_ScriptCommand_GetInventoryInfo` | 1944 | getinventoryinfo <道具的背包序号>,<要查看的信息类型>{,<角色编号>}; getcartinfo <道具的手推车序号>,<要查看的信息类型>{,<角色编号>}; getguildstorageinfo <道具的公会仓库序号>,<要查看的信息类型>{,<角色编号>}; getstorageinfo <道具的个人仓库/扩充仓库序号>,<要查看的信息类型>{{,<仓库编号>},<角色编号>}; |
| 345 | `Pandas_ScriptCommand_StatusCheck` | 1948 | 是否启用 statuscheck 脚本指令 [Sola丶小克] 判断状态是否存在, 并取得相关的状态参数 (该指令有一个用于兼容的别名: sc_check) |
| 346 | `Pandas_ScriptCommand_RentTimeIdx` | 1952 | 是否启用 renttimeidx 脚本指令 [Sola丶小克] 增加/减少指定背包序号道具的租赁时间 |
| 347 | `Pandas_ScriptCommand_PartyLeave` | 1956 | 是否启用 party_leave 脚本指令 [Sola丶小克] 使当前角色或指定角色退出队伍 (主要出于兼容目的而实现该指令) |
| 348 | `Pandas_ScriptCommand_Script4Each` | 1960 | 是否启用 script4each / script4eachmob / script4eachnpc 脚本指令 [Sola丶小克] 对指定范围的玩家 / 魔物 / NPC 执行相同的一段脚本 |
| 349 | `Pandas_ScriptCommand_SearchArray` | 1964 | 是否启用 searcharray 脚本指令 [Sola丶小克] 由于 rAthena 已经实现 inarray 指令, 这里兼容老版本 searcharray 指令 |
| 350 | `Pandas_ScriptCommand_GetSameIpInfo` | 1968 | 是否启用 getsameipinfo 脚本指令 [Sola丶小克] 获得某个指定 IP 在线的玩家信息 |
| 351 | `Pandas_ScriptCommand_Logout` | 1972 | 是否启用 logout 脚本指令 [Sola丶小克] 使指定的角色立刻登出游戏 |
| 352 | `Pandas_ScriptCommand_WarpPartyRevive` | 1976 | 是否启用 warppartyrevive 脚本指令 [Sola丶小克] 与 warpparty 类似, 但可以复活死亡的队友并传送 (该指令有一个用于兼容的别名: warpparty2) |
| 353 | `Pandas_ScriptCommand_GetAreaGid` | 1980 | 是否启用 getareagid 脚本指令 [Sola丶小克] 获取指定范围内特定类型单位的全部 GID (注意: 该指令不再兼容以前 rAthenaCN 的同名指令) |
| 354 | `Pandas_ScriptCommand_ProcessHalt` | 1986 | （需回查原始碼區塊） |
| 355 | `Pandas_ScriptCommand_SetEventTrigger` | 1993 | （需回查原始碼區塊） |
| 356 | `Pandas_ScriptCommand_MessageColor` | 1998 | 是否启用 messagecolor 脚本指令 [Sola丶小克] 使用该指令可以发送指定颜色的消息文本到聊天窗口中 |
| 357 | `Pandas_ScriptCommand_Copynpc` | 2002 | 是否启用 copynpc 脚本指令 [Sola丶小克] 使用该指令可以复制指定的 NPC 到一个新的位置 (坐标等相对可以灵活设置) |
| 358 | `Pandas_ScriptCommand_GetTimeFmt` | 2006 | 是否启用 gettimefmt 脚本指令 [Sola丶小克] 将当前时间格式化输出成字符串, 是 gettimestr 的改进版 |
| 359 | `Pandas_ScriptCommand_MultiCatchPet` | 2012 | （需回查原始碼區塊） |
| 360 | `Pandas_ScriptCommand_SelfDeletion` | 2017 | 是否启用 selfdeletion 脚本指令 [Sola丶小克] 设置 NPC 的自毁策略, 用于配合 copynpc 实现在开宝箱/挖矿时进行自毁等场景 |
| 361 | `Pandas_ScriptCommand_SetCharTitle` | 2022 | 是否启用 setchartitle 脚本指令 [Sola丶小克] 设置指定玩家的称号ID, 客户端封包版本大于等于 20150513 才可用 |
| 362 | `Pandas_ScriptCommand_GetCharTitle` | 2026 | 是否启用 getchartitle 脚本指令 [Sola丶小克] 获得指定玩家的称号ID, 客户端封包版本大于等于 20150513 才可用 |
| 363 | `Pandas_ScriptCommand_NpcExists` | 2031 | 是否启用 npcexists 脚本指令 [Sola丶小克] 该指令用于判断指定名称的 NPC 是否存在, 就算不存在控制台也不会报错 |
| 364 | `Pandas_ScriptCommand_StorageGetItem` | 2036 | 是否启用 storagegetitem 脚本指令 [Sola丶小克] 往仓库直接创造一个指定的道具, 必须在仓库关闭的时候才能调用 |
| 365 | `Pandas_ScriptCommand_SetInventoryInfo` | 2041 | 是否启用 setinventoryinfo 脚本指令 [Sola丶小克] 该指令用于设置指定背包序号道具的部分详细信息, 与 getinventoryinfo 对应 |
| 366 | `Pandas_ScriptCommand_UpdateInventory` | 2045 | 是否启用 updateinventory 脚本指令 [Sola丶小克] 该指令用于重新下发关联玩家的背包数据给客户端 (刷新客户端背包数据) |
| 367 | `Pandas_ScriptCommand_GetCharMacAddress` | 2051 | （需回查原始碼區塊） |
| 368 | `Pandas_ScriptCommand_GetConstant` | 2056 | 是否启用 getconstant 脚本指令 [Sola丶小克] 该指令用于查询一个常量字符串对应的数值 |
| 369 | `Pandas_ScriptCommand_Preg_Search` | 2060 | 是否启用 preg_search 脚本指令 [Sola丶小克] 该指令用于执行一个正则表达式搜索并返回首个匹配的分组内容 |
| 370 | `Pandas_ScriptCommand_Aura` | 2066 | （需回查原始碼區塊） |
| 371 | `Pandas_ScriptCommand_UnitAura` | 2074 | （需回查原始碼區塊） |
| 372 | `Pandas_ScriptCommand_GetUnitTarget` | 2079 | 是否启用 getunittarget 脚本指令 [Sola丶小克] 该指令用于获取指定单位当前正在攻击的目标单位编号 |
| 373 | `Pandas_ScriptCommand_UnlockCmd` | 2083 | 是否启用 unlockcmd 脚本指令 [Sola丶小克] 该指令用于解锁实时事件和过滤器事件的指令限制, 只能用于实时或过滤器事件 |
| 374 | `Pandas_ScriptCommand_BattleRecordQuery` | 2090 | 是否启用 batrec_query 脚本指令 [Sola丶小克] 查询指定单位的战斗记录, 查看与交互目标单位产生的具体记录值 |
| 375 | `Pandas_ScriptCommand_BattleRecordRank` | 2094 | 是否启用 batrec_rank 脚本指令 [Sola丶小克] 查询指定单位的战斗记录并对记录的值进行排序, 返回排行榜单 |
| 376 | `Pandas_ScriptCommand_BattleRecordSortout` | 2098 | 是否启用 batrec_sortout 脚本指令 [Sola丶小克] 移除指定单位的战斗记录中交互单位已经不存在 (或下线) 的记录 |
| 377 | `Pandas_ScriptCommand_BattleRecordReset` | 2102 | 是否启用 batrec_reset 脚本指令 [Sola丶小克] 清除指定单位的战斗记录 |
| 378 | `Pandas_ScriptCommand_EnableBattleRecord` | 2106 | 是否启用 enable_batrec 脚本指令 [Sola丶小克] 该指令用于启用指定单位的战斗记录 |
| 379 | `Pandas_ScriptCommand_DisableBattleRecord` | 2110 | 是否启用 disable_batrec 脚本指令 [Sola丶小克] 该指令用于禁用指定单位的战斗记录 |
| 380 | `Pandas_ScriptCommand_Login` | 2117 | （需回查原始碼區塊） |
| 381 | `Pandas_ScriptCommand_CheckSuspend` | 2124 | （需回查原始碼區塊） |
| 382 | `Pandas_ScriptCommand_BonusScriptRemove` | 2129 | 是否启用 bonus_script_remove 脚本指令 [Sola丶小克] 该指令用于移除指定的 bonus_script 效果脚本 |
| 383 | `Pandas_ScriptCommand_BonusScriptList` | 2133 | 是否启用 bonus_script_list 脚本指令 [Sola丶小克] 该指令用于获取指定角色当前激活的全部 bonus_script 效果脚本编号 |
| 384 | `Pandas_ScriptCommand_BonusScriptExists` | 2137 | 是否启用 bonus_script_exists 脚本指令 [Sola丶小克] 该指令用于查询指定角色是否已经激活了特定的 bonus_script 效果脚本 |
| 385 | `Pandas_ScriptCommand_BonusScriptGetId` | 2141 | 是否启用 bonus_script_getid 脚本指令 [Sola丶小克] 该指令用于查询效果脚本代码对应的效果脚本编号 |
| 386 | `Pandas_ScriptCommand_BonusScriptInfo` | 2145 | 是否启用 bonus_script_info 脚本指令 [Sola丶小克] 该指令用于查询指定效果脚本的相关信息 |
| 387 | `Pandas_ScriptCommand_ExpandInventoryAdjust` | 2149 | 是否启用 expandinventory_adjust 脚本指令 [Sola丶小克] 该指令用于增加角色的背包容量上限 |
| 388 | `Pandas_ScriptCommand_GetInventorySize` | 2153 | 是否启用 getinventorysize 脚本指令 [Sola丶小克] 该指令用于查询并获取当前角色的背包容量上限 |
| 389 | `Pandas_ScriptCommand_GetMapSpawns` | 2159 | （需回查原始碼區塊） |
| 390 | `Pandas_ScriptCommand_GetMobSpawns` | 2166 | （需回查原始碼區塊） |
| 391 | `Pandas_ScriptCommand_GetCalendarTime` | 2171 | 是否启用 getcalendartime 脚本指令 [Haru] 该指令用于获取下次出现指定时间的 UNIX 时间戳 |
| 392 | `Pandas_ScriptCommand_GetSkillInfo` | 2175 | 是否启用 getskillinfo 脚本指令 [聽風] 该指令用于获取指定技能在技能数据库中所配置的各项信息 |
| 393 | `Pandas_ScriptCommand_BossMonster` | 2181 | （需回查原始碼區塊） |
| 394 | `Pandas_ScriptCommand_Sleep3` | 2186 | 是否启用 sleep3 脚本指令 [人鱼姬的思念] 该指令用于休眠一段时间再执行后续脚本, 与 sleep2 类似但忽略报错 |
| 395 | `Pandas_ScriptCommand_GetQuestTime` | 2190 | 是否启用 getquesttime 脚本指令 [Sola丶小克] 该指令用于查询角色指定任务的时间信息 (感谢 "SSBoyz" 建议) |
| 396 | `Pandas_ScriptCommand_UnitSpecialEffect` | 2194 | 是否启用 unitspecialeffect 脚本指令 [人鱼姬的思念] 该指令用于使指定游戏单位可以显示某个特效, 并支持控制特效可见范围 |
| 397 | `Pandas_ScriptCommand_Next_Dropitem_Special` | 2198 | 是否启用 next_dropitem_special 脚本指令 [Sola丶小克] 该指令用于对下一个掉落到地面上的物品进行特殊设置, 支持魔物掉落道具和 makeitem 系列指令 |
| 398 | `Pandas_ScriptCommand_GetGradeItem` | 2203 | 是否启用 getgradeitem 脚本指令 [Sola丶小克] 该指令用于创造带有指定附魔评级的道具, 由于 rAthena 已经正式实现了 getitem4, getgradeitem 仅用于兼容旧版本的脚本, 请尽量使用 getitem4 |
| 399 | `Pandas_ScriptCommand_GetRateIdx` | 2207 | 是否启用 getrateidx 脚本指令 [Sola丶小克] 随机获取一个数值型数组的索引序号, 数组中每个元素的值为权重值 |
| 400 | `Pandas_ScriptCommand_GetBossInfo` | 2211 | 是否启用 getbossinfo 脚本指令 [Sola丶小克] 该指令用于查询 BOSS 魔物重生时间及其坟墓等信息 |
| 401 | `Pandas_ScriptCommand_WhoDropItem` | 2215 | 是否启用 whodropitem 脚本指令 [Sola丶小克] 该指令用于查询指定道具会从哪些魔物身上掉落以及掉落的机率信息 |
| 402 | `Pandas_ScriptCommand_GetInventoryList` | 2233 | - 可控制每次想查询的数据类型 - 用于解决仓库和背包容量超大时候填充大量不使用的数据带来的性能问题 更多详细用法请移步 doc/pandas_script_commands.txt 文件 |
| 403 | `Pandas_ScriptCommand_QuerySql_Async` | 2245 | （需回查原始碼區塊） |
| 404 | `Pandas_ScriptConstants_CartWeight` | 2256 | 是否扩展 CartWeight 脚本常量 [人鱼姬的思念] |
| 405 | `Pandas_ScriptConstants_MaxCartWeight` | 2259 | 是否扩展 MaxCartWeight 脚本常量 [人鱼姬的思念] |
| 406 | `Pandas_ScriptResults_OnSellItem` | 2268 | 使 OnSellItem 标签可以返回被出售道具的背包序号 [Sola丶小克] |
| 407 | `Pandas_ScriptParams_ReadParam` | 2277 | 是否拓展 readparam 脚本指令的可用参数 [Sola丶小克] |
| 408 | `Pandas_ScriptParams_GetItemInfo` | 2280 | 是否拓展 getiteminfo 脚本指令的可用参数 [Sola丶小克] |
| 409 | `Pandas_ScriptParams_DamageTaken_From_Database` | 2284 | 是否拓展 getunitdata 指令的参数 使之能读取指定魔物在 DB 中设置的承伤倍率 (UMOB_DAMAGETAKEN_DB) [Sola丶小克] |
| 410 | `Pandas_ScriptParams_DamageTaken_Extend` | 2289 | 是否扩展 setunitdata / getunitdata 指令的参数 使 UMOB_DAMAGETAKEN 能支持 -1 的值, 表示采用 DB 中设置的承伤倍率 [Sola丶小克] 该选项主要为了兼容旧版本熊猫模拟器的用户可能已经使用了 -1 值的情况 |
| 411 | `Pandas_ScriptParams_UnitData_Experience` | 2295 | （需回查原始碼區塊） |
| 412 | `Pandas_WebServer_Database_EncodingAdaptive` | 2309 | 客户端发送给 WEB 接口的内容使用的是 UTF8 编码, 我们需要将内容存放到数据库中去 但数据库本身的编码可能不是 UTF8, 因此在入库之前需要将内容进行适当的编码转换, 否则数据库中看到的会是乱码 同理, 将数据库中保存的内容读取出来后也需要转换成 UTF8 编码才能发送给客户端 |
| 413 | `Pandas_WebServer_Console_EncodingAdaptive` | 2317 | 客户端发送给 WEB 接口的内容使用的是 UTF8 编码, 但我们的终端程序通常不是工作在 UTF8 编码环境下, 因此如果将客户端发送来的中文直接打印到终端就会变成乱码. 启用该选项后将会对客户端发送来的 UTF8 信息在输出时转换成当前终端使用的编码再打印到终端 |
| 414 | `Pandas_WebServer_Logger_Improved_Presentation` | 2320 | 是否改进开启 print_req_res 后打印信息的呈现方式, 使信息的区域划分更清晰 [Sola丶小克] |
| 415 | `Pandas_WebServer_Rewrite_Controller_HandlerFunc` | 2325 | （需回查原始碼區塊） |
| 416 | `Pandas_WebServer_ApplyMutex_For_Logger` | 2333 | 如果不进行互斥操作的话, 在打开 print_req_res 的情况下， 如果请求间隔很短会导致终端输出日志信息的时候由于并发而混在一起 比如: 冒险者查询接口就是 party/list 然后立刻 party/get 两个请求间隔非常短 |

## 移植判定規則

1. **原生等價**：brHades 已有同等行為，需附上對應檔案與程式碼位置，不重複移植。
2. **已移植**：功能程式碼、設定／腳本介面與相依項目已納入工作分支，且有測試與建置證據。
3. **部分移植**：只有部分程式碼或介面，不得視為完成。
4. **待移植**：尚無等價實作。
5. **待確認**：上游巨集存在，但需追蹤所有呼叫點或確認功能實際行為。

## 後續工作要求

- 逐一追蹤全部 416 項巨集，不能只挑選容易移植的項目。
- 以功能行為為單位盤點，不以檔案差異數量代替功能差異。
- 對上游本身只有旗標宣告、缺少實際使用點或疑似不完整的功能，標記待確認並記錄證據，不自行猜測補寫。
- 每一批移植後都執行相應回歸測試及 Debug／Release、x64／Win32 雲端建置。
- 另行盤點不由此設定檔控制的 Pandas 功能、NPC、資料庫、腳本、Web Server、封包、工具與文件；本清冊不能代替全 repo 稽核。
