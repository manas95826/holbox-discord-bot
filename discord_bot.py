import discord
from discord.ext import commands
from event_agent import Agent
import os
from dotenv import load_dotenv
from supabase import create_client
from datetime import datetime

load_dotenv()

# Initialize Supabase client
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# Initialize Discord bot with intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize the event agent
agent = Agent()

# Register functions from event_agent.py
from event_agent import onboard_new_member, get_community_help, generate_content, general_chat, get_community_guidelines, get_upcoming_events, report_issue, get_community_stats, get_resource_links, get_chat_summary

functions = [
    onboard_new_member,
    get_community_help,
    generate_content,
    general_chat, 
    get_community_guidelines,
    get_upcoming_events,
    report_issue,
    get_community_stats,
    get_resource_links,
    get_chat_summary
]

for func in functions:
    agent.register_function(func)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    print("on_message triggered")
    print(f"Received message: {message.content} from {message.author}")
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Check if the message is in the welcome channel or mod channel
    if message.channel.id in [int(os.getenv('WELCOME_CHANNEL_ID')), int(os.getenv('MOD_CHANNEL_ID'))]:
        try:
            # Process the query using the agent
            result = agent.process_query(message.content)
            response = result['result']
            
            # Store the conversation in the discussions table
            result = supabase.table('discussions').insert({
                'title': f"Chat with {message.author.name}",
                'content': f"User Query: {message.content}\nBot Response: {response}",
                'last_activity': datetime.now().isoformat()
            }).execute()
            print(result)
            
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
    await bot.process_commands(message)

def main():
    # Run the bot with the token from environment variables
    bot.run(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    main()
