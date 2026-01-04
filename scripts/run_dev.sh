#!/bin/bash

echo "Starting Aura LLM API..."
uvicorn app.main:app --reload &
sleep 2
echo "Starting Discord Bot..."
python bots/discord/bot.py
