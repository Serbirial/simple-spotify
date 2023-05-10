
SpotifyIDRegex = r"[0-9][0-9A-Za-z]+[0-9a-z]+"


class SpotifyAlbum(object): 
    """ Spotify Album Object 
        This is sometimes re-used for other things, like playlists. """
    def __init__(self, name, tracks: list = None, total: int = 0):
        self.name          = name
        self.tracks        = tracks if tracks else []
        self.total         = total

class SpotifyTrack(object):
    """ Spotify Track Object """
    def __init__(self, name, artist, album, other_artists):
        self.name          = name
        self.artist        = artist
        self.album         = album
        self.other_artists = other_artists