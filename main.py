import auth_getter
import time

commands = {"help":"displays all available commands", 
            "quit":"shuts MuConvee down", 
            "auth": "start authentication service", 
            "credits": "displays thanks to all contributors"}


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

        elif option.lower() == "credits":
            print("Thanks to our one contributor, Creature Keamon!")

        elif option.lower() == "auth":
            print("starting authentication service")
            auth_getter.start()
        
        else:
            print("Not a valid command. Please try again.")


startup()