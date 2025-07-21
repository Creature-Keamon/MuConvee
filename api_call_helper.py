import hashlib
import string
import requests
import base64
import secrets
import urllib.parse

from flask import Flask,redirect

app = Flask(__name__)
spotify_client_id = "5ecb385927d94694819928aa033f888c"
spotify_client_secret = "cdac46ae967e4609b3b30d5982f67a7e"
redirect_uri = "http://127.0.0.1:8888/callback"
auth_code = ""


def get_spotify_data(url, access_token):
    """given a Spotify URL and a valid access token, requests the data at the 
    link. Throws ConnectionRefusedError if the incoming status code is anything
    other than 200."""

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





def spotify_login():
    scopes = "playlist-read-private playlist-modify-private playlist-modify-public"
    state = generate_random_string(64);
    
    redirect_url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode({
        "response_type": "code",
        "client_id": spotify_client_id,
        "scope": scopes,
        "redirect_uri" :redirect_uri,
        "state":state
    })
    return redirect(redirect_url)
    
    
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
    if auth_code == "":

        code = spotify_login()
    access_token = establish_spotify_connection(spotify_client_id,spotify_client_secret)
    app.run(port=8888)
    
    
    access_token = access_token["access_token"]
    extract_track_data(spotify_search_track("Devonian: Nascent The Ocean", access_token))
    spotify_get_user_playlists(access_token)