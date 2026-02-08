class leaf:
    def __init__(self, previous, name, artist, album, song_id):
        self.previous = previous
        self.name = name
        self.artist = artist
        self.album = album
        self.id = song_id

class branch:
    def __init__(self, letter, leaf):
        self.letter = letter
        self.leaf = leaf

class node:
    def __init__(self, previous, letter):
        self.previous = previous
        self.letter = letter
    

def construct_tree(playlist):
    pass