import save_data

class PartyManager:
    def __init__(self, party_file=None):
        self.name = ""
        self.notes = []
        self.characters = {}
        self.tod_h = 8
        self.tod_m = 0
        if party_file is not None:
            self.party_data = party_file
        else:
            self.party_data = save_data.PartyDataFile()

    def push_data(self):
        """normally done before saving"""
        self.party_data.characters = self.characters
        self.party_data.name = self.name
        self.party_data.notes = self.notes
        self.party_data.tod = (self.tod_h, self.tod_m)

    def pull_data(self):
        """for when loading files, combat data will be loaded in before, this just fills parameters"""
        self.name = self.party_data.name
        self.notes = self.party_data.notes
        self.characters = self.party_data.characters
        self.tod_h = self.party_data.tod[0]
        self.tod_m = self.party_data.tod[1]

    def remove_note(self, note_index):
        if len(self.notes) > note_index >= 0:
            print(self.notes[note_index])
            self.notes.remove(self.notes[note_index])

    def time_forwards(self):
        if self.tod_m + 15 == 60:
            self.tod_m = 0
            if self.tod_h + 1 == 24:
                self.tod_h = 0
            else:
                self.tod_h += 1
        else:
            self.tod_m += 15

    def time_backwards(self):
        if self.tod_m - 15 == -15:
            self.tod_m = 45
            if self.tod_h - 1 == -1:
                self.tod_h = 23
            else:
                self.tod_h -= 1
        else:
            self.tod_m -= 15

    def set_tod(self, hour, minute):
        self.tod_h = hour
        self.tod_m = minute

