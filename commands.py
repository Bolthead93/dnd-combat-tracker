import os
import pickle
import character
import save_data

class CommandInput:
    def __init__(self, user_input, characters):
        self.characters = characters
        self.command = None
        self.item = None
        self.items = None
        self.mod = None
        self.read(user_input)
        self.filter_characters()

    def filter_characters(self):
        if self.items is not None:
            filtered_characters = {name: char for name, char in self.characters.items() if name in self.items}
            self.characters = filtered_characters
        else:
            self.characters = None

    def read(self, command_input):
        """take an input and returns a tuple, the first item is a command,
        second is a list of items, third is a value"""
        commands_list = command_input.split(sep="/")
        self.command = commands_list[0]

        if len(commands_list) > 2:
            if len(commands_list[1]) > 0:
                self.items = commands_list[1].split(",")
            else:
                self.items = None
            if len(commands_list[2]) > 0:
                self.mod = commands_list[2]
            else:
                self.mod = None

        elif len(commands_list) == 2:
            if len(commands_list) > 0:
                self.items = commands_list[1].split(",")
            else:
                self.items = None
                self.mod = None

        if self.items is not None and len(self.items) == 1:
            self.item = self.items[0]
        else:
            self.item = None

    def has_items(self):
        if self.items is None:
            return False
        else:
            return True

    def has_mod(self):
        if self.mod is None:
            return False
        else:
            return True

    def has_characters(self):
        if self.characters is None:
            return False
        else:
            return True

    def has_item(self):
        if self.item is None:
            return False
        else:
            return True


# ----------------------- ACTIONS ---------------------------


class ActionAdd:
    def __init__(self):
        self.valid_commands = ["a", "action"]

    def execute(self, command):
        if command.has_characters():
            action = input("Enter the action: ")
            for char in command.characters.values():
                char.add_action(action)


class ActionOverwrite:
    def __init__(self):
        self.valid_commands = ["ao", "action"]

    def execute(self, command):
        if command.has_characters():
            action = input("Enter the action: ")
            for char in command.characters.values():
                char.actions = [action]


class ActionRemoveLast:
    def __init__(self):
        self.valid_commands = ["arl"]

    def execute(self, command):
        if command.has_characters():
            for char in command.characters.values():
                if len(char.actions) >= 1:
                    char.remove_action(-1)


class ActionRemoveFirst:
    def __init__(self):
        self.valid_commands = ["arf"]

    def execute(self, command):
        if command.has_characters():
            for char in command.characters.values():
                char.remove_action(0)


# ----------------------- BUFFS ---------------------------


class BuffAdd:
    def __init__(self):
        self.valid_commands = ["b", "buff"]

    def execute(self, command):
        if command.has_characters():
            buff_name = input("Buff name: ")
            duration = input("Duration: ")
            for char in command.characters.values():
                char.apply_buff(buff_name, duration)


class BuffRemove:
    def __init__(self):
        self.valid_commands = ["br"]

    def execute(self, command):
        if command.has_characters():
            buff_name = input("Buff name: ")
            for char in command.characters.values():
                char.remove_buff(buff_name)


class BuffRemoveAll:
    def __init__(self):
        self.valid_commands = ["bra"]

    def execute(self, command):
        if command.has_characters():
            for char in command.characters.values():
                char.remove_all_buffs()


# ----------------------- CONDITIONS ---------------------------


class CondAdd:
    def __init__(self):
        self.valid_commands = ["c", "cond", "condition"]

    def execute(self, command):
        if command.has_characters():
            cond_name = input("Condition name: ")
            duration = input("Duration: ")
            for char in command.characters.values():
                char.apply_condition(cond_name, duration)


class CondRemove:
    def __init__(self):
        self.valid_commands = ["cr"]

    def execute(self, command):
        if command.has_characters():
            cond_name = input("Condition name: ")
            for char in command.characters.values():
                char.remove_condition(cond_name)


class CondRemoveAll:
    def __init__(self):
        self.valid_commands = ["cra"]

    def execute(self, command):
        if command.has_characters():
            for char in command.characters.values():
                char.remove_all_conditions()


# ----------------------- HEALTH ---------------------------


class SetHealth:
    def __init__(self):
        self.valid_commands = ["h", "hp", "health", "damage", "heal"]

    def execute(self, command):
        if command.has_mod() and command.mod[-1].isnumeric():
            health_input = command.mod
        else:
            health_input = input("Set(#), increase(+#), or decrease(-#):")
        for char in command.characters.values():
            char.set_hp(health_input)


