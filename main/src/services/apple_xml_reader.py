"""
apple_xml_reader_playlist.py
when given an XML file with the correct formatting, read_apple_xml_file returns a dictionary 
with the playlist name and description in the format of: {Name:Description} 
and a tracklist, with each entry in the format of: [Name, Artist, Album, Year, Genre]
"""
import xml.etree.ElementTree as ET 

PLAYLIST_DATA_INDEX = -1
SONG_INFO_INDEX = 17
IMPORTANT_ITEM_INDEXES = 4
SKIP_KEYS = 2
SONG_NAME_INDEX = 3

def read_apple_xml_file(file):
    """given an Apple Music playlist XML file, returns a dictionary and a list. The dictionary has information 
    about the playlist of format: 
    [Name, Description]
    and the list with the songs of format:
    [[Name, [Artist0,..., ArtistN], Album, Year]]
    """

    tree = ET.parse(file)
    root = tree.getroot()
    data = root[0]
    playlist_xml = data[PLAYLIST_DATA_INDEX][0]
    tracklist_xml = data[SONG_INFO_INDEX]
    playlist_info = get_playlist_info(playlist_xml)
    tracklist_info = get_playlist_songs(tracklist_xml)
    return playlist_info, tracklist_info


# Gets and returns a dictionary with the playlist information in the format of [Name, Description]
def get_playlist_info(playlist_info):

    new_playlist_info = []
    for i in range(0, IMPORTANT_ITEM_INDEXES, SKIP_KEYS): 
        new_playlist_info.append(playlist_info[i].text)
    return new_playlist_info


# Gets and returns a list with the playlist tracklist in the format of [Name, [Artist], Album, Year, Genre]
def get_playlist_songs(tracklist_info):

    song_list = []
    
    # Skips over track keys
    for i in range(1,len(tracklist_info), SKIP_KEYS):
        
        current_song_data = tracklist_info[i]
        song_name = current_song_data[SONG_NAME_INDEX].text
        current_song = [song_name,[]]
        keys = ["Album", "Year"]
        
        # Because the positions of the Album and Year data can differ between tracks,
        # we need to loop through the dict to find them
        for key in range(0,len(current_song_data),SKIP_KEYS):
            if len(keys) == 0:
                break
            # Need to find all artists considering there could be 1 to N of them per track
            if current_song_data[key].text == "Artist":
                current_song[1].append(current_song_data[key+1].text)
                
            if current_song_data[key].text == keys[0]:
                current_song.append(current_song_data[key+1].text)
                keys.pop(0)
        song_list.append(current_song)
    return song_list
