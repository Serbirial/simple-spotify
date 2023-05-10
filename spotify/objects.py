

class SpotifyAlbum(object): 
    """ Spotify Album Object

    this can be re-used to trick things into thinking a playlist is an album as you will only get returned a list of tracks when getting playlists
    letting you use the same logic in your project as you would for albums """
    def __init__(self, name, tracks: list = None, total: int = None):
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