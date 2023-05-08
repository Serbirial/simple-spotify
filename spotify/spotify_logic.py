import time
import requests

from .request_data import *
from .objects import *

from threading import Thread

def thread_object(loop_def):
    expiration_loop = Thread(target=loop_def)
    expiration_loop.daemon = True
    expiration_loop.name = 'Token Expiration Thread'
    return expiration_loop

class SpotifyHandler:
    def __init__(self, client_id: str, client_secret: str):
        self.token_request_data  = build_token_req_data(client_id, client_secret)
        self.client_id           = client_id
        self.client_secret       = client_secret
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


    # Interfacing with spotify #

    def search_many_tracks(self, track_ids: list):
        """ Why individually send a request for every track to get info, when you can get everything all in one? """
        req_data   = build_many_tracks_req_data(track_ids, self.access_token)
        r = requests.get(req_data[0], headers=req_data[1])
        data = r.json()
        if r.status_code == 200:
            tracks = []
            for x in data["tracks"]:
                tracks.append(SpotifyTrack(
                    x["name"],
                    data["tracks"][0]["artists"][0]["name"],
                    x["album"]["name"],
                    None if len(data["tracks"][0]["artists"]) <= 1 else [y["name"] for y in data["tracks"][0]["artists"] if y["name"] != data["tracks"][0]["artists"][0]["name"]]
                    ))
        return tracks

    def search_id(self, track_id: str):
        """ Searches spotify, looking for a track with `track_id `"""
        req_data = build_track_search_req_data(track_id, self.access_token)
        r = requests.get(req_data[0], headers=req_data[1])
        data = r.json()
        if r.status_code == 200:
            return SpotifyTrack(
                data["name"],
                data["artists"][0]["name"],
                data["album"]["name"],
                None if len(data["artists"]) <= 1 else [x["name"] for x in data["artists"] if x["name"] != data["artists"][0]["name"]]
                )

    def search_album_tracks(self, album_id: str):
        """ Gets all tracks off an album, searches for album by `album_id` """
        req_data   = build_album_track_req_data(album_id, self.access_token)
        album_req = build_album_req_data(album_id, self.access_token)
        r = requests.get(req_data[0], headers=req_data[1])
        r2 = requests.get(album_req[0], headers=album_req[1])
        data = r.json()
        album = None
        if r2.status_code == 200: album = r2.json()["name"]
        if r.status_code == 200:
            album_obj = SpotifyAlbum(name=album, total=data["total"])
            for x in data["items"]:
                album_obj.tracks.append(SpotifyTrack(
                    x["name"],
                    data["items"][0]["artists"][0]["name"],
                    album,
                    None if len(data["items"][0]["artists"]) <= 1 else [y["name"] for y in data["items"][0]["artists"] if y["name"] != data["items"][0]["artists"][0]["name"]]
                    ))
        return album_obj

    def search_playlist_tracks(self, playlist_id: list):
        """ Get all tracks off a playlist, searches for playlist by `playlist_id` """
        req_data   = build_playlist_tracks_req_data(playlist_id, self.access_token)
        r = requests.get(req_data[0], headers=req_data[1])
        data = r.json()
        if r.status_code == 200:
            tracks = []
            for x in data["items"]:
                if x["track"]["type"] == "track":
                    tracks.append(SpotifyTrack(
                        x["track"]["name"],
                        x["track"]["artists"][0]["name"],
                        x["track"]["album"]["name"],
                        None if len(x["track"]["artists"]) <= 1 else [artist["name"] for artist in x["track"]["artists"] if artist["name"] != x["track"]["artists"][0]["name"]]
                        ))
        return tracks