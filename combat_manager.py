import save_data
import pickle

class CombatManager:
    def __init__(self, combat_file=None):
        self.name = ""
        self.initiatives = {}
        self.notes = []
        self.round_data = {}
        self.round_number = 1
        self.highest_round = 1
        self.characters = {}
        self.turn = 0
        if combat_file is not None:
            self.combat_data = combat_file
        else:
            self.combat_data = save_data.CombatDataFile()


    def set_initiative(self):
        for char in self.characters.values():
            char.initiative = input(f"Initiative for {char.name}: ")
        self.sort_initiative()

    def sort_initiative(self):
        init_dict = {name.title(): char.initiative for name, char in self.characters.items()}
        self.initiatives = dict(sorted(init_dict.items(), key=lambda item: int(item[1]), reverse=True))

    def next_turn(self):
        init_size = len(self.initiatives)
        if self.turn + 1 > init_size - 1:
            self.turn = 0
        else:
            self.turn += 1

    def previous_turn(self):
        init_size = len(self.initiatives)
        if self.turn - 1 < 0:
            self.turn = init_size - 1
        else:
            self.turn -= 1

    def dump_round_characters(self):
        self.round_data[self.round_number] = pickle.dumps(self.characters)

    def load_round_characters(self):
        self.characters = pickle.loads(self.round_data[self.round_number])

    def next_round(self):
        self.dump_round_characters()
        self.round_number += 1
        self.highest_round = self.round_number
        self.turn = 0
        for char in self.characters.values():
            char.count_round()

    def undo_round(self):
        self.dump_round_characters()
        if self.round_number > 1:
            self.round_number -= 1
            self.load_round_characters()

    def redo_round(self):
        if self.round_number + 1 <= self.highest_round:
            self.round_number += 1
            self.load_round_characters()

    def push_data(self):
        """normally done before saving"""
        self.dump_round_characters()
        self.combat_data.round_data = self.round_data
        self.combat_data.highest_round = self.highest_round
        self.combat_data.name = self.name
        self.combat_data.notes = self.notes

    def pull_data(self):
        """for when loading files, combat data will be loaded in before, this just fills parameters"""
        self.name = self.combat_data.name
        self.notes = self.combat_data.notes
        self.round_data = self.combat_data.round_data
        self.round_number = self.combat_data.highest_round
        self.highest_round = self.combat_data.highest_round
        self.load_round_characters()

    def remove_note(self, note_index):
        if len(self.notes) > note_index >= 0:
            print(self.notes[note_index])
            self.notes.remove(self.notes[note_index])

