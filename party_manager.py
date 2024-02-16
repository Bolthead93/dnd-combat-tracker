import save_data

class PartyManager:
    def __init__(self, party_file=None):
        self.name = ""
        self.notes = []
        self.characters = {}
        if party_file is not None:
            self.party_data = party_file
        else:
            self.party_data = save_data.PartyDataFile()

    def push_data(self):
        """normally done before saving"""
        self.party_data.characters = self.characters
        self.party_data.name = self.name
        self.party_data.notes = self.notes

    def pull_data(self):
        """for when loading files, combat data will be loaded in before, this just fills parameters"""
        self.name = self.party_data.name
        self.notes = self.party_data.notes
        self.characters = self.party_data.characters

    def remove_note(self, note_index):
        if len(self.notes) > note_index >= 0:
            print(self.notes[note_index])
            self.notes.remove(self.notes[note_index])

