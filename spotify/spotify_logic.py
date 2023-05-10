import time
import re
import requests

from .request_data import build_headers, route, _build_token_req_data
from .objects import SpotifyAlbum, SpotifyTrack, SpotifyIDRegex
from .cache import Cache

from threading import Thread

def thread_object(loop_def):
    expiration_loop = Thread(target=loop_def)
    expiration_loop.daemon = True
    expiration_loop.name = 'Token Expiration Thread'
    return expiration_loop

class SpotifyHandler:
    """ Do not use this unless you have looked through the source-code, this is for internal use. """
    def __init__(self, client_id: str, client_secret: str):
        self.token_request_data  = _build_token_req_data(client_id, client_secret)
        self.client_id           = client_id
        self.client_secret       = client_secret
        self.cache = Cache()
        self.create_access_token()

    # Authentication #

    def check_expiration_loop(self):
        if not hasattr(self, "expiration_thread"):
            thread = thread_object(self.expiration_loop)
            self.expiration_thread = thread
            self.expiration_thread.start()
        elif hasattr(self, "expiration_thread"):
            if not self.expiration_thread.is_alive():
                thread = thread_object(self.expiration_loop)
                self.expiration_thread = thread
                self.expiration_thread.start()

    def expiration_loop(self):
        while True:
            time.sleep(self.expiration)
            try:
                self.create_access_token()
            except Exception as e:
                self.error = e
                exit(0)

    def create_access_token(self):
        r = requests.post(self.token_request_data[0], self.token_request_data[2], headers=self.token_request_data[1], )
        if r.status_code == 200:
            data = r.json()
        else: 
            raise Exception(f"Couldnt create access token. ({r.status_code})")
        self.access_token = data["access_token"]
        self.expiration   = data["expires_in"]
        self.check_expiration_loop()

    # Internal

    def _put_object_in_cache(self, spotify_id: str, _object):
        """ Using this WILL cause the library to break. """
        self.cache.put(spotify_id, _object)

    # Interfacing with spotify #

    def search_many_tracks(self, track_ids: list) -> list:
        """ Why individually send a request for every track to get info, when you can get everything all in one? `track_ids` is a list of track IDs to search"""
        tracks = []
        # Check if ID is already in cache
        for _id in track_ids:
            if self.cache.get(_id):
                tracks.append(self.cache.get(_id))
        # All the tracks have been found in the cache
        if len(track_ids)==len(tracks):
            return tracks
        # Get tracks data
        r = requests.get(route(f"tracks?ids={'%2c'.join(track_ids)}"), headers=build_headers(self.access_token))
        data = r.json()
        if r.status_code == 200:
            for x in data["tracks"]:
                track = SpotifyTrack(
                    x["name"],
                    x["artists"][0]["name"],
                    x["album"]["name"],
                    None if len(x["artists"]) <= 1 else [y["name"] for y in x["artists"] if y["name"] != x["artists"][0]["name"]]
                    )
                # Put track in cache
                self._put_object_in_cache(x["id"], track)
                tracks.append(track)
            return tracks

    def search_id(self, track_id: str) -> SpotifyTrack:
        """ Searches spotify, looking for a track with `track_id `"""
        check = self.cache.get(track_id)
        if check:
            return check
        # Get track data
        r = requests.get(route(f'tracks/{track_id}'), headers=build_headers(self.access_token))
        data = r.json()
        if r.status_code == 200:
            track = SpotifyTrack(
                data["name"],
                data["artists"][0]["name"],
                data["album"]["name"],
                None if len(data["artists"]) <= 1 else [x["name"] for x in data["artists"] if x["name"] != data["artists"][0]["name"]]
                )
            # Put track in cache
            self._put_object_in_cache(track_id, track)
            return track

    def search_album_tracks(self, album_id: str) -> SpotifyAlbum:
        """ Gets all tracks off an album, searches for album by `album_id` """
        check = self.cache.get(album_id)
        if check:
            return check
        # Get album tracks data
        r = requests.get(route(f'albums/{album_id}/tracks'), headers=build_headers(self.access_token))
        # Get album data
        r2 = requests.get(route(f'albums/{album_id}'), headers=build_headers(self.access_token))
        data = r.json()
        album = None
        if r2.status_code == 200: album = r2.json()["name"]
        if r.status_code == 200:
            album_obj = SpotifyAlbum(name=album, total=data["total"])
            for x in data["items"]:
                album_obj.tracks.append(SpotifyTrack(
                    x["name"],
                    x["artists"][0]["name"],
                    album,
                    None if len(x["artists"]) <= 1 else [y["name"] for y in x["artists"] if y["name"] != x["artists"][0]["name"]]
                    ))
            # Put album in cache
            self._put_object_in_cache(album_id, album_obj)
            return album_obj

    def search_playlist_tracks(self, playlist_id: list) -> list:
        """ Get all tracks off a playlist, searches for playlist by `playlist_id`"""
        check = self.cache.get(playlist_id)
        if check:
            return check
        # Get playlist tracks data
        r = requests.get(route(f"playlists/{playlist_id}/tracks"), headers=build_headers(self.access_token))
        data = r.json()
        if r.status_code == 200:
            playlist_obj = SpotifyAlbum(name="User Playlist [PLAYLIST NAMES NOT SUPPORTED YET]")
            for x in data["items"]:
                if x["track"]["type"] == "track":
                    playlist_obj.tracks.append(SpotifyTrack(
                        x["track"]["name"],
                        x["track"]["artists"][0]["name"],
                        x["track"]["album"]["name"],
                        None if len(x["track"]["artists"]) <= 1 else [artist["name"] for artist in x["track"]["artists"] if artist["name"] != x["track"]["artists"][0]["name"]]
                        ))

                    playlist_obj.total += 1
            # Put playlist in cache
            self._put_object_in_cache(playlist_id, playlist_obj)
            return playlist_obj