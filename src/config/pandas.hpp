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
#define Pandas_MapFlag_NoAutoLoot
#define Pandas_MapFlag_NoToken
#define Pandas_MapFlag_NoMail
#define Pandas_MapFlag_NoCapture
#define Pandas_MapFlag_NoSlave
#define Pandas_MapFlag_NoAttack
#define Pandas_MapFlag_NoUseItem

#endif // CONFIG_PANDAS_HPP
