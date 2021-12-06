from typing import List, Union
import spotipy
from discord import FFmpegOpusAudio
from sakura.utils.secrets import get_secret
from spotipy.oauth2 import SpotifyClientCredentials
from abc import ABC, abstractproperty

class Music(ABC):

    @abstractproperty
    def song_name(self):
        pass
    
    @abstractproperty
    def song_artists(self) -> List[str]:
        pass

    @abstractproperty
    def audio_source(self):
        pass

class SpotifyPreviewMusic(Music):
    def __init__(self, track_id: str, spotify: Union[spotipy.Spotify, None] = None):
        if spotify is None:
            auth = SpotifyClientCredentials(
                client_id = get_secret("spotify", "client_id"),
                client_secret = get_secret("spotify", "client_secret")
            )

            spotify = spotipy.Spotify(auth_manager=auth)

        self.track = spotify.track(track_id)

    @property
    def song_name(self):
        return self.track["name"]

    @property
    def song_artists(self):
        return [
            artist["name"]
            for artist in self.track["artists"]
        ]

    @property
    def audio_source(self):
        return FFmpegOpusAudio(
            self.track["preview_url"]
        )

