#!/bin/bash

source .venv/bin/activate

if [ -f "bot_token.txt" ]; then
	bot_token=`cat bot_token.txt`
fi
if [ -f "api_key.txt" ]; then
	api_key=`cat api_key.txt`
fi
if [ -f "guild_id_list.txt" ]; then
	guild_id_list=`cat guild_id_list.txt`
fi
if [ -f "setup_summoner.txt" ]; then
	setup_summoner=`cat setup_summoner.txt`
fi
if [ -f "bot_owner_id_list.txt" ]; then
	bot_owner_id_list=`cat bot_owner_id_list.txt`
fi
if [ -f "version.txt" ]; then
	version=`cat version.txt`
fi
