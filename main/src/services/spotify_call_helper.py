from secrets import token_bytes
import requests
import base64

class Spotify_call_helper:

    def __init__(self, client_id, client_secret):
        self.client_id = client_id 
        self.client_secret = client_secret 
        self.redirect_uri = "http://127.0.0.1:8888/callback"
        self.auth_code = ""
        with open("spotify_credentials.muco") as f:
            f = f.read()
            f = f.splitlines()
        self.access_token = f[0]


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
            error_message = token_data["error"]
            try:
                ConnectionRefusedError(f"data not received, received code {data.status_code} with message: {token_data['message']} instead.")
            except KeyError:
                ConnectionRefusedError(f"data not received, received code {data.status_code} with message: {error_message["message"]} instead.")

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
        playlists = list(playlist_data["items"])
        playlist_list = [[] for _ in playlists]
        print(playlists)
        for playlist in range(len(playlists)):
            current_playlist = playlists[playlist]
            playlist_list[playlist].append({"playlist link": current_playlist["external_urls"]["spotify"]})
            playlist_list[playlist].append({"playlist": current_playlist["name"]})
            
            playlist_list[playlist].append({"album link": current_playlist["album"]["external_urls"]["spotify"]})
            playlist_list[playlist].append({"album": current_playlist["album"]["name"]})
        print(playlist_list)
