def extract_track_data(track):
    """given data about a track, returns a list of lists with the track 
    link, track name, [artist link, artist name], album link and  album 
    name.
    """

    artists = {}
    for artist_num in range(len(track["artists"])):
        artists[
            "artist link " + str(artist_num)
            ] = track["artists"][artist_num]["external_urls"]["spotify"]
        artists[
            "artist " + str(artist_num)
            ] = track["artists"][artist_num]["name"]       
    track_info = {"track link": track["external_urls"]["spotify"],
                        "name": track["name"], 
                        "album link": track["album"]["external_urls"]["spotify"], 
                        "album": track["album"]["name"]} + artists 
    return track_info
