# HEADERS #

def _build_headers(session_key = None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'
        }
    if session_key:
        headers['Authorization'] = f'Bearer {session_key}'
    return headers

def build_token_req_data(client_id, client_secret):
    return f'https://accounts.spotify.com/api/token', _build_headers(), {"grant_type": "client_credentials", "client_id": client_id, "client_secret": client_secret}

# REQUEST DATA #

def _build_req_data(endpoint: str, session_key = None, json: dict = None):
    return f'https://api.spotify.com/v1/{endpoint}', _build_headers(session_key), json

def build_track_search_req_data(track_id: str, session_key):
    return _build_req_data(f'tracks/{track_id}', session_key)

def build_album_track_req_data(album_id: str, session_key):
    return _build_req_data(f'albums/{album_id}/tracks', session_key)

def build_album_req_data(album_id: str, session_key):
    return _build_req_data(f'albums/{album_id}', session_key)

def build_many_tracks_req_data(track_ids: list, session_key):
    return _build_req_data(f'tracks?ids={"%2c".join(track_ids)}', session_key)


def build_playlist_tracks_req_data(playlist_id: str, session_key):
    return _build_req_data(f'playlists/{playlist_id}/tracks', session_key)

