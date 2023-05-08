

class SpotifyAlbum(object):
    def __init__(self, name, tracks: list = None, total: int = None):
        self.name          = name
        self.tracks        = tracks if tracks else []
        self.total         = total

class SpotifyTrack(object):
    def __init__(self, name, artist, album, other_artists):
        self.name          = name
        self.artist        = artist
        self.album         = album
        self.other_artists = other_artists