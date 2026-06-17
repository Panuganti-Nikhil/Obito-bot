import discord
from discord.ext import commands
import yt_dlp
import asyncio

# Suppress noise about console usage from errors
yt_dlp.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class MusicControlView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(label="Play/Pause", style=discord.ButtonStyle.primary, custom_id="music_play_pause")
    async def play_pause(self, interaction: discord.Interaction, button: discord.ui.Button):
        ctx = await self.cog.bot.get_context(interaction.message)
        if ctx.voice_client:
            if ctx.voice_client.is_playing():
                ctx.voice_client.pause()
                await interaction.response.send_message("Paused music.", ephemeral=True)
            elif ctx.voice_client.is_paused():
                ctx.voice_client.resume()
                await interaction.response.send_message("Resumed music.", ephemeral=True)
            else:
                await interaction.response.send_message("Nothing is playing.", ephemeral=True)
        else:
            await interaction.response.send_message("Bot is not in a voice channel.", ephemeral=True)

    @discord.ui.button(label="Skip", style=discord.ButtonStyle.secondary, custom_id="music_skip")
    async def skip(self, interaction: discord.Interaction, button: discord.ui.Button):
        ctx = await self.cog.bot.get_context(interaction.message)
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await interaction.response.send_message("Skipped track.", ephemeral=True)
        else:
            await interaction.response.send_message("Not playing any music.", ephemeral=True)

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.danger, custom_id="music_stop")
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        ctx = await self.cog.bot.get_context(interaction.message)
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await interaction.response.send_message("Stopped and disconnected.", ephemeral=True)
        else:
            await interaction.response.send_message("Bot is not in a voice channel.", ephemeral=True)

class Music(commands.Cog, name="music"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="musicpanel")
    async def musicpanel(self, ctx):
        """Spawns the interactive music control panel."""
        embed = discord.Embed(title="Music Control Panel", description="Use the buttons below to control playback.", color=discord.Color.blue())
        view = MusicControlView(self)
        await ctx.send(embed=embed, view=view)

    @commands.command(name="join")
    async def join(self, ctx, *, channel: discord.VoiceChannel = None):
        """Joins a voice channel."""
        if not channel:
            if ctx.author.voice:
                channel = ctx.author.voice.channel
            else:
                await ctx.send("You are not connected to a voice channel.")
                return

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command(name="play")
    async def play(self, ctx, *, query):
        """Plays a song from youtube/url."""
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                return

        async with ctx.typing():
            try:
                player = await YTDLSource.from_url(query, loop=self.bot.loop, stream=True)
                ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
                await ctx.send(f'Now playing: {player.title}')
            except Exception as e:
                await ctx.send(f"An error occurred: {e}")

    @commands.command(name="pause")
    async def pause(self, ctx):
        """Pauses the currently playing track."""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Paused playback.")
        else:
            await ctx.send("Nothing is playing right now.")

    @commands.command(name="resume")
    async def resume(self, ctx):
        """Resumes the paused track."""
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Resumed playback.")
        else:
            await ctx.send("Nothing is paused right now.")

    @commands.command(name="skip")
    async def skip(self, ctx):
        """Skips the currently playing track."""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Skipped track.")
        else:
            await ctx.send("Nothing is playing right now.")

    @commands.command(name="stop")
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice."""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Disconnected.")
        else:
            await ctx.send("Not connected to a voice channel.")

    @commands.command(name="volume")
    async def volume(self, ctx, volume: int):
        """Changes the player's volume."""
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command(name="nowplaying")
    async def nowplaying(self, ctx):
        """Shows the currently playing track."""
        if ctx.voice_client and ctx.voice_client.source:
            await ctx.send(f"Currently playing: {ctx.voice_client.source.title}")
        else:
            await ctx.send("Nothing is playing right now.")
