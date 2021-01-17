
# simple class for turning a dict into a class

class Classify:
    def __init__(self, keys: dict):
        for key in keys:
            print(key, keys[key])
            setattr(self, str(key), keys[key])