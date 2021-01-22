# simple class for turning a dict into class properties

class Classify:
    def __init__(self, keys: dict):
        for key in keys:
            setattr(self, str(key), keys[key])
            
    def get(self, key: str):
        return vars(self)[key]
    
    def declassify(self):
        return vars(self)