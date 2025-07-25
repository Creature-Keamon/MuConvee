import urllib.parse
import webbrowser
import helper
import requests
import base64
from flask import Flask, request
from spotify_call_helper import Spotify_call_helper


app = Flask(__name__)

client_id = ""
client_secret = ""
redirect_uri = "http://127.0.0.1:8888/callback"

@app.route('/')
def spotify_login():
    """Requests an access token without use of the PKCE standard.
    Users are Redirected to the Spotify website to login"""
    
    scopes = "playlist-read-private playlist-modify-private playlist-modify-public"
    state = helper.generate_random_string(16)
    
    redirect_url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode({
        "response_type": "code",
        "client_id": client_id,
        "scope": scopes,
        "redirect_uri" : redirect_uri,
        "state":state
    })
    webbrowser.open(redirect_url)
    return "redirecting to Spotify login"

@app.route('/callback')
def callback():
    """catches the callback request and extracts the auth code and 
    state from it, assuming no errors occurred. Upon an error 
    occurring, no attempts to retrieve the auth code or state are
    made.
"""
    auth_code = request.args.get("code")
    state = request.args.get("state")

    if state == None:
        return "An error occurred. Something has interrupted the authorisation process, you may try again."
    else:
        url = "Https://accounts.spotify.com/api/token"
        form = {"code": auth_code,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code"}
        headers = {"content-type": "application/x-www-form-urlencoded",
                   "Authorization": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode('utf-8')).decode('utf-8')}
        data = requests.post(url,form,headers=headers)
        data = data.json()
        
        bob = Spotify_call_helper(client_id, client_secret)


spotify_log = input("login to spotify? y/n")
if spotify_log.lower() == "y":
    if __name__ == '__main__':
        app.run(port=8888)
else:
   print("boohoo")