from typing import Any, List, Union
import spotipy
from discord import FFmpegOpusAudio
from sakura.utils.secrets import get_secret
from spotipy.oauth2 import SpotifyClientCredentials
import musicbrainzngs
from abc import ABC, abstractproperty

import logging
logger = logging.getLogger(__name__)

musicbrainzngs.set_useragent("Sakura", "1.0.0", contact="sakura+musicbrainz@hexf.me")

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
    def __init__(self, track_id: str, spotify: Union[spotipy.Spotify, None] = None, spotify_track_data: Any = None):
        if spotify is None and spotify_track_data is None:
            auth = SpotifyClientCredentials(
                client_id = get_secret("spotify", "client_id"),
                client_secret = get_secret("spotify", "client_secret")
            )

            spotify = spotipy.Spotify(auth_manager=auth)

        if spotify_track_data is None:
            self.track = spotify.track(track_id)
        elif spotify_track_data is not None:
            self.track = spotify_track_data

        isrc = self.track["external_ids"]["isrc"]

        logger.debug(f"Getting track from musicbrainz by {isrc=}")
        self.mbmeta = []

        try:
            self.mbmeta = musicbrainzngs.get_recordings_by_isrc(
                isrc,
                includes = ["artists"]
            )

            logger.debug(f"Got track metadata: {self.mbmeta}")
        except:
            logger.debug(f"Couldn't find this recording on musicbrains using the given isrc")

        if len(self.mbmeta) > 0:
            # we have musicbrainz data, lets use it
            self.mbrecording = self.mbmeta["isrc"]["recording-list"][0]

            self.track_name = self.mbrecording["title"]

            self.artists = [
                credit["artist"]["name"]
                for credit in self.mbrecording["artist-credit"]
                if type(credit) is not str
            ]

        else:
            # we have to default to spotify data

            self.track_name = self.track["name"]

            self.artists = [
                artist["name"]
                for artist in self.track["artists"]
            ]

    @property
    def song_name(self):
        return self.track_name

    @property
    def song_artists(self):
        return self.artists

    @property
    def audio_source(self):
        return FFmpegOpusAudio(
            self.track["preview_url"]
        )

