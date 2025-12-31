from services import auth_getter
from services.spotify_call_helper import Spotify_call_helper
import time
 

commands = {"help":"displays all available commands",
            "quit":"shuts MuConvee down",
            "auth": "start authentication service",
            "get spotify": "gets all playlists from the logged in account from the specified service"}

global client_id
global client_secret

def startup():   
    loop = True
    while loop:
        option = input("What do you want to do? type 'help' for a list of commands. ")
        if option.lower() == "help":
            for key, value in commands.items():
                print(f"{key}: {value}")
        
        elif option.lower() == "quit":
            print("goodbye!")
            exit()

        elif option.lower() == "auth":
            print("starting authentication service")
            auth_getter.start()
        
        elif option.lower() == "get spotify":
            print("starting Spotify playlist getter service")
            with open("spotify_keys.muco", encoding="utf8") as keys:
                keys = keys.read()
                keys = keys.splitlines()
                client_id = keys[0]
                client_secret = keys[1]
            spotify_caller = Spotify_call_helper(client_id, client_secret)
            print("Getting user playlists")
            spotify_caller.spotify_get_user_playlists()
        else:
            print("Not a valid command. Please try again.")


startup()