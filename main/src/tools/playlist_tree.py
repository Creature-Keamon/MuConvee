class Leaf:
    def __init__(self, previous, name, artist, album, song_id):
        self.previous = previous
        self.name = name
        self.artist = artist
        self.album = album
        self.song_id = song_id

class Node:
    def __init__(self, previous = None):
        self.previous = previous
        self.letters = set()
        self.links = set()
    
    def add_letter(self, letter, node):
        if not self.check_for_letter(letter):
            self.links.add(tuple(letter, node))
            self.letters.add(letter)
        

    def check_for_letter(self, letter):
        if letter in self.letters:
            return True
        else:
            return False
    
    def set_previous(self, previous):
        self.previous = previous

def tree_maker(songlist):
    root = Node()
    for song in songlist:
        tree_maker_helper(song, root)


def tree_maker_helper(song, root):
    pass