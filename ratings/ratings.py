import csv
import numpy as np

from generation.aesthetic_settings import AestheticSettings
from dungeon_level.dungeon_tiles import Tiles

class Ratings():
    def __init__(self, file):
        # Open the csv file
        self.file = file
        self.file_data = ''
        self.header = "id,seed,"+AestheticSettings.csv_header()+"brandon_rating,ryan_rating\n"

        with open(file, 'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            for i, row in enumerate(csv_reader):
                if i == 0:
                    continue
                self.file_data += ','.join(row) + "\n"

    def add_level(self, id, seed):
        z = np.zeros(13).astype('str')
        print("SEED: {}".format(int(seed)))
        self.file_data += "{},{}".format(id, int(seed))+",".join(z)+",0,0\n"
        print("File Data: ", self.file_data)
        print("Sub Fild Data: {},{}".format(id, int(seed)))
        print("After:", ",".join(z))
    
    def level_count(self):
        return len(self.file_data.splitlines())
    
    def add_rating(self, id, seed, name, aesthetics, rating):
        new_file_data = ""
        for row in self.file_data.splitlines():
            if self.header == row:
                continue
            data = row.split(",")

            b_rating = data[14]
            r_rating = data[15]
            if int(data[0]) == id and int(data[1]) == int(seed):
                if name == "brandon":
                    b_rating = rating
                else:
                    r_rating = rating

                new_file_data  += "{},{},".format(data[0],data[1])+aesthetics.csv_data()+",{},{}\n".format(b_rating, r_rating)

            else:
                new_file_data += row+"\n"
            
        
        self.file_data = new_file_data

    def level_seed(self, i):
        return int(self.file_data.splitlines()[i].split(",")[1])

    def level_aesthetic(self, i):
        data = self.file_data.splitlines()[i].split(",")
        ret = AestheticSettings()
        ret.level_space_aesthetic.rectangle_count = int(data[2])
        ret.level_space_aesthetic.rectangle_min = int(data[3])
        ret.level_space_aesthetic.rectangle_max = int(data[4])
        ret.level_space_aesthetic.noise_percentage = float(data[5])
        ret.level_space_aesthetic.noise_empty_percentage = float(data[6])
        ret.mission_aesthetic.hazard_spread_probability[Tiles.water] = float(data[7])
        ret.mission_aesthetic.hazard_spread_probability[Tiles.fire] = float(data[8])
        ret.mission_aesthetic.single_lock_is_hazard_probability = float(data[9])
        ret.tweaker_aesthetic.should_fill_unused_space = bool(data[10])
        ret.mission_graph_aesthetic.max_depth = int(data[11])
        ret.mission_graph_aesthetic.min_depth = int(data[12])
        branch_probability = data[13][1:-1].split(":")
        ret.mission_graph_aesthetic.branch_probability[0] = float(branch_probability[0])
        ret.mission_graph_aesthetic.branch_probability[1] = float(branch_probability[1])
        ret.mission_graph_aesthetic.branch_probability[2] = float(branch_probability[2])
        ret.mission_graph_aesthetic.branch_probability[3] = float(branch_probability[3])
        ret.mission_graph_aesthetic.max_multi_lock_count = int(data[14])
        ret.mission_graph_aesthetic.max_locks_per_multi_lock = int(data[15])
        return ret

    def save(self):
        # Write file_data to file
        with open(self.file, 'w') as csvfile:
            csvfile.write(self.header + self.file_data)