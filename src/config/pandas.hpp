// Pandas 特色功能移植設定
// 本檔僅啟用目前已移植的 Pandas 功能及其必要相依項目。

#ifndef CONFIG_PANDAS_HPP
#define CONFIG_PANDAS_HPP

#define PANDAS_NPCE_MAX 10
#define PANDAS_NPCE_NONE 0xFF

#define Pandas_BattleConfig_Identify_Event_Mode

#define Pandas_Struct_Map_Session_Data_Pandas
#define Pandas_Struct_Map_Session_Data_WorkInEvent
#define Pandas_Struct_Map_Session_Data_EventHalt

#define Pandas_NpcFilter_IDENTIFY
#define Pandas_ScriptCommand_ProcessHalt
#define Pandas_Mapflags
#define Pandas_MobInfomation_Extend
#define Pandas_MapFlag_MobInfo
#define Pandas_MapFlag_NoAutoLoot
#define Pandas_MapFlag_NoToken
#define Pandas_MapFlag_NoMail
#define Pandas_MapFlag_NoPet
#define Pandas_MapFlag_NoMerc
#define Pandas_MapFlag_MobDroprate
#define Pandas_MapFlag_MvpDroprate
#define Pandas_MapFlag_MaxHeal
#define Pandas_MapFlag_MaxDmg_Skill
#define Pandas_MapFlag_MaxDmg_Normal
#define Pandas_MapFlag_NoBank
#define Pandas_MapFlag_NoCapture
#define Pandas_MapFlag_NoSlave
#define Pandas_MapFlag_NoAttack
#define Pandas_MapFlag_NoUseItem
#define Pandas_MapFlag_HideGuildInfo
#define Pandas_MapFlag_HidePartyInfo
#define Pandas_MapFlag_HideDamage

#endif // CONFIG_PANDAS_HPP
