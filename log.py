class Log:
    verbose = False
    @staticmethod
    def print(string):
        if Log.verbose:
            print(string)