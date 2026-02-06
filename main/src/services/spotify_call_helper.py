import base64
import requests
from services.spotify_data_reader import extract_track_data

MAX_QUERY_LENGTH = 20
YEAR_LENGTH = 4

class SpotifyCallHelper:
    """defines methods for performing operations with the Spotify API
    """

    def __init__(self, client_id, client_secret):
        self.client_id = client_id 
        self.client_secret = client_secret 
        self.redirect_uri = "http://127.0.0.1:8888/callback"
        self.auth_code = ""
        self.playlist_list = []
        with open("spotify_credentials.muco", 'r') as f:
            f = f.read()
            f = f.splitlines()
            f.close()
        self.access_token = f[0]


    def data_requester(self, url, user_data = None):
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
            playlist_list.append({"playlist id": playlist["id"],
                                   "name": playlist["name"], 
                                   "description": playlist["description"],
                                   "length": playlist["tracks"]["total"]})
        return playlist_list


    def get_playlist_items(self, playlist_id):
        """given a playlist id, returns the entire tracklist and track information for
        the playlist, converted into the format of [Name, [Artist0,..., ArtistN], Album, Year].
        """
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        playlist_content = self.data_requester(url)
        tracklist = playlist_content["items"]
        track_items = []
        for item in tracklist:
            track_items.append(extract_track_data(item))
        return playlist_content


    def create_playlist(self, user_id, name, description):
        """creates a Spotify playlist with the given name and description,
        and returns the playlist's id ready for adding songs."""
       
        url = f"https://api.spotify.com/v1/{user_id}/playlists"
        data = {"name":name,"description":description}
        returned_data = self.data_requester(url, data)
        return returned_data["id"]

    
    def add_to_playlist(self, playlist_id, song, send=False):
        """give a song, and this function will add it to a list. Once the 
        list becomes MAX_QUERY_LENGTH (or there are no more songs to add) 
        add_to_playlist_helper is called to add them to the appropriate 
        playlist.
        """
        
        self.playlist_list.append(song)
        if len(self.playlist_list) == MAX_QUERY_LENGTH or send:
            callback = self.add_to_playlist_helper(playlist_id)

    
    def add_to_playlist_helper(self, playlist_id):
        data = {"uris":[f"{item}," for item in self.playlist_list]}
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        snapshot = self.data_requester(url, data)
        return snapshot

def get_service(service):
    if service == "spotify":
        print("starting Spotify playlist getter service")
        with open("spotify_keys.muco", encoding="utf8") as keys:
            keys = keys.read()
            keys = keys.splitlines()
            client_id = keys[0]
            client_secret = keys[1]
        spotify_caller = SpotifyCallHelper(client_id, client_secret)
        print("Getting user playlists")
        spotify_caller.get_user_playlists()
    else:
        print("syntax error: either you typed a service that is unavailable, or a misspelling has occurred.")