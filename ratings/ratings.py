import csv

class Ratings():
    def __init__(self, file):
        # Open the csv file
        self.file = file
        self.file_data = ''

        open(file, 'a').close() # Create a file if it doesn't exist.

        with open(file, 'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            for i, row in enumerate(csv_reader):
                if i == 0:
                    continue
                self.file_data += ','.join(row) + "\n"

    def add_level(self, seed):
        self.file_data += "{},0,0\n".format(seed)
    
    def level_count(self):
        return len(self.file_data.splitlines())
    
    def add_rating(self, name, seed, rating):
        new_file_data = ""
        for row in self.file_data.splitlines():
            data = row.split(",")
            if data[0] == 'seed':
                continue

            b_rating = data[1]
            r_rating = data[2]
            if int(data[0]) == int(seed):
                if name == "brandon":
                    b_rating = rating
                else:
                    r_rating = rating
            
            new_file_data  += "{},{},{}\n".format(data[0], b_rating, r_rating)
        
        self.file_data = new_file_data

    def level_seed(self, i):
        return int(self.file_data.splitlines()[i].split(",")[0])

    def save(self):
        # Write file_data to file
        header = "seed,brandon_rating,ryan_rating\n"
        with open(self.file, 'a') as csvfile:
            csvfile.write(header + self.file_data)