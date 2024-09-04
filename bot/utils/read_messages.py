import re
from datetime import datetime, timedelta
from pytz import timezone, utc
from typing import Optional, List, Dict
from discord import message, Client, TextChannel
from utils.command_parser import WhatLogicResult

def convert_time_string_to_datetime(from_time: str) -> datetime:
    """
    Expects a string like "today", "{number} hours", "{number} days", or "{number} weeks"
    and returns a datetime object representing the corresponding time in PST.
    """
    pst = timezone('America/Los_Angeles')
    now = datetime.now(pst)
    if from_time.lower() == 'today':
        return now.replace(hour=0, minute=0, second=0, microsecond=0)
    # Handle "{number} hours"
    hours_match = re.match(r'(\d+)\s*hour(s)?', from_time, re.IGNORECASE)
    if hours_match:
        hours = int(hours_match.group(1))
        return now - timedelta(hours=hours)
    # Handle "{number} days"
    days_match = re.match(r'(\d+)\s*day(s)?', from_time, re.IGNORECASE)
    if days_match:
        days = int(days_match.group(1))
        return now - timedelta(days=days)
    # Handle "{number} weeks"
    weeks_match = re.match(r'(\d+)\s*week(s)?', from_time, re.IGNORECASE)
    if weeks_match:
        weeks = int(weeks_match.group(1))
        return now - timedelta(weeks=weeks)
    raise ValueError(f"Invalid time period: {from_time}")


async def read_messages(message: message, what_logic_dict: WhatLogicResult) -> Dict[str, List[str]]:
    """
    Reads messages from a specified channel and filters based on time and users.
    Returns a dictionary where keys are channel names and values are lists of messages.
    """
    since_time = what_logic_dict['since_time']
    if isinstance(since_time, datetime):
        from_time_dt = since_time if since_time.tzinfo else since_time.replace(tzinfo=timezone.utc)
    else:
        from_time_dt = convert_time_string_to_datetime(since_time)  # Ensure this function converts a string to datetime
    channels = message.guild.channels
    messages_dict = {}
    for channel in channels:
        if isinstance(channel, TextChannel):
            if what_logic_dict.get('channel_name') and channel.name != what_logic_dict['channel_name']:
                continue
            messages = []
            async for msg in channel.history(limit=10000, after=from_time_dt):  # Adjust the limit as necessary
                if msg.author.display_name not in what_logic_dict['users']:
                    continue
                if msg.content.startswith("!") or msg.content.startswith("/"):
                    continue
                messages.append(f"{msg.author.display_name}: {msg.content}")
            if messages:
                messages_dict[channel.name] = messages
    return messages_dict
