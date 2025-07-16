import requests
import base64

client_id = ""
client_secret = ""
url = "https://accounts.spotify.com/api/token"
headers = {"Authorization": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode('utf-8')).decode('utf-8')}
form = {'grant_type': 'client_credentials'}

response = requests.post(url,form, headers= headers)

if response.status_code == 200:
    token_data = response.json()
    print(token_data)
    url = "https://api.spotify.com/v1/artists/6fuALtryzj4cq7vkglKLxq"
    print(token_data['access_token'])
    headers = {"Authorization": "Bearer " + token_data['access_token']}
    response2 = requests.get(url, form, headers=headers)
    data = response2.json()
    for key, value in data.items():
        print(key,value)
    
