from .spotify_logic import SpotifyHandler

class SpotifyInterface:
    def __init__(self, client_id: str, client_secret: str):
        self.spotify_handler = SpotifyHandler(client_id, client_secret)


    def search_track_id(self, track_id: str):
        """ Search a track on spotify. `track_id` is a spotify track ID, returns a SpotifyTrack object."""
        return self.spotify_handler.search_id(track_id)

    def search_album_tracks(self, album_id: str):
        """ Search an albums tracks on spotify. `album_id` is a spotify track ID, returns a SpotifyAlbum object"""
        return self.spotify_handler.search_album_tracks(album_id)

    def search_many_tracks(self, tracks_ids: list):
        """ Search for multiple tracks at once. `track_ids` is a list full of spotify track IDs, returns a list of SpotifyTrack objects """
        return self.spotify_handler.search_many_tracks(album_id)

    def search_playlist_tracks(self, playlist_id: str):
        """ Search a playlists tracks on spotify. `playlist_id` is a spotify playlist ID, returns a list of SpotifyTrack objects"""
        return self.spotify_handler.search_playlist_tracks(album_id)