class SetMaxHealth:
    def __init__(self):
        self.valid_commands = ["hpm", "maxhp", "hpmax"]

    def execute(self, command):
        if command.has_mod() and command.mod[-1].isnumeric():
            hp_max = command.mod
        else:
            hp_max = input("Enter new max HP: ")
        for char in command.characters.values():
            char.set_max_hp(hp_max)


class SetTempHealth:
    def __init__(self):
        self.valid_commands = ["hpt", "temp", "temphp", "hptemp"]

    def execute(self, command):
        if command.has_mod() and command.mod[-1].isnumeric():
            temp_health = command.mod
        else:
            temp_health = input("Set temp health: ")
        for char in command.characters.values():
            char.temp_hp(temp_health)


# ----------------------- AC ---------------------------


class SetAC:
    def __init__(self):
        self.valid_commands = ["ac", "armour"]

    def execute(self, command):
        if command.has_mod() and command.mod[-1].is_numeric():
            ac = command.mod
        else:
            ac = input("Set AC: ")
        for char in command.characters.values():
            char.set_ac(ac)


# ----------------------- INITIATIVE / TOD ---------------------------


class SetInitiative:
    def __init__(self):
        self.valid_commands = ["i", "init"]

    def execute(self, command):
        if command.has_mod() and command.mod[-1].isnumeric():
            initiative = command.mod
        else:
            initiative = input("Set Initiative: ")
        for char in command.characters.values():
            char.initiative = initiative

class NextTurn:
    def __init__(self):
        self.valid_commands = ["t"]

    def execute(self, cm):
        cm.next_turn()

class PreviousTurn:
    def __init__(self):
        self.valid_commands = ["tr"]

    def execute(self, cm):
        cm.previous_turn()

class TimeForwards:
    def __init__(self):
        self.valid_commands = ["t"]

    def execute(self, pm):
        pm.time_forwards()

class TimeBackwards:
    def __init__(self):
        self.valid_commands = ["tr"]

    def execute(self, pm):
        pm.time_backwards()

class SetTOD:
    def __init__(self):
        self.valid_commands = ["tod"]

    def execute(self, command, pm):
        if command.has_items() and len(command.items) > 1:
            if command.items[0].isnumeric() and command.items[1].isnumeric():
                pm.set_tod(int(command.items[0]), int(command.items[1]))


# ----------------------- INVENTORY ---------------------------

class SetAmmo:
    def __init__(self):
        self.valid_commands = ["ammo"]

    def execute(self, command):
        ammo = ""
        if command.has_mod() and command.mod.isnumeric():
            ammo = command.mod
        for char in command.characters.values():
            char.set_ammo(ammo)


# ----------------------- REMOVE ---------------------------


class RemoveCharacter:
    def __init__(self):
        self.valid_commands = ["remove"]

    def execute(self, command, char_list):
        if command.has_characters():
            for name in command.characters.keys():
                del char_list[name]


# ----------------------- CREATION AND GROUPS ---------------------------


class AddPlayer:
    def __init__(self):
        self.valid_commands = ["np", "player"]

    def execute(self, command, char_list):
        if command.has_items():
            for name in command.items:
                char_list[name.strip()] = character.Character(name.title(), char_type="party")


class AddCreature:
    def __init__(self):
        self.valid_commands = ["nc", "creature"]

    def execute(self, command, char_list):
        if command.has_items() is not None:
            for name in command.items:
                char_list[name.strip()] = character.Character(name.title().strip(), char_type="creatures")


class AddCreatureGroup:
    def __init__(self):
        self.valid_commands = ["ncg", "creaturegroup"]

    def execute(self, command, char_list):
        if command.has_mod() and command.has_items():
            for x in range(int(command.mod)):
                char_name = f"{command.items[0].strip()}{x+1}"
                char_list[char_name] = character.Character(char_name.title(),
                                                               char_type="creatures", group_type=command.items[0])


class SetGroup:
    def __init__(self):
        self.valid_commands = ["group", "grp", "g"]

    def execute(self, command, char_input):
        if command.has_mod and command.has_items:
            if len(char_input) > 1:
                for char in char_input.values():
                    char.group = command.mod



class GetGroups:
    def __init__(self):
        self.valid_commands = ["group", "grp", "g"]

    def get_all_from_groups(self, command, char_list):
        temp_items = []
        temp_chars = {}
        for item in command.items:
            for char in char_list.values():
                if char.group.lower() == item.lower():
                    temp_chars[char.name.lower()] = char
                    temp_items.append(char.name.lower())
        return temp_items, temp_chars


