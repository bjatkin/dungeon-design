from validation.sokoban.sokomap import SokoMap

class HashTable:
    def __init__(self):
        self.table = {}


    def check_add(self, sokomap):
        key = str(sokomap.get_blocks() + [sokomap.get_player()])
        if key in self.table:
            return True
        else:
            self.table[key] = True
            return False