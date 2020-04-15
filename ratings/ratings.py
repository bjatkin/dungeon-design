import csv
import numpy as np

from generation.aesthetic_settings import AestheticSettings
from dungeon_level.dungeon_tiles import Tiles

class Ratings():
    CSV_SEPARATOR = "\t"
    ID_INDEX = 0
    SEED_INDEX = 1
    SETTINGS_INDEX = 2
    BRANDON_INDEX = -2
    RYAN_INDEX = -1
    def __init__(self, file):
        # Open the csv file
        self.file = file
        self.file_data = ''
        self.header = Ratings.CSV_SEPARATOR.join(["id", "seed"] + AestheticSettings.get_csv_header() + ["brandon_rating", "ryan_rating"]) + "\n"

        open(file, 'a').close() # Create a file if it doesn't exist.

        with open(file, 'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=Ratings.CSV_SEPARATOR)
            for i, row in enumerate(csv_reader):
                if i == 0:
                    continue
                self.file_data += Ratings.CSV_SEPARATOR.join(row) + "\n"

    def add_level(self, id, seed):
        settings = ["0"] * len(AestheticSettings.get_csv_data_paths())
        line = [str(id), str(int(seed))] + settings + ["0","0"]
        self.file_data += Ratings.CSV_SEPARATOR.join(line) + "\n"
        # print("Seed: {}".format(int(seed)))
        # print("File Data: ", self.file_data)
        # print("Sub Field Data: {},{}".format(id, int(seed)))
        # print("After:", Ratings.CSV_SEPARATOR.join(settings))
    
    def level_count(self):
        return len(self.file_data.splitlines())
    
    def add_rating(self, id, seed, name, aesthetics, rating):
        new_file_data = ""
        for row in self.file_data.splitlines():
            if self.header == row:
                continue
            data = row.split(Ratings.CSV_SEPARATOR)

            b_rating = data[Ratings.BRANDON_INDEX]
            r_rating = data[Ratings.RYAN_INDEX]
            if int(data[Ratings.ID_INDEX]) == id and int(data[Ratings.SEED_INDEX]) == int(seed):
                if name == "brandon":
                    b_rating = rating
                else:
                    r_rating = rating

                new_file_data += Ratings.CSV_SEPARATOR.join([str(data[Ratings.ID_INDEX]), str(data[Ratings.SEED_INDEX])] + aesthetics.get_csv_data() + [b_rating, r_rating]) + "\n"

            else:
                new_file_data += row+"\n"
            
        
        self.file_data = new_file_data

    def level_seed(self, i):
        return int(self.file_data.splitlines()[i].split(Ratings.CSV_SEPARATOR)[Ratings.SEED_INDEX])

    def level_aesthetic(self, i):
        data = self.file_data.splitlines()[i].split(Ratings.CSV_SEPARATOR)[Ratings.SETTINGS_INDEX:Ratings.SETTINGS_INDEX + len(AestheticSettings.get_csv_data_paths())]
        aesthetic = AestheticSettings()
        aesthetic.from_csv_data(data)
        return aesthetic

    def save(self):
        # Write file_data to file
            with open(self.file, 'w') as csvfile:
                csvfile.write(self.header + self.file_data)
