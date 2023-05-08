EMPTY_LIST = []

class SpotifyAlbum(object):
    def __init__(self, name, tracks: list = EMPTY_LIST, total: int = None):
        self.name          = name
        self.tracks        = tracks
        self.total         = total

class SpotifyTrack(object):
    def __init__(self, name, artist, album, other_artists):
        self.name          = name
        self.artist        = artist
        self.album         = album
        self.other_artists = other_artists