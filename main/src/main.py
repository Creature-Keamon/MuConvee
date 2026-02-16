from services import auth_getter
from services.spotify_call_helper import get_service
from services.apple_xml_reader import open_playlist
import time

PREFIX_LENGTH = 4

commands = {"help":"displays all available commands",
            "quit":"shuts MuConvee down",
            "auth": "start authentication service",
            "get spotify": "gets all playlists from the logged in account from the specified service"}

global client_id
global client_secret

def main():  
    """MuConvees' 'main loop'. Calls other functions to perform all of it's actions."""
    spotify_caller = False
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
        elif option[0:PREFIX_LENGTH].lower() == "get ":
            get_service(option[PREFIX_LENGTH:])  
            spotify_caller == True
        elif option.lower() == "convert playlist":
            if spotify_caller == None:
                print("You must get your Spotify data first!")
            else:
                open_playlist()
        else:
            print("Not a valid command. Please try again.")


if __name__ == "__main__":
    main()