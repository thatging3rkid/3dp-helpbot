#!/bin/bash
{
python3 /home/user/3dp-helpbot/bot.py
} 2>&1> /home/user/3dp-helpbot/logs/log-`date +%m-%d-%Y_%H:%M:%S`.txt &
