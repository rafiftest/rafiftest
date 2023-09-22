import discord
from discord.ext import commands, tasks
import aiohttp
import asyncio

# Define bot intents
intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True

# Create a bot instance with specified intents
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}!')

    # Start the background task to update the activity
    update_activity.start()

# Function to fetch the total number of online players in Growtopia
async def get_total_online_players():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.growtopiagame.com/detail') as response:
            if response.status == 200:
                data = await response.text()
                # Parse the online player count from the response
                total_online = int(data[data.find('"online_user":"')+15:data.find('"online_user":"')+20])
                return total_online
            else:
                return None

# Background task to periodically update the bot's activity
@tasks.loop(minutes=1)
async def update_activity():
    total_online = await get_total_online_players()
    if total_online is not None:
        activity = discord.Activity(type=discord.ActivityType.watching,name=f"{total_online} Online Users")
        await bot.change_presence(status=discord.Status.online, activity=activity)
    await asyncio.sleep(60)
# Define a command to provide a list of available commands  
@bot.command()
async def command(ctx):
    await ctx.send(f'Available Commands: !growtopiaplayer, !ping')

# Define a command to fetch and display the total online players in Growtopia
@bot.command()
async def growtopiaplayer(ctx):
    total_online = await get_total_online_players()
    if total_online is not None:
        await ctx.send(f'Total Players: {total_online}')
    else:
        await ctx.send('Failed to fetch online player data.')

# Define a command to check the bot's latency
@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'Latency is {latency}ms. API Latency is {latency}ms')

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot.run('MTA2NTk2NDQ2NjgxNjE2Nzk1Ng.GcmtgX.ijFj5HV4UcSCX3A_IPxwEaLkPSFQ-qyM7Q_a1o')
