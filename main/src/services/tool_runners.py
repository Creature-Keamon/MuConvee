from services.spotify_call_helper import SpotifyCallHelper
from services.apple_xml_reader import read_apple_xml_file

def open_playlist():
    playlist = False
    while not playlist:
        file_loc = input("Please provide the location to an XML file playlist exported from Apple Music or iTunes.")
        try:
            with open(file_loc, "r") as playlist:
                if file_loc[-4:].lower() != ".xml":
                    print("This file is not an XML! Try again.")
                
                playlist_info, tracklist_info = read_apple_xml_file(playlist)
                print(tracklist_info)
        except FileNotFoundError:
            print("FileNotFoundError: sorry! Either that file does not exist, or a mistype has occurred.")

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