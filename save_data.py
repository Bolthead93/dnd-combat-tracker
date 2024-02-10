import os
import pickle


class SaveFile:

    def __init__(self):
        self.round_data = {}
        self.encounter_name = ""
        self.highest_round = 1
        self.notes = []


class RoundData:

    def __init__(self, round_number=1, characters={}):
        self.round = round_number
        self.characters = characters


def save_file(file_name, data_file):
    save_path = f"{os.getcwd()}\\saved_files\\"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    with open(f"{save_path}\\{file_name}.pkl", "wb") as f:
        pickle.dump(data_file, f)


def does_file_exists(file_name):
    file_path = f"{os.getcwd()}\\saved_files\\{file_name}.pkl"
    return os.path.exists(file_path)


def load_file(file_name):
    file_path = f"{os.getcwd()}\\saved_files\\{file_name}.pkl"
    with open(f"{file_path}", "rb") as f:
        data_file = pickle.load(f)
    return data_file
