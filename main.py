import discord
import configparser
from discord import commands, Button, SelectMenu, SelectOption, ButtonStyle, default_permissions
from discord.ui import View, Select, InputText, Modal
from discord.ext import commands
import musicBrainz
import json
import time
from datetime import timedelta, datetime
import asyncio
from asyncio import Semaphore, Lock
import os
discord_token = os.environ.get('DISCORD_TOKEN')
message = os.environ.get('PING_MESSAGE')
lock = asyncio.Lock()
config = configparser.ConfigParser()
config.read('config.ini')
config.set('SECRETS', 'Token', discord_token)
intents = discord.Intents.all()
intents.message_content = True
intents.presences = True
intents.members = True
prefix = config['GENERAL']['Prefix']
# Bot = commands.Bot(command_prefix=commands.when_mentioned_or(f'{prefix}'), intents=intents)
Bot = discord.Bot(intents=intents)
guildID=config['GENERAL']['guildID']
spotify = Bot.create_group("spotify", "Spotify querying")
currentGenres = config['GENERAL']['Genres']
currentArtists = config['GENERAL']['individualartists']
individual_artists = config['GENERAL']['individualartists']
folder_path = 'artists'
@Bot.event
async def on_ready():
    print(f'We have logged in as {Bot.user}')
    genres_str = config['GENERAL']['Genres']
    genres = genres_str.split(', ')
    Bot.loop.create_task(artistQuery(genres))
    async with lock:
        file_path = f'{folder_path}/customartist.json'
        with open(file_path, 'w') as file:
            json.dump(individual_artists.split(','), file)

wallofshame = Bot.create_group("wallofshame", "Modifying genre/artists")

