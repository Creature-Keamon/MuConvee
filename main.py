import requests
import base64

client_id = "5ecb385927d94694819928aa033f888c"
client_secret = "faaf18e18019452b8a116b64bab4aaff"
url = "https://accounts.spotify.com/api/token"
headers = {"Authorisation": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode('utf-8')).decode('utf-8')}
form = {'grant_type': 'client_credentials'}

response = requests.post(url,form, headers= headers)

if response.status_code == 200:
    token_data = response.json()
    print(token_data)
else:
    print(f"Error: {response.status_code}")