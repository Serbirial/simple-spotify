# simple-spotify
Simple Spotify Library for Python


## Installation
For now, there is not way to install, please just drag/drop the folder until the project is in a more complete state, and is pip-installable 


## Usage 
getting a tracks data
```
from spotify.spotify import SpotifyInterface


spotify = SpotifyInterface(CLIENT_ID, CLIENT_SECRET)

to_search = input("Please enter a spotify track ID: ")

track = spotify.search_track_id(to_search)

print(f"{track.name} By {track.artist} ({track.album})")
```


# Roadmap/Planned Features
## Planned
- [x] Track searching
- [x] Album searching
- [x] No-Credential (ID only) authentication
- [] Multiple track searching
- [] Returning full data with Track/Album objects

## Not planned (PR only)
- [] Interacting with spotify (liking/saving/etc)
- [] Authenticating by password/oauth/etc (non-user ID only authentication)