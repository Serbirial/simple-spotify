# Global Spotify API base
BASE = 'https://api.spotify.com/v1/'

# Build a usable API URL
def route(endpoint: str) -> str:
    return BASE + endpoint

def _build_token_req_data(client_id, client_secret):
    return f'https://accounts.spotify.com/api/token', build_headers(), {"grant_type": "client_credentials", "client_id": client_id, "client_secret": client_secret}


# Construct API request headers
def build_headers(session_key: str = None) -> dict:
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'
        }
    if session_key:
        headers['Authorization'] = f'Bearer {session_key}'
    return headers


