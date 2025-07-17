import requests
import base64

spotify_client_id = "5ecb385927d94694819928aa033f888c"
spotify_client_secret = "7b5b6a9f89ea45fb9bd55773c6c838ba"

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
    
def spotify_search_track(search_query, access_token, type=0):
    
    query_split = list(search_query.split(" "))
    url = "https://api.spotify.com/v1/search?q="

    prev_token = None
    
    for item in query_split:
        if item.lower() in {"track:", "album:", "artist:", "year:", "genre:"}:
            url += "%2520"+ item[:-1] + "%3A"
            prev_token = "key"
        
        else:
            if ":" in item:
                print(item)
                item = item.replace(":", "%3A")
                url += item
                prev_token = "value + semi"

            else:
                if prev_token in {"key","value + semi"}:
                    url += item
                else:
                    url += "%2520" + item
                prev_token = "value"
    url += "&type=track"
    headers = {"Authorization": "Bearer " + access_token}
    data = requests.get(url,headers=headers)
    data = data.json()
    print(url)
    print(data)


        

token_data = establish_spotify_connection(spotify_client_id, spotify_client_secret)
    
spotify_search_track("track: Subboreal artist: The Ocean", token_data["access_token"])
    
