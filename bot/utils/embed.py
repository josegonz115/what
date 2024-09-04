from discord import Embed, message
from typing import Dict

# def embed_summary(message: message):
        # {
        #     "general": "The conversation in the 'general' channel started with casual greetings, with users discussing their busy schedules. The conversation then shifted towards a shared interest in a new series, with user4 expressing their enthusiasm for the latest episode and user1 confirming they watched it and enjoyed the plot twists.",
        #     "random": "The 'random' channel focused on a recent sports game, with users discussing the outcome and their reactions. User5 and user6 shared their excitement about the game's intensity and the close final score. User7 expressed regret for missing the game and user5 provided details about the home team's overtime win."
        # }

def embed_summary(message: message, summaries: Dict[str, str]) -> Embed:
    """
    Creates an embed to display the summaries of conversations in different channels.
    
    :param message: The message object (used for contextual information like author, etc.).
    :param summaries: A dictionary where the keys are channel names and the values are summaries of those channels.
    :return: A Discord Embed object that can be sent as a reply or message.
    """
    usernames = [member.display_name for member in message.guild.members if not member.bot]
    embed = Embed(
        title="Conversation Summaries",
        description="Here are the summaries of recent conversations in the specified channels:",
        color=0x7289da  # Discord color code (blurple)
    )
    
    for channel_name, summary in summaries.items():
        for username in usernames:
            summary = summary.replace(username, f"`{username}`")
        if len(summary) > 1000:
            for i in range(0, len(summary), 1000):
                chunk = summary[i:i + 1000]
                embed.add_field(
                    name=f"#{channel_name}" if i == 0 else f"#{channel_name} (cont'd)",
                    value=chunk,
                    inline=False
                )
        else:
            embed.add_field(
                name=f"#{channel_name}",
                value=summary,
                inline=False
            )
    embed.set_footer(text=f"Requested by {message.author.display_name}", icon_url=message.author.avatar)
    return embed

def handle_help():
    """ 
    Creates an embed with information on how to use the `!what` command.
    :return: A Discord Embed object with the help information.
    """
    embed = Embed(
        title='WHAT Help Menu',
        description="Welcome to the What Help Menu! Use `!what` command to generate summaries based on chat history.",
        color=0x7289da
    )
    embed.add_field(
        name="Basic Command: `!what`",
        value=(
            "The `!what` command generates a summary of recent conversations. "
            "You could also filter by time, user, or channel."
        ),
        inline=False
    )
    embed.add_field(
        name="Time Filter",
        value=(
            "You can specify a time range to filter the messages. The options are:\n"
            "- `today`: Messages from today.\n"
            "- `[number] hours`: Messages from the past 'number' of hours (e.g., `3 hours`).\n"
            "- `[number] days`: Messages from the past 'number' of days (e.g., `2 days`).\n"
            "- `[number] weeks`: Messages from the past 'number' of weeks (e.g., `1 week`)."
        ),
        inline=False
    )
    embed.add_field(
        name="User Filter: `from [user1] [user2] ...`",
        value=(
            "You can specify 1 or more users to focus the summary on messages from those specific users. "
            "Use the `from` keyword followed by the usernames, separated by spaces. For example:\n"
            "- `from user1`: Summarizes messages from `user1`.\n"
            "- `from user1 user2`: Summarizes messages from `user1` and `user2`."
        ),
        inline=False
    )
    embed.add_field(
        name="Channel Filter: `!what channel`",
        value=(
            "Use the `channel` keyword to only summarize the current channel. "
            "This will only include messages from the current channel in the summary."
        ),
        inline=False
    )
    embed.add_field(
        name="Combining Filters",
        value=(
            "You can combine time, user, and channel filters. Here are some examples:\n"
            "- `!what 3 days from user1 user2`: Summarizes messages from `user1` and `user2` over the last 3 days.\n"
            "- `!what today channel`: Summarizes all messages from today in the current channel.\n"
            "- `!what 2 weeks from user3 channel`: Summarizes messages from `user3` in the past 2 weeks, only in the current channel."
        ),
        inline=False
    )
    embed.add_field(
        name="Help Command: `!help`",
        value="Displays this help menu.",
        inline=False
    )
    embed.set_footer(text="Use the `!what` command to easily summarize chat activity!")
    return embed