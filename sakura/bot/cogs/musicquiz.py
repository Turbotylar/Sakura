
import asyncio
from logging import Logger
from typing import List, Union

from discord.bot import Bot
from discord.guild import Guild
from discord.message import Message
from sakura.bot.utils.music import Music, SpotifyPreviewMusic
from discord.channel import TextChannel, VoiceChannel
from discord.commands.context import ApplicationContext
from discord.ext import commands
from sakura.bot.utils.command import sakura_command

import nltk
import spotipy
import random

from sakura.utils.secrets import get_secret
from spotipy.oauth2 import SpotifyClientCredentials


GUESS_TOLERANCE = 2


class MusicQuizGame():
    currently_playing: Union[Music, None]

    def __init__(self, bot: Bot, voice_channel: VoiceChannel, answers_channel: TextChannel, playlist: List[Music], logger: Logger, guild: Guild):
        self.bot = bot
        self.voice_channel = voice_channel
        self.answers_channel = answers_channel
        self.playlist = playlist

        self.voice_client = None
        self.currently_playing = None

        self.guessed_artist = False
        self.guessed_track = False

        self.points = {}

        self.logger = logger
        self.guild = guild

        self.active = True
        
    def song_finished(self, error):
        async def handle():
            if error is not None:
                await self.answers_channel.send(f"Sorry! An error occured while playing, and the game has been terminated. Final points {self.points}")
                await self.voice_client.disconnect()
                self.active = False

            await self.answers_channel.send(f"The song was **{self.currently_playing.song_name}** by **{' & '.join(self.currently_playing.song_artists)}**")
            if len(self.playlist) == 0:
                await self.answers_channel.send(f"That all folks! Thanks for playing! {self.points}")
                await self.voice_client.disconnect()
                self.active = False
            else:
                self.logger.debug("Queueing next song")
                await self.next_song()

        self.logger.debug(f"Song finished handler. Error: {error}")
        
        asyncio.run_coroutine_threadsafe(handle(), self.bot.loop)
        
    
    async def make_guess(self, message: Message):
        val = message.content.lower()
        valid = False
        if not self.guessed_track and nltk.edit_distance(val, self.currently_playing.song_name.lower()) <= GUESS_TOLERANCE:
            self.guessed_track = True
            valid = True
        elif not self.guessed_artist and min([
            nltk.edit_distance(val, artist.lower())
            for artist in self.currently_playing.song_artists
        ]) <= GUESS_TOLERANCE:
            self.guessed_artist = True
            valid = True

        self.logger.info(f"Guess of {val} has distances {[nltk.edit_distance(val, v.lower()) for v in [self.currently_playing.song_name, *self.currently_playing.song_artists]]}")
        
        if valid:
            await message.add_reaction("✅")
            await self.answers_channel.send(f"{message.author.mention} got it right! +1 pt")

            try:
                self.points[message.author.id] += 1
            except KeyError:
                self.points[message.author.id] = 1
            
            if self.guessed_artist and self.guessed_track:
                self.voice_client.stop() # trigger next song
        else:
            await message.add_reaction("❌")


            

            
        

    async def next_song(self):
        if self.voice_client is None or not self.voice_client.is_connected():
            self.voice_client = await self.voice_channel.connect()

        self.currently_playing = self.playlist.pop()
        self.guessed_artist = False
        self.guessed_track = False

        self.logger.info(f"Current track: {self.currently_playing.song_name} by {self.currently_playing.song_artists}")
        while self.voice_client.is_playing():
            pass

        self.logger.debug("Starting song")
        self.voice_client.play(self.currently_playing.audio_source, after=self.song_finished)



        

    


class MusicQuizCog(commands.Cog):
    current_games: List[MusicQuizGame]
    def __init__(self, client) -> None:
        self.client = client
        self.current_games = []
        auth = SpotifyClientCredentials(
                client_id = get_secret("spotify", "client_id"),
                client_secret = get_secret("spotify", "client_secret")
            )

        self.spotify = spotipy.Spotify(auth_manager=auth)
        self.spotify_playlist_items = self.spotify.playlist_items(
            get_secret("spotify", "quiz_playlist"),
            fields='items(track(id,preview_url,name, artists(name)))'
        )["items"]

        self.spotify_playlist_items = [item for item in self.spotify_playlist_items if item["track"]["preview_url"] is not None]

    @sakura_command()
    async def start_quiz(self, ctx: ApplicationContext):
        if ctx.author.voice is None:
            await ctx.respond("You are not in a voice channel")
        elif len([game for game in self.current_games if game.active and game.guild == ctx.guild]) != 0:
            await ctx.respond("You cannot have multiple games going at once")
        else:
            await ctx.defer()
            voice_channel = ctx.author.voice.channel
            answers_channel = ctx.channel

            playlist_items = random.sample(self.spotify_playlist_items, 15)
            
            playlist = [
                SpotifyPreviewMusic(item["track"]["id"], spotify_track_data=item["track"])
                for item in playlist_items
                ]
            game = MusicQuizGame(self.client, voice_channel, answers_channel, playlist, ctx.logger, ctx.guild)

            self.current_games.append(game)

            await game.next_song()

            await ctx.respond("Guess the song's name and artists!")
    
    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return

        for game in self.current_games:
            if game.active and game.answers_channel == message.channel:
                await game.make_guess(message)
                
        


def setup(bot):
    bot.add_cog(MusicQuizCog(bot))