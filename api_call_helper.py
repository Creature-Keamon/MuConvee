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
    
def spotify_search(search_query, access_token, type=0):
    
    query_split = list(search_query.split(" "))
    url = "https://api.spotify.com/v1/search?q="
    if query_split[0][:-1].lower() in {"track", "album", "artist", "year", "genre"}:
        url += query_split[0][:-1]
    prev_token = None
    for item in query_split:
        if item[:-1].lower() in {"track", "album", "artist", "year", "genre"}:
            url += "%2520"+ item[:-1]
            prev_token = "key"
        else:
            if prev_token == "value":
                url += "%2520" + item
            else:
                url += "%3A" + item
            prev_token = "value"
    headers = {"Authorization": "Bearer " + access_token}
    print(url)
    data = requests.get(url,headers=headers)
    print(data.status_code)




        

token_data = establish_spotify_connection(spotify_client_id, spotify_client_secret)
    
spotify_search("track: Devonian: Nascent artist: The Ocean", token_data["access_token"])
    