class ModalGenreInput(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        config.read('config.ini')
        currentGenres = config['GENERAL']['genres']
        self.add_item(discord.ui.InputText(label="Genre", value=currentGenres, style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        if self.children[0].value != currentGenres:
            config['GENERAL']['genres'] = self.children[0].value
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
        embed = discord.Embed(title="Genre Updated")
        embed.add_field(value=self.children[0].value,name="Custom Genres")
        musicBrainz.write_artists()
        await interaction.response.send_message(embeds=[embed])

class ModalCustomArtistInput(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        config.read('config.ini')
        currentArtists = config['GENERAL']['individualartists']
        self.add_item(discord.ui.InputText(label="Custom Artists", value=currentArtists, style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        if self.children[0].value != currentArtists:
            config['GENERAL']['individualartists'] = self.children[0].value
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
        embed = discord.Embed(title="Custom Artists Updated")
        embed.add_field(value=self.children[0].value,name="Custom Artists")
        musicBrainz.write_artists()
        await interaction.response.send_message(embeds=[embed])

@wallofshame.command()
@default_permissions(manage_messages=True)
async def genre(ctx: discord.ApplicationContext):
    modal = ModalGenreInput(title="Input Genre")
    await ctx.send_modal(modal)
@wallofshame.command()
@default_permissions(manage_messages=True)
async def custom_artists(ctx: discord.ApplicationContext):
    modal = ModalCustomArtistInput(title="Input Custom Artists")
    await ctx.send_modal(modal)

@spotify.command(guild_ids=[guildID])
async def serverwide(ctx):
    found_spotify_activity = False
    for member in ctx.guild.members:
        if member.activities:
            for activity in member.activities:
                if isinstance(activity, discord.Spotify):
                    found_spotify_activity = True
                    embed = discord.Embed(title=f"{member.name}", description=f"Listening to {activity.title}", color=member.color)
                    embed.set_thumbnail(url=activity.album_cover_url)
                    embed.add_field(name="Artist", value=activity.artist)
                    embed.add_field(name="Album", value=activity.album)
                    embed.add_field(name="Duration", value=str(activity.duration)[2:7])
                    embed.add_field(name="Link", value=activity.track_url)
                    embed.set_footer(text=f"Song started at {activity.created_at.strftime('%H:%M')}")
                    await ctx.respond(embed=embed)
@spotify.command(guild_ids=[guildID])
async def personal(ctx):
    found_spotify_activity = False
    member=ctx.author
    if member.activities:
        for activity in member.activities:
            if isinstance(activity, discord.Spotify):
                found_spotify_activity = True
                embed = discord.Embed(title=f"{member.name}", description=f"Listening to {activity.title}", color=member.color)
                embed.set_thumbnail(url=activity.album_cover_url)
                embed.add_field(name="Artist", value=activity.artist)
                embed.add_field(name="Album", value=activity.album)
                embed.add_field(name="Duration", value=str(activity.duration)[2:7])
                embed.add_field(name="Link", value=activity.track_url)
                embed.set_footer(text=f"Song started at {activity.created_at.strftime('%H:%M')}")
                await ctx.respond(embed=embed)
                break
    if not found_spotify_activity:
        await ctx.respond("You are not playing anything")

async def spotifyold(ctx):
    found_spotify_activity = False
    for member in ctx.guild.members:
        if member.activities:
            for activity in member.activities:
                if isinstance(activity, discord.Spotify):
                    found_spotify_activity = True
                    embed = discord.Embed(title=f"{member.name}", description=f"Listening to {activity.title}", color=member.color)
                    embed.set_thumbnail(url=activity.album_cover_url)
                    embed.add_field(name="Artist", value=activity.artist)
                    embed.add_field(name="Album", value=activity.album)
                    embed.add_field(name="Duration", value=str(activity.duration)[2:7])
                    embed.add_field(name="Link", value=activity.track_url)
                    embed.set_footer(text=f"Song started at {activity.created_at.strftime('%H:%M')}")
                    await ctx.respond(embed=embed)
                    break
artists = []
last_activation={}
beforeStart=None
@Bot.event
async def on_presence_update(before, after):
    async with lock:
        config.read('config.ini')
        wallofShame = int(config["GENERAL"]['wallofShame'])
        listofGenres = config["GENERAL"]['genres']
        artists = []
        global beforeStart
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    artists_data = json.load(f)
                    artists.extend(artists_data)
        for activity in before.activities:
            if isinstance(activity, discord.Spotify):
                beforeStart=activity.start
                break
        for activity in after.activities:
            if isinstance(activity, discord.Spotify):
                for artist in activity.artists:
                    if artist in artists and activity.start != beforeStart:
                        activation_key = (after.name, artist, activity.title)  # Use activity.title as the third element of the activation key
                        print (activation_key)
                        print(f"before: {beforeStart}\nafter:{activity.start}")
                        current_time = time.time()
                        cooldown_duration = 3 # Set the cooldown duration in seconds
                        last_activation_time = last_activation.get(activation_key, 0)
                        if current_time - last_activation_time >= cooldown_duration:
                            artist = activity.artist.replace(";", "\n")
                            channel = Bot.get_channel(wallofShame)
                            embed = discord.Embed(title=activity.title, color=after.color)
                            embed.set_image(url=activity.album_cover_url)
                            embed.add_field(name="Artist", value=artist)
                            embed.add_field(name="Album", value=activity.album)
                            embed.add_field(name="Link", value=activity.track_url)
                            await channel.send(f"{after.mention} {message}", embed=embed)
                            last_activation[activation_key] = current_time  # Update the last_activation dictionary with the current activation time
                            print(f"{after.name} has been shamed")

async def on_voice_state_update(member, before, after):
    vcRoleName = config["GENERAL"]["VCRole"]
    vcRole = discord.utils.get(member.guild.roles , name=f"{vcRoleName}")
    channel_id = int(config["GENERAL"]["vcChatChannelId"])
    channel = Bot.get_channel(channel_id)
    deleteList = []
    if after.channel:
        await member.add_roles(vcRole)
        embed = discord.Embed(title=f"{member.name}", description=f"has joined voice chat", color=member.color)
        await channel.send(embed=embed)
    else:
        await member.remove_roles(vcRole)
        embed = discord.Embed(title=f"{member.name}", description=f"has left voice chat", color=member.color)
        await channel.send(embed=embed)
        async for msg in channel.history(limit=None):
            if msg.author.id == member.id:
                deleteList.append(msg)
        if len(deleteList) > 0:
            await channel.delete_messages(deleteList)
            print("vc-chat purged")

async def artistQuery(genres):
    print("musicBrainz query loaded")
    genres_str = config['GENERAL']['Genres']
    genres = genres_str.split(', ')
    musicBrainz.search_artists_by_genre(genre)
    print(f"{list(genres)} genres queried")
    await asyncio.sleep(86400)  # Delay for 24 hours
    Bot.loop.create_task(artistQuery(genres))  # Create a new task instead of awaiting

Bot.run(discord_token)