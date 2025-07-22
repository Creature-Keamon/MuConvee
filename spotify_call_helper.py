import requests
import base64
import urllib.parse
import helper
from flask import Flask, redirect

# instance of flask application
app = Flask(__name__)


class Spotify_call_helper:

    def __init__(self, client_id, client_secret):
        self.client_id = client_id 
        self.client_secret = client_secret 
        self.redirect_uri = "http://127.0.0.1:8888/callback"
        self.auth_code = ""
        self.access_token = ""

    def get_spotify_data(self, url):
        """given a Spotify URL and a valid access token, requests the data at the 
        link. Throws ConnectionRefusedError if the incoming status code is anything
        other than 200."""

        header = {"Authorization": "Bearer " + self.access_token}
        data = requests.get(url, headers=header)
        token_data = data.json()

        if data.status_code == 200:
            return token_data
        else:
            ConnectionRefusedError(f"data not received, received code {data.status_code} with message: {token_data["message"]} instead.")


    def establish_spotify_connection(self):
        """Given a client ID, client secret and API URL, a connection request to Spotify
        is made, raises ConnectionRefusedError if the status code recieved is anything
        other than 200."""
        
        url = "https://accounts.spotify.com/api/token"
        headers = {"Authorization": "Basic " + base64.b64encode(f"{self.client_id}:{self.client_secret}".encode('utf-8')).decode('utf-8')}
        form = {'grant_type': 'client_credentials'}
        data = requests.post(url,form, headers= headers)
        token_data = data.json()
        if data.status_code == 200:
            self.access_token = token_data["access_token"]
            return token_data
        else:
            ConnectionRefusedError(f"data not received, received code {data.status_code} with message: {token_data["message"]} instead.")        
        
    def spotify_search_track(self, search_query):
        """Given a search query and a valid access token, returns the top 3 results,
        and all related data, of that query from Spotify's servers."""

        query_split = list(search_query.split(" "))
        url = "https://api.spotify.com/v1/search?q="
        url += query_split[0]
        
        for item in query_split[1:]:
            url += "+" + item
        
        url += "&type=track&limit=3"
        data = self.get_spotify_data(url)
        return data


    def extract_track_data(self, data):
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


    def spotify_get_user_playlists(self):

        url = "https://api.spotify.com/v1/me/playlists"
        playlist_data = self.get_spotify_data(url)
        print(playlist_data)

@app.route('/spotify_login')
def spotify_login(client_id, redirect_uri):
    """Requests an access token without use of the PKCE standard.
    Users are Redirected to the Spotify website to login, and upon
    a successful login, an access code is recieved."""
    
    scopes = "playlist-read-private playlist-modify-private playlist-modify-public"
    state = helper.generate_random_string(16)
    
    redirect_url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode({
        "response_type": "code",
        "client_id": client_id,
        "scope": scopes,
        "redirect_uri" : redirect_uri,
        "state":state
    })
    return redirect(redirect_url)


if __name__== '__main__':
    bob = Spotify_call_helper("", "")
    if bob.auth_code == "":
        app.run(port=8888)
    else:
        pass