class GetType:
    def __init__(self):
        self.valid_commands = ["party", "creatures"]

    def get_all_from_types(self, command, char_list):
        temp_chars = ({name: char for name, char in char_list.items() if char.type in command.items})
        temp_items = ([name for name, char in temp_chars.items() if char.type in command.items])
        return temp_items, temp_chars


# ----------------------- SAVING AND LOADING ---------------------------

class SaveParty:
    def __init__(self):
        self.valid_commands = ["sp", "saveparty"]

    def execute(self, party_data):
        file_name = input("Enter party name: ").lower()
        save_data.save_party(file_name, party_data)


class LoadParty:
    def __init__(self):
        self.valid_commands = ["lp", "loadparty"]

    def execute(self):
        os.system("cls")
        print(self.format_party_list(self.get_party_files()))
        file_name = input("\nEnter party to load: ").lower()
        if save_data.does_file_exists(f"P-{file_name}"):
            return save_data.load_party(file_name)

    def get_party_files(self):
        save_data.make_save_directory()
        file_list = os.listdir(save_data.get_save_directory())
        party_list = []
        if len(file_list) != 0:
            for file in file_list:
                if file[0:2] == "P-":
                    party_list.append(file[2:-4])
        if len(party_list) != 0:
            return True, party_list
        else:
            return False

    def format_party_list(self, party_list):
        nice_names = "Party files:\n\n"
        nice_names += str("\n").join(party_list[1])
        return nice_names


class ImportCreatures:
    def __init__(self):
        self.valid_commands = ["lc", "loadCreatures", "import"]

    def execute(self):
        print(self.format_combat_list(self.get_combat_files()))
        file_name = input("\nEnter encounter to import creatures from: ").lower()
        if save_data.does_file_exists(file_name):
            combat_data = save_data.load_file(file_name)
            character_dict = pickle.loads(combat_data.round_data[combat_data.highest_round])
            creature_dict = {name: creature for name, creature in character_dict.items() if creature.type == "creatures"}
            return creature_dict
        else:
            print("file not found")
            return None

    def get_combat_files(self):
        save_data.make_save_directory()
        file_list = os.listdir(save_data.get_save_directory())
        combat_list = []
        if len(file_list) != 0:
            for file in file_list:
                if not file[0:2] == "P-":
                    combat_list.append(file[0:-4])
        if len(combat_list) != 0:
            return True, combat_list
        else:
            return False

    def format_combat_list(self, combat_list):
        nice_names = "Combat files:\n\n"
        nice_names += str("\n").join(combat_list[1])
        return nice_names


class LoadCombatFile:
    def __init__(self):
        self.valid_commands = ["load"]

    def execute(self):
        print(self.format_combat_list(self.get_combat_files()))
        file_name = input("\nEnter encounter to load: ").lower()
        if save_data.does_file_exists(file_name):
            file_to_load = save_data.load_file(file_name)
            return file_to_load
        else:
            print("file not found")
            return None

    def get_combat_files(self):
        save_data.make_save_directory()
        file_list = os.listdir(save_data.get_save_directory())
        combat_list = []
        if len(file_list) != 0:
            for file in file_list:
                if not file[0:2] == "P-":
                    combat_list.append(file[0:-4])
        if len(combat_list) != 0:
            return True, combat_list
        else:
            return False

    def format_combat_list(self, combat_list):
        nice_names = "Combat files:\n\n"
        nice_names += str("\n").join(combat_list[1])
        return nice_names


class SaveCombatFile:
    def __init__(self):
        self.valid_commands = ["save"]

    def execute(self, save_data_file):
        file_name = input("Enter file name: ").lower()
        if save_data.does_file_exists(file_name):
            save_overwrite = input("Save file with this name exists, do you want to overwrite? Y/N ").lower()
            if save_overwrite == "y":
                save_data.save_file(file_name, save_data_file)
        else:
            save_data.save_file(file_name, save_data_file)


# ----------------------- ROUNDS ---------------------------

class NextRound:
    def __init__(self):
        self.valid_commands = ["r", "round"]

    def execute(self, combat_manager):
        combat_manager.next_round()


class UndoRound:
    def __init__(self):
        self.valid_commands = ["rr", "undo"]

    def execute(self, combat_manager):
        combat_manager.undo_round()


class RedoRound:
    def __init__(self):
        self.valid_commands = ["rf", "redo"]

    def execute(self, combat_manager):
        combat_manager.redo_round()


class EndCombat:
    def __init__(self):
        self.valid_commands = ["end", "exit"]

    def execute(self, combat_manager):
        combat_manager.push_data()
        save_data.save_file(combat_manager.name, combat_manager.combat_data)
