from services import auth_getter
from services.spotify_call_helper import Spotify_call_helper
import time
 

commands = {"help":"displays all available commands", 
            "quit":"shuts MuConvee down", 
            "auth": "start authentication service",
            "get <service>": "gets all playlists from the logged in account from the specified service"}


def startup():

    print("Hello!")
    time.sleep(1)
    print("Welcome to")
    time.sleep(1)
    print(""" ____    ____            ______                                       
|_   \\  /   _|         .' ___  |                                      
  |   \\/   |  __   _  / .'   \\_|  .--.   _ .--.  _   __  .---.  .---. 
  | |\\  /| | [  | | | | |       / .'`\\ \\[ `.-. |[ \\ [  ]/ /__\\\\/ /__\\\\
 _| |_\\/_| |_ | \\_/ |,\\ `.___.'\\| \\__. | | | | | \\ \\/ / | \\__.,| \\__.,
|_____||_____|'.__.'_/ `.____ .' '.__.' [___||__] \\__/   '.__.' '.__.'""")
    print("version 0.2n (the n is for non-functional)\n")
    
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
            print("starting Spotify service")
            with open("spotify_keys.muco") as keys:
                keys = keys.read()
                keys = keys.splitlines()
                global client_id
                global client_secret
                client_id = keys[0]
                client_secret = keys[1]
            spotify_caller = Spotify_call_helper(client_id, client_secret)
            print("Getting user playlists")
            spotify_caller.spotify_get_user_playlists()
            
        
        else:
            print("Not a valid command. Please try again.")


startup()