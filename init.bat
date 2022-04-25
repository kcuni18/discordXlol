@echo off

CALL .venv\Scripts\activate.bat

if EXIST "bot_token.txt" (
	set /p bot_token=<bot_token.txt
)
if EXIST "api_key.txt" (
	set /p api_key=<api_key.txt
)
if EXIST "guild_id_list.txt" (
	set /p guild_id_list=<guild_id_list.txt
)
if EXIST "setup_summoner.txt" (
	set /p setup_summoner=<setup_summoner.txt
)
if EXIST "bot_owner_id_list.txt" (
	set /p bot_owner_id_list=<bot_owner_id_list.txt
)
if EXIST "version.txt" (
	set /p version=<version.txt
)
