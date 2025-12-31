import base64
import requests


class SpotifyCallHelper:
    """defines methods for performing operations with the Spotify API
    """

    def __init__(self, client_id, client_secret):
        self.client_id = client_id 
        self.client_secret = client_secret 
        self.redirect_uri = "http://127.0.0.1:8888/callback"
        self.auth_code = ""
        self.playlist_list = []
        with open("spotify_credentials.muco") as f:
            f = f.read()
            f = f.splitlines()
        self.access_token = f[0]


    def data_requester(self, url, user_data={}):
        """Helper function. Given a Spotify URL and a valid access token, requests 
        the data at the link. Throws ConnectionRefusedError if the incoming status
        code is anything other than 200."""

        header = {"Authorization": "Bearer " + self.access_token}
        data = requests.get(url, headers = header,data = user_data)
        token_data = data.json()

        if data.status_code == 200:
            return token_data
        else:
            error_message = token_data["error"]
            try:
                raise ConnectionRefusedError(f"data not received, received code {data.status_code} with message: {token_data['message']} instead.")
            except KeyError:
                raise ConnectionRefusedError(f"data not received, received code {data.status_code} with message: {error_message["message"]} instead.")


    def establish_connection(self):
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
            raise ConnectionRefusedError(f"data not received, received code {data.status_code} with message: {token_data["message"]} instead.")        
       

    def search_track(self, search_query):
        """Given a search query and a valid access token, returns the top 3 results,
        and all related data, of that query from Spotify's servers."""

        query_split = list(search_query.split(" "))
        url = "https://api.spotify.com/v1/search?q="
        url += query_split[0]       
        for item in query_split[1:]:
            url += "+" + item      
        url += "&type=track&limit=3"
        data = self.data_requester(url)
        return data


    def get_current_user_id(self):
        "returns the id of the currently logged in user"

        url = "https://api.spotify.com/v1/me/playlists"
        userdata = self.data_requester(url)
        return userdata["id"]


    def get_user_playlists(self):
        """returns a list with the current logged in user's playlists with 
        information in a formatted dictionary like: 
        [{playlist link:string, name:string, length:integer, tracks link:string}]."""

        url = "https://api.spotify.com/v1/me/playlists"
        playlist_data = self.data_requester(url)
        playlists = list(playlist_data["items"])
        playlist_list = []
        for playlist in playlists:
            playlist_list.append({"playlist link": playlist["external_urls"]["spotify"],
                                   "name": playlist["name"], 
                                   "length": playlist["tracks"]["total"],
                                   "tracks link": playlist["tracks"]["href"]})
        return playlist_list


    def create_playlist(self, user_id, name, description):
        """creates a Spotify playlist with the given name and description,
        and returns the playlist's id ready for adding songs."""
       
        url = f"https://api.spotify.com/v1/{user_id}/playlists"
        data = {"name":name,"description":description}
        returned_data = self.data_requester(url, data)
        return returned_data["id"]

    def add_to_playlist(self, playlist_id, playlist_length, song, send):
        self.playlist_list.append(song)
        
        if len(self.playlist_list) == 20 or send:
            data = {"uris":[f"{item}," for item in self.playlist_list],"position":playlist_length}
            callback = self.add_to_playlist_helper(playlist_id, data)

    def add_to_playlist_helper(self, playlist_id, data):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        snapshot = self.data_requester(url, data)
        return snapshot