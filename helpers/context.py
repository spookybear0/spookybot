

class Context: # simple context class
    def __init__(self, keys: dict):
        for key in keys:
            setattr(self, str(key), keys[key])