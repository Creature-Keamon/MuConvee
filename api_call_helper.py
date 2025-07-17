import requests
import base64

spotify_client_id = ""
spotify_client_secret = ""

def establish_spotify_connection(client_id, client_secret):
    """Given a client ID, client secret and API URL, a connection request to Spotify
    is made, raises ConnectionRefusedError if the status code recieved is anything
    other than 200."""
    
    url = "https://accounts.spotify.com/api/token"
    headers = {"Authorization": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode('utf-8')).decode('utf-8')}
    form = {'grant_type': 'client_credentials'}
    response = requests.post(url,form, headers= headers)

    if response.status_code == 200:
        token_data = response.json()
        return token_data
    else:
        raise ConnectionRefusedError(f"data not received, received code {response.status_code} instead.")
    
def spotify_search_track(search_query, access_token):
    """Given a search query and a valid access token, returns the top 3 results,
    and all related data, of that query from Spotify's servers."""

    query_split = list(search_query.split(" "))
    url = "https://api.spotify.com/v1/search?q="
    url += query_split[0]
    
    for item in query_split[1:]:
        url += "+" + item
    
    url += "&type=track&limit=3"
    headers = {"Authorization": "Bearer " + access_token}
    data = requests.get(url,headers=headers)
    data = data.json()
    return data

def extract_track_data(data):
    tracks = data["tracks"]["items"]
    print(tracks)


    

extract_track_data(spotify_search_track("Subboreal The Ocean", 
                   establish_spotify_connection(spotify_client_id,spotify_client_secret)["access_token"]))