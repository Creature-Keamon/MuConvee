PLAYLIST_NAME_INDEX = 0
PLAYLIST_DESCRIPTION_INDEX = 1

def transfer_playlist(songlist, playlist_information, current_session):
    user_id = current_session.get_current_user_id()
    playlist_id, playlist_exists = check_playlist_creation(playlist_information, current_session, user_id)
    if playlist_exists:
        pass



def check_playlist_creation(playlist_information, current_session, user_id):
    """given the Apple Music playlist information, an instance of spotify_call_helper.SpotifyCallHelper and
    the current Spotify User's ID, either return the ID of an existing playlist or return the ID of a freshly
    created one"""

    spotify_playlists = current_session.get_user_playlists()
    apple_playlist_name = playlist_information[PLAYLIST_NAME_INDEX]
    apple_playlist_description = playlist_information[PLAYLIST_DESCRIPTION_INDEX]

    #checks if playlist already exists
    for spotify_playlist in spotify_playlists:
        if spotify_playlist["name"].lower() == apple_playlist_name.lower():
            return spotify_playlist["playlist id"], True
    return current_session.create_playlist(user_id, apple_playlist_name, apple_playlist_description), False


def add_to_existing_playlist(songlist):
    pass

def add_to_new_playlist(songlist):
    pass