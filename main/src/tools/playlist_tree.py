""""""

class Leaf:
    def __init__(self, previous, name, artist, album, song_id):
        self.previous = previous
        self.name = name
        self.artist = artist
        self.album = album
        self.song_id = song_id
        obj = "L"


    def set_previous(self, previous):
        self.previous = previous


class Node:
    def __init__(self, previous = None):
        self.previous = previous
        self.letters = set()
        self.links = set()
        obj = "N"

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
    letterlist = list(song)
    letterlist.reverse()
    node = root
    current_letter = letterlist.pop()
    current_obj = "N"
    letter_exists = current_letter in node.letters
    # traverses the current tree until either a song leaf or a location for the song to go is found
    while letter_exists and current_obj == "N":

        # loops through the connected nodes to find the correct letter
        for tup in node.links:
            if tup[0] == letterlist[0]:
                node = tup[1]
                current_letter = letterlist.pop()
                current_obj = node.obj
                letter_exists = current_letter in node.letters
                break

def move_leaf(leaf, letter):
    new_node = Node()
    previous = letter.previous()
    new_node.set_previous(previous)
