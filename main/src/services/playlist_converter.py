PLAYLIST_NAME_INDEX, ARTISTS_INDEX, FIRST_ARTIST_INDEX, SONG_NAME_INDEX = 0, 0, 0, 0
PLAYLIST_DESCRIPTION_INDEX = 1

from services.spotify_data_reader import extract_track_data

def transfer_playlist(songlist, playlist_information, current_session):
    user_id = current_session.get_current_user_id()
    playlist_id, playlist_exists = check_playlist_creation(playlist_information, current_session, user_id)
    if playlist_exists:
        add_to_existing_playlist(songlist, playlist_id, current_session)
    else:
        add_to_new_playlist(songlist, playlist_id, current_session)



def check_playlist_creation(playlist_information, current_session, user_id):
    """given the Apple Music playlist information, an instance of spotify_call_helper.SpotifyCallHelper and
    the current Spotify User's ID, either return the ID of an existing playlist or return the ID of a freshly
    created one
    """

    spotify_playlists = current_session.get_user_playlists()
    apple_playlist_name = playlist_information[PLAYLIST_NAME_INDEX]
    apple_playlist_description = playlist_information[PLAYLIST_DESCRIPTION_INDEX]

    #checks if playlist already exists
    for spotify_playlist in spotify_playlists:
        if spotify_playlist["name"].lower() == apple_playlist_name.lower():
            return spotify_playlist["playlist id"], True
    return current_session.create_playlist(user_id, apple_playlist_name, apple_playlist_description), False

def add_to_existing_playlist(songlist, playlist_id, current_session):
    pass

def add_to_new_playlist(songlist, playlist_id, current_session):

    for song in songlist:
        song = get_song(song, current_session)
        print(f"Current track: {song["name"]} by {song["artists"][1]}")
        song_id = song["id"]
        current_session.add_to_playlist(playlist_id, song_id)
        
        

def get_song(song, current_session):
    """"""
    # Sometimes metadata between services is inconsistent,
    # so we only search using the song name and artist name
    # initially to avoid the chance of a potential metadata
    # discrepency fetching the wrong track.
    query = song[SONG_NAME_INDEX] + '' + song[ARTISTS_INDEX][FIRST_ARTIST_INDEX]   
    spotify_song_information = current_session.search_track(query)
    tracklist = spotify_song_information["items"]
    track_items = []
    for item in tracklist:
        track_items.append(extract_track_data(item))
    return track_items[0] #may replace with fuzzy search algorithm