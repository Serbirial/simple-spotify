from .spotify_logic import SpotifyHandler

class SpotifyInterface:
    def __init__(self, client_id: str, client_secret: str):
        self.spotify_handler = SpotifyHandler(client_id, client_secret)


    def search_track_id(self, track_id: str):
        return self.spotify_handler.search_id(track_id)

    def search_album_tracks(self, album_id: str):
        return self.spotify_handler.search_album_tracks(album_id)