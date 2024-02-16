import os
import pickle

class PartyDataFile:
    def __init__(self):
        self.characters = {}
        self.name = ""
        self.notes = []
        self.tod = 0.0


class CombatDataFile:
    def __init__(self):
        self.round_data = {}
        self.name = ""
        self.highest_round = 1
        self.notes = []



def get_save_directory():
    return f"{os.getcwd()}\\saved_files\\"


def make_save_directory():
    if not os.path.exists(get_save_directory()):
        os.makedirs(get_save_directory())


def does_file_exists(file_name):
    file_path = f"{get_save_directory()}{file_name}.pkl"
    return os.path.exists(file_path)


def save_file(file_name, data_file):
    """save out the provided data file"""
    make_save_directory()
    with open(f"{get_save_directory()}{file_name}.pkl", "wb") as f:
        pickle.dump(data_file, f)


def load_file(file_name):
    """find files by name and returns that file type, e.g. a combat file"""
    file_path = f"{get_save_directory()}{file_name}.pkl"
    with open(f"{file_path}", "rb") as f:
        data_file = pickle.load(f)
    return data_file


def save_party(file_name, characters):
    """take characters with the 'player' type and saves them to 'P-(file_name)'"""
    make_save_directory()
    temp_characters = {n: c for (n, c) in characters.items() if c.type == "party"}
    with open(f"{get_save_directory()}P-{file_name}.pkl", "wb") as f:
        pickle.dump(temp_characters, f)


def load_party(file_name, characters):
    """takes current characters and fills add characters with the 'player' type"""
    make_save_directory()
    with open(f"{get_save_directory()}P-{file_name}.pkl", "rb") as f:
        temp_characters = pickle.load(f)
    for name, char in temp_characters.items():
        if temp_characters[name].type == "party":
            characters[name] = char

