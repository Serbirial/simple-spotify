# simple-spotify
Simple Spotify Library for Python


## Installation
For now, there is not a way to install, please just drag/drop the folder until the project is in a more complete state, and is pip-installable 


## Usage 
Getting a track’s data:
```py
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
- [x] Playlist searching
- [x] Multiple track searching
- [x] No-Credential (ID only) authentication
- [ ] Returning full data with Track/Album objects

## Not planned (PR only)
- [ ] Interacting with spotify (liking/saving/etc)
- [ ] Authenticating by password/oauth/etc (non-user ID only authentication)







# Notes
- I do not plan on covering the FULL spotify API myself, if you wish for something to be added thats not in the Planned section of the roadmap, please add a PR with the change.

- This library at its core is about getting data from spotify, not changing it, that would require code and developer input which defeats the point of this project, which is being simple as possible and requiring as little as possible on the developers end.

- This library does not support any way of authenticating other than client id/secret.