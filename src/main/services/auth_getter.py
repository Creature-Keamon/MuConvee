import threading
import urllib.parse
import webbrowser
import helper
import requests
import base64
from flask import Flask, request
import time

services = {"Spotify": "sp",
            "Apple Music": "ap",
            "Qobuz": "qo"}

client_id = ""
client_secret = ""

app = Flask(__name__)

redirect_uri = "http://127.0.0.1:8888/spotcallback"
running = True
shutdown_flag = threading.Event()

@app.route('/spotlogin')
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


@app.route('/spotcallback')
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

        saved_data = open("spotify_credentials.muco", "w")
        for key, value in data.items():
            saved_data.write(f"{value}\n")
        webbrowser.open("http://127.0.0.1:8888/shutdown")
        return "authentication successful."


@app.route('/shutdown', methods={'GET'})
def shutdown():
    """Unfreezes the main thread, but keeps the server running for reauthentication"""

    global running
    running = False
    return "You may now close all tabs used to login to Spotify"

def run_spotify():
    app.run(port=8888)


def start():
    
    run = True
    while run:
        login_type = input("Which service would you like to sign into now? type help to see the commands, or quit to Quit the auth getter and return to the options screen. ")
        if login_type.lower() == "sp":
            with open("spotify_keys.muco") as keys:
                keys = keys.read()
                keys = keys.splitlines()
                global client_id
                global client_secret
                client_id = keys[0]
                client_secret = keys[1]
            t1 = threading.Thread(target=run_spotify)
            t1.start()
            webbrowser.open("http://127.0.0.1:8888/spotlogin")
            while running:
                print("running")
                time.sleep(1)
            
            
        if login_type.lower() == "ap":
            pass
        if login_type.lower() == "qo":
            pass
        if login_type.lower() == "quit":
            run = False
        if login_type.lower() == "help":
            for key, value in services.items():
                print(f"{key}: {value}")
    
    
    print("stopped")
