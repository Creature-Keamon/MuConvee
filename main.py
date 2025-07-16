import requests
import base64

client_id = "Client ID"
client_secret = "Client Secret"
url = "https://accounts.spotify.com/api/token"
headers = {"Authorization": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode('utf-8')).decode('utf-8')}
form = {'grant_type': 'client_credentials'}

response = requests.post(url,form, headers= headers)

if response.status_code == 200:
    token_data = response.json()
    print(token_data)
    url = "https://open.spotify.com/artist/6fuALtryzj4cq7vkglKLxq"
    print(token_data['access_token'])
    headers = {"Authorization": "Bearer " + base64.b64encode(token_data['access_token'].encode('utf-8')).decode('utf-8')}
    response2 = requests.get(url, form, headers=headers)
    print(response2)
    data = response2.json()
    print(data)
