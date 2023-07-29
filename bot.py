import discord
import typing
from discord import app_commands
from discord.ext import commands
from api import *
pip i
intents = discord.Intents.default()
client = discord.Client(intents=intents)
bot = app_commands.CommandTree(client)

@bot.command(name="stream", description="Stream Music from Radio Garden") #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def stream_music(interaction, url: str):
   channel = fetch_station_id_url(url)
   try:
      station_data = get_channel_station(channel)
      stream_url = get_channel_station_broadcast_head(channel)
      await restartStream(interaction, stream_url)
      message = f":musical_keyboard: Playing **{station_data['name']}** from **{station_data['country']['name']}**"
   except Exception as e:
      print(e)
      message = ":x: No found stream URL. Please use other URL"
   await interaction.response.send_message(message)

@bot.command(name="search", description="Search and play Radio Station from Radio Garden") #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def stream_music(interaction, query: str, region: typing.Optional[str]="XX"):
   query_data = fetch_radio_stations(query)
   if len(region) == 2 and region != "XX":
      regions_data = get_stations_by_region(query_data, region)
      station = get_first_station_region(regions_data)
   elif len(region) > 2 or len(region) < 2:
      message = ":x: Invalid station region. Please use other like: PL, DE, US"
      return await interaction.response.send_message(message)
   else:
      station = get_first_station(query_data)
      print(station)
   channel = get_channel_id(station)
   station_data = get_channel_station(channel)
   try:
      stream_url = get_channel_station_broadcast_head(channel)
      await restartStream(interaction, stream_url)
      message = f":musical_keyboard: Playing **{station_data['name']}** from **{station_data['country']['name']}**"
   except Exception as e:
      print(e)
      message = ":x: No found stream URL. Please use other query"
   await interaction.response.send_message(message)

@bot.command(name="stop", description="Stop playing station")
async def stop_music(interaction):
   if (interaction.guild.voice_client.is_playing()):
      interaction.guild.voice_client.stop()
      await interaction.response.send_message(":stop_button: Stopped playing station")

@bot.command(name="left", description="Left from voice channel")
async def left_channel(interaction):
      if (interaction.guild.voice_client.is_playing()):
         interaction.guild.voice_client.stop()
      voice = discord.utils.get(client.voice_clients, guild=interaction.guild)
      await voice.disconnect()
      await interaction.response.send_message(":stop_button: Left from the voice channel")

@bot.command(name="geturl", description="Get direct Stream URL from Radio Garden station")
async def url(interaction: discord.Interaction, url: str):
   channel = fetch_station_id_url(url)
   try:
      stream_url = get_channel_station_broadcast_head(channel)
   except:
      stream_url = ":x: No found stream URL. Please use other URL"
   await interaction.response.send_message(stream_url)


@bot.command(name="getquery", description="Get direct Stream URL from Radio Garden station")
async def url(interaction: discord.Interaction, query: str):
   query_data = fetch_radio_stations(query)
   station = get_first_station(query_data)
   channel = get_channel_id(station)
   try:
      stream_url = get_channel_station_broadcast_head(channel)
   except:
      stream_url = ":x: No found stream URL. Please use other query"
   await interaction.response.send_message(stream_url)

async def restartStream(ctx, url: str):
   guild = ctx.guild
   user = ctx.user
   if guild.voice_client is None:
      if user.voice:
         await user.voice.channel.connect()
         guild.voice_client.play(discord.FFmpegPCMAudio(url))
      else:
         await ctx.response.send_message(":x: You are not connected to a voice channel.")
         raise commands.CommandError("Author not connected to a voice channel.")
   elif guild.voice_client.is_playing():
      guild.voice_client.stop()
      guild.voice_client.play(discord.FFmpegPCMAudio(url))

@client.event
async def on_ready():
   await bot.sync()
   print("🌍 Ready to play world stations!")
   await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="🌍 World Stations"))
   # await updateStatus(discord.ActivityType.listening, "🌍 World Stations", 15)
   # await updateStatus(discord.ActivityType.watching, "🌳 Powered by: radio.garden", 15)



client.run("[YOUR_TOKEN]")