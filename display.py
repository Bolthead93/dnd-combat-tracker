import art
import os


class CombatLogger:

    def display_initiative(self, cm):
        init_size = len(cm.initiatives)
        if init_size > 0:
            current_char = list(cm.initiatives)[cm.turn]
            next_turns = list(cm.initiatives)[cm.turn+1:] + list(cm.initiatives)[0:cm.turn]
            next_turns = str(", ").join(next_turns)
            if cm.turn == 0:
                print("NEW ROUND!!!")
            else:
                print("Current turn:")
            init_output = (f"{cm.initiatives[current_char]}. {current_char} - Next turn: {next_turns}")
            if len(init_output) > 50:
                print(f"{init_output[0:49]}...")
            else:
                print(init_output)

    def display_notes(self, cm):
        if len(cm.notes) > 0:
            # print(art.create_banner("NOTES"))
            for n in cm.notes:
                note_index = cm.notes.index(n)
                print(f"{note_index + 1}. {str().join(n)}")

    def update(self, cm):
        os.system("cls")
        art.make_combat_title(cm.name)
        print(art.create_banner(f"--- ROUND {cm.round_number} / {cm.highest_round} ---"))

        self.display_notes(cm)
        self.display_initiative(cm)

        if len(cm.characters) > 0:
            print(art.create_banner("--- PLAYERS--- "))
        for c in cm.characters.values():
            if c.type == "party":

                print(f"{c.initiative}. {c.get_info()}")
                if c.check_finished_modifiers():
                    print(c.get_finished_modifiers())

        if len(cm.characters) > 0:

            print(art.create_banner("--- CREATURES ---"))
        for c in cm.characters.values():
            if c.type == "creatures":
                print(f"{c.initiative}. {c.get_info()}")
                if c.check_finished_modifiers():
                    print(c.get_finished_modifiers())


class PartyLogger:
    def display_tod(self, pm):
        if pm.tod_h >= 12:
            am_pm = "pm"
        else:
            am_pm = "am"
        print(f"Time of Day: {pm.tod_h:02d}:{pm.tod_m:02d} {am_pm}")


    def display_notes(self, pm):
        if len(pm.notes) > 0:
            print(art.create_banner("NOTES"))
            for n in pm.notes:
                note_index = pm.notes.index(n)
                print(f"{note_index + 1}. {str().join(n)}")

    def update(self, pm):
        os.system("cls")
        art.make_combat_title(pm.name)

        self.display_notes(pm)
        self.display_tod(pm)

        if len(pm.characters) > 0:
            print(art.create_banner("--- PLAYERS--- "))
        for c in pm.characters.values():
            if c.type == "party":
                print(f"{c.get_info().strip()}")
                if c.check_finished_modifiers():
                    print(c.get_finished_modifiers())

