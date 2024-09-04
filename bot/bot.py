from discord import Client, message, Intents
import os
from dotenv import load_dotenv
base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(base_dir, '.env'))
token = os.getenv('DISCORD_TOKEN')
import logging
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
from utils.command_parser import handle_what_logic, handle_what_logic_no_time
from utils.read_messages import read_messages
from utils.google_gemini import send_to_gemini_api
from utils.embed import embed_summary, handle_help



class MyClient(Client):

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message: message):
        if message.author.id == self.user.id:
            return
        # example `message.reference`: <MessageReference message_id=1280648913753210941 
        # channel_id=1273735194624393307 guild_id=1160305385236873358>

        # example `message.created_at`: 2024-09-03 23:09:11.558000+00:00

        if message.content.startswith('!help'):
            embed = handle_help()
            await message.channel.send(embed=embed, mention_author=True)
            return 
        
        has_reference = bool(message.reference)
        try:
            if message.content.startswith('!what'):
                what_dict = None
                if 'channel' in message.content:
                    what_dict = handle_what_logic(message, is_channel=True)
                elif has_reference:
                    what_dict = handle_what_logic_no_time(message)
                else:
                    what_dict = handle_what_logic(message)
                await message.reply(what_dict['message'], mention_author=True)
                messages_dict = await read_messages(message, what_dict)
                gemini_response = await send_to_gemini_api(messages_dict)
                embed = embed_summary(message, gemini_response)
                await message.channel.send(embed=embed)
        except ValueError as e:
            await message.reply(f'An error occurred: {str(e)}', mention_author=True)

intents = Intents.default()
intents.message_content = True
intents.members = True

client = MyClient(intents=intents)
client.run(token)
