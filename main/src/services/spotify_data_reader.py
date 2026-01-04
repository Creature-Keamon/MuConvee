def extract_track_data( data):
    """given data about the recieved tracks, returns a list of lists with
    the track link, track name, [artist link, artist name]+, album link and 
    album name"""

    tracks = list(data["tracks"]["items"])
    tracklist = []
    for track in tracks:
        artists = {}
        for artist_num in range(len(track["artists"])):
            artists[
                "artist link " + str(artist_num)
                ] = track["artists"][artist_num]["external_urls"]["spotify"]
            artists[
                "artist " + str(artist_num)
                ] = track["artists"][artist_num]["name"]       
        tracklist.append({"track link": track["external_urls"]["spotify"],
                            "track": track["name"], 
                            "album link": track["album"]["external_urls"]["spotify"], 
                            "album": track["album"]["name"]} + artists)       
    return tracklist
