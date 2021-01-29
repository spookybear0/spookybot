import os, json

path = os.path.dirname(os.path.realpath(__file__))

class JsonFile:
    def __init__(self, file_name: str):
        self.file = None
        self.file_name = file_name
        if os.path.exists(file_name):
            with open(file_name) as f:
                self.file = json.load(f)

    def get_file(self) -> dict:
        """Returns the loaded JSON file as a dict."""
        return self.file

    def write_file(self, new_content: dict) -> None:
        """Writes a new dict to the file."""
        with open(self.file_name, "w") as f:
            json.dump(new_content, f, indent=4)
        self.file = new_content

def dict_keys(dictioary: dict) -> tuple:
    """Returns a tuple of all the dictionary keys."""
    return tuple(dictioary.keys())

default_config = {
    "sql_server": "localhost",
    "sql_user": "root",
    "sql_db": "spookybot",
    "sql_password": "",
    "sql_port": 3308
}

user_config = {}

config_options = list(default_config.keys())


def load_config(location: str=path + "/../config.json"):
    config = JsonFile(location)
    user_config_temp = config.get_file()

    if user_config_temp is None:
        print("Generating new config")
        config.write_file(default_config)
        print("Generated new config! Please edit it and restart GDPyS.")
        raise SystemExit

    # Checks for default configuration updates.
    config_keys = list(user_config_temp.keys())
    updated_conf = False

    for def_conf_option in config_options:
        if def_conf_option not in config_keys:
            updated_conf = True
            user_config_temp[def_conf_option] = default_config[def_conf_option]

    if updated_conf:
        config.write_file(user_config_temp)
        print(
            "Your config has been updated! Please change the new vaulues to your liking."
        )
        raise SystemExit

    for key in dict_keys(user_config_temp):
        user_config[key] = user_config_temp[key]