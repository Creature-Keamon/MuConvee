import requests
import base64
import secrets
import urllib.parse
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World"

spotify_client_id = ""
spotify_client_secret = ""
redirect_uri = ""

def get_spotify_data(url, access_token):

    header = {"Authorization": "Bearer " + access_token}
    data = requests.get(url, headers=header)
    token_data = data.json()
    print(token_data)
    if data.status_code == 200:
        return token_data
    else:
        ConnectionRefusedError(f"data not received, received code {data.status_code} with message: {token_data["message"]} instead.")


def establish_spotify_connection(client_id, client_secret):
    """Given a client ID, client secret and API URL, a connection request to Spotify
    is made, raises ConnectionRefusedError if the status code recieved is anything
    other than 200."""
    
    url = "https://accounts.spotify.com/api/token"
    headers = {"Authorization": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode('utf-8')).decode('utf-8')}
    form = {'grant_type': 'client_credentials'}
    data = requests.post(url,form, headers= headers)
    token_data = data.json()
    if data.status_code == 200:
        return token_data
    else:
        ConnectionRefusedError(f"data not received, received code {data.status_code} with message: {token_data["message"]} instead.")

def spotify_login(client_id,redirect_uri):
    scopes = "playlist-read-private playlist-modify-private playlist-modify-public"
    state = secrets.token_urlsafe(16);
    redirect_url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode({
        "response_type": "code",
        "client_id": client_id,
        "scope": scopes,
        "redirect_uri" :redirect_uri,
        "state":state
    })
    
    
def spotify_search_track(search_query, access_token):
    """Given a search query and a valid access token, returns the top 3 results,
    and all related data, of that query from Spotify's servers."""

    query_split = list(search_query.split(" "))
    url = "https://api.spotify.com/v1/search?q="
    url += query_split[0]
    
    for item in query_split[1:]:
        url += "+" + item
    
    url += "&type=track&limit=3"
    data = get_spotify_data(url, access_token)
    return data

def extract_track_data(data):
    """given data about the recieved tracks, returns a list of lists with
    the track link, track name, [artist link, artist name]+, album link and 
    album name"""

    tracks = list(data["tracks"]["items"])
    tracklist = [[] for _ in tracks]
    for track in range(len(tracks)):
        current_track = tracks[track]
        tracklist[track].append({"track link": current_track["external_urls"]["spotify"]})
        tracklist[track].append({"track": current_track["name"]})
        for artist_num in range(len(current_track["artists"])):
            tracklist[track].append({"artist link " + str(artist_num): current_track["artists"][artist_num]["external_urls"]["spotify"]})
            tracklist[track].append({"artist " + str(artist_num): current_track["artists"][artist_num]["name"]})
        tracklist[track].append({"album link": current_track["album"]["external_urls"]["spotify"]})
        tracklist[track].append({"album": current_track["album"]["name"]})
    return tracklist

def spotify_get_user_playlists(access_token):

    url = "https://api.spotify.com/v1/me/playlists"
    playlist_data = get_spotify_data(url, access_token)
    print(playlist_data)

if __name__== '__main__':
    app.run()
    

access_token = establish_spotify_connection(spotify_client_id,spotify_client_secret)
access_token = access_token["access_token"]


extract_track_data(spotify_search_track("Devonian: Nascent The Ocean", access_token))
spotify_get_user_playlists(access_token)