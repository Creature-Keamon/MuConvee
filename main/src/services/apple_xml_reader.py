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
ARTIST_INDEX = 5

def read_apple_xml_file(file):
    """given an Apple Music playlist XML file, returns a dictionary and a list. The dictionary has information 
    about the playlist of format: 
    {Name: Description} 
    and the list with the songs of format:
    [[Name, Artist, Album, Year, Genre]]
    """

    tree = ET.parse(file)
    root = tree.getroot()
    data = root[0]
    playlist_xml = data[PLAYLIST_DATA_INDEX][0]
    tracklist_xml = data[SONG_INFO_INDEX]
    playlist_info = get_playlist_info(playlist_xml)
    tracklist_info = get_playlist_songs(tracklist_xml)
    
    for item in tracklist_info:
        print(item)
    return playlist_info, tracklist_info


#Gets and returns a dictionary with the playlist information in the format of {Name: Description}
def get_playlist_info(playlist_info):

    new_playlist_dict = {}
    #Skips over the xml keys
    for i in range(0, IMPORTANT_ITEM_INDEXES, SKIP_KEYS): 
        new_playlist_dict[playlist_info[i].text] = playlist_info[i+1].text
    return new_playlist_dict


#Gets and returns a list with the playlist tracklist in the format of [Name, Artist, Album, Year, Genre]
def get_playlist_songs(tracklist_info):

    song_list = []
    
    #Skips over track keys
    for i in range(1,len(tracklist_info), SKIP_KEYS):
        
        current_song_data = tracklist_info[i]
        song_name, artist = current_song_data[SONG_NAME_INDEX].text, current_song_data[ARTIST_INDEX].text
        current_song = [song_name,artist]
        keys = set(("Album", "Genre", "Year"))
        
        #Because the positions of the Album, Genre and Year data can differ between tracks,
        #we need to loop through the dict to find them
        for key in range(0,len(current_song_data),SKIP_KEYS):
            if len(keys) == 0:
                break
            if current_song_data[key].text in keys:
                current_song.append(current_song_data[key+1].text)
                keys.remove(current_song_data[key].text)
        song_list.append(current_song)
    return song_list

read_apple_xml_file("src/main/resources/Iron Deficient.xml")
