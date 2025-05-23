import discord
from discord.ext import commands
from datetime import datetime
from src.agent.agent import CommunityAgent
from src.database.supabase_client import supabase
from config.config import (
    DISCORD_TOKEN,
    WELCOME_CHANNEL_ID,
    MOD_CHANNEL_ID,
    COMMAND_PREFIX
)

class CommunityBot:
    def __init__(self):
        # Initialize Discord bot with intents
        intents = discord.Intents.default()
        intents.message_content = True
        self.bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)
        self.agent = CommunityAgent()
        self._setup_events()

    def _setup_events(self):
        @self.bot.event
        async def on_ready():
            print(f'{self.bot.user} has connected to Discord!')

        @self.bot.event
        async def on_message(message):
            print("on_message triggered")
            print(f"Received message: {message.content} from {message.author}")
            
            # Ignore messages from the bot itself
            if message.author == self.bot.user:
                return

            # Check if the message is in the welcome channel or mod channel
            if message.channel.id in [WELCOME_CHANNEL_ID, MOD_CHANNEL_ID]:
                try:
                    # Process the query using the agent
                    result = self.agent.process_query(message.content)
                    response = result['result']
                    
                    # Store the conversation in the discussions table
                    supabase.table('discussions').insert({
                        'title': f"Chat with {message.author.name}",
                        'content': f"User Query: {message.content}\nBot Response: {response}",
                        'last_activity': datetime.now().isoformat()
                    }).execute()
                    
                    # Send the response back to the channel
                    await message.channel.send(f"{response}")
                except Exception as e:
                    print(f"Exception occurred: {e}")
                    error_message = f"Error processing your request: {str(e)}"
                    # Store the error in the discussions table
                    supabase.table('discussions').insert({
                        'title': f"Error in chat with {message.author.name}",
                        'content': f"User Query: {message.content}\nError: {error_message}",
                        'last_activity': datetime.now().isoformat()
                    }).execute()
                    await message.channel.send(error_message)

            # Process commands
            await self.bot.process_commands(message)

    def run(self):
        self.bot.run(DISCORD_TOKEN) 