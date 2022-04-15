#!/bin/bash

source .venv/bin/activate

if [ -f "bot_token.txt" ]; then
  bot_token=`cat bot_token.txt`
fi
if [ -f "api_key.txt" ]; then
  api_key=`cat api_key.txt`
fi
if [ -f "guild_id.txt" ]; then
  guild_id=`cat guild_id.txt`
fi
if [ -f "starting_summoner.txt" ]; then
  starting_summoner=`cat starting_summoner.txt`
fi
