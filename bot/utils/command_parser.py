from discord import message
import re
from typing import TypedDict, List, Optional
from datetime import datetime

def check_if_users_exist(message: message, users: list[str]) -> bool:
    for user in users:
        if not any(user.lower() == member.display_name.lower() and not member.bot for member in message.guild.members):
            return False
    return True

class WhatLogicResult(TypedDict):
    message: str
    users: List[str]
    channel_name: Optional[str]
    since_time: str | datetime

def handle_what_logic_no_time(message: message):
    # example message.reference: message.reference: <MessageReference message_id=1280648913753210941 
    # channel_id=1273735194624393307 guild_id=1160305385236873358>
    from_pattern = r'\bfrom\b\s+([a-zA-Z0-9\+\-_]+(?:\s+[a-zA-Z0-9\+\-_]+)*)'
    full_pattern = rf'^!what\b.*{from_pattern}'
    match = re.search(full_pattern, message.content, re.IGNORECASE)
    users = [user.display_name for user in message.guild.members if not user.bot]
    message_string = None
    if match:
        names = match.group(1).strip()
        names_strs = names.split()
        if names and not check_if_users_exist(message, names_strs):
            raise ValueError('One or more users do not exist in the server.')
        else:
            users = names_strs
            message_string = f'You asked about {names} in {message.channel}!'
    elif message.content == '!what':
        message_string = f'You asked about everyone in {message.channel}!'
    else:
        raise ValueError('Did not catch that, ask again')
    return WhatLogicResult(
        message=message_string, 
        users=users, 
        channel_name=message.channel.name,
        since_time=message.reference.resolved.created_at
    )


def handle_what_logic(message: message, is_channel=False):
    time_pattern = r'(today|\d+\s*hour(s)?|\d+\s*day(s)?|\d+\s*week(s)?)'
    from_pattern = r'\bfrom\b\s+([a-zA-Z0-9\+\-_]+(?:\s+[a-zA-Z0-9\+\-_]+)*)'
    full_pattern = rf'^!what\b.*{time_pattern}.*{from_pattern}'
    match = re.search(full_pattern, message.content, re.IGNORECASE)
    only_time_match = re.search(rf'^!what\b.*{time_pattern}', message.content, re.IGNORECASE)
    users = [user.display_name for user in message.guild.members if not user.bot]
    if match:
        time_period = since_time = match.group(1)
        names = match.group(5).strip()
        names_str = names.split()
        if names and not check_if_users_exist(message, names_str):
            raise ValueError('One or more users do not exist in the server.')
        users = names_str
        if is_channel:
            message_string = f'You asked about {time_period} from {names} in {message.channel}!'
        else:
            message_string = f'You asked about {time_period} from {names}!'
    elif only_time_match:
        time_period = since_time = only_time_match.group(1)
        if is_channel:
            message_string = f'You asked about {time_period} from everyone in {message.channel}!'
        else:
            message_string = f'You asked about {time_period} from everyone!'
    else:
        raise ValueError('Did not catch that, ask again')
        
    return WhatLogicResult(
        message=message_string,
        users=users,
        channel_name= message.channel.name if is_channel else None,
        since_time=since_time
    )


