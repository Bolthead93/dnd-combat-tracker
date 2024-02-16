import character
import save_data
import copy

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


    def check_has_item(self):
        if len(self.items) == 1:
            self.item = self.items[0]
            return True
        else:
            return False

    def read(self, command_input):
        """take an input and returns a tuple, the first item is a command,
        second is a list of items, third is a value"""
        commands_list = command_input.split(sep="/")
        self.command = commands_list[0]

        if len(commands_list) > 2:
            self.items = commands_list[1].split(",")
            self.mod = commands_list[2]

        elif len(commands_list) == 2:
            self.items = commands_list[1].split(",")
            self.mod = None


# ----------------------- ACTIONS ---------------------------


class ActionAdd:
    def __init__(self):
        self.valid_commands = ["a", "action"]

    def execute(self, characters):
        action = input("Enter the action: ")
        for char in characters.values():
            char.add_action(action)


class ActionOverwrite:
    def __init__(self):
        self.valid_commands = ["ao", "action"]

    def execute(self, characters):
        action = input("Enter the action: ")
        for char in characters.values():
            char.actions = [action]


class ActionRemoveLast:
    def __init__(self):
        self.valid_commands = ["arl"]

    def execute(self, characters):
        for char in characters.values():
            if len(char.actions) >= 1:
                char.remove_action(-1)


class ActionRemoveFirst:
    def __init__(self):
        self.valid_commands = ["arf"]

    def execute(self, characters):
        for char in characters.values():
            char.remove_action(0)


# ----------------------- BUFFS ---------------------------


class BuffAdd:
    def __init__(self):
        self.valid_commands = ["b", "buff"]

    def execute(self, characters):
        buff_name = input("Buff name: ")
        duration = input("Duration: ")
        for char in characters.values():
            char.apply_buff(buff_name, duration)


class BuffRemove:
    def __init__(self):
        self.valid_commands = ["br"]

    def execute(self, characters):
        buff_name = input("Buff name: ")
        for char in characters.values():
            char.remove_buff(buff_name)


class BuffRemoveAll:
    def __init__(self):
        self.valid_commands = ["bra"]

    def execute(self, characters):
        for char in characters.values():
            char.remove_all_buffs()


# ----------------------- CONDITIONS ---------------------------


class CondAdd:
    def __init__(self):
        self.valid_commands = ["c", "cond", "condition"]

    def execute(self, characters):
        cond_name = input("Condition name: ")
        duration = input("Duration: ")
        for char in characters.values():
            char.apply_condition(cond_name, duration)


class CondRemove:
    def __init__(self):
        self.valid_commands = ["cr"]

    def execute(self, characters):
        cond_name = input("Condition name: ")
        for char in characters.values():
            char.remove_condition(cond_name)


class CondRemoveAll:
    def __init__(self):
        self.valid_commands = ["cra"]

    def execute(self, characters):
        for char in characters.values():
            char.remove_all_conditions()


# ----------------------- HEALTH ---------------------------


class SetHealth:
    def __init__(self):
        self.valid_commands = ["h", "hp", "health", "damage", "heal"]

    def execute(self, characters, mod):
        if (mod is None) or not (mod[-1].isnumeric()):
            health_input = input("Set(#), increase(+#), or decrease(-#):")
        else:
            health_input = mod
        for char in characters.values():
            char.set_hp(health_input)


class SetMaxHealth:
    def __init__(self):
        self.valid_commands = ["hpm", "maxhp", "hpmax"]

    def execute(self, characters, mod):
        if (mod is None) or not (mod[-1].isnumeric()):
            hp_max = input("Enter new max HP: ")
        else:
            hp_max = mod
        for char in characters.values():
            char.set_max_hp(hp_max)


class SetTempHealth:
    def __init__(self):
        self.valid_commands = ["hpt", "temp", "temphp", "hptemp"]

    def execute(self, characters, mod):
        if (mod is None) or not (mod[-1].isnumeric()):
            temp_health = input("Set temp health: ")
        else:
            temp_health = mod
        for char in characters.values():
            char.temp_hp(temp_health)


# ----------------------- AC ---------------------------


class SetAC:
    def __init__(self):
        self.valid_commands = ["ac", "armour"]

    def execute(self, characters, mod):
        if (mod is None) or not (mod[-1].isnumeric()):
            ac = input("Set AC: ")
        else:
            ac = mod
        for char in characters.values():
            char.set_ac(ac)


# ----------------------- INITIATIVE ---------------------------


class SetInitiative:
    def __init__(self):
        self.valid_commands = ["i", "init"]

    def execute(self, characters, mod):
        if (mod is None) or not (mod[-1].isnumeric()):
            initiative = input("Set Initiative: ")
        else:
            initiative = mod
        for char in characters.values():
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


# ----------------------- INVENTORY ---------------------------

class SetAmmo:
    def __init__(self):
        self.valid_commands = ["ammo"]

    def execute(self, characters, mod):
        ammo = ""
        if mod is not None:
            if mod.isnumeric():
                ammo = mod
        for char in characters.values():
            char.set_ammo(ammo)


# ----------------------- REMOVE ---------------------------


class RemoveCharacter:
    def __init__(self):
        self.valid_commands = ["remove"]

    def execute(self, characters_list={}, characters_input={}):
        for name in characters_input.keys():
            del characters_list[name]



# ----------------------- CREATION AND GROUPS ---------------------------


class AddPlayer:
    def __init__(self):
        self.valid_commands = ["np", "player"]

    def execute(self, to_add, char_list):
        if to_add is not None:
            for name in to_add:
                char_list[name.strip()] = character.Character(name.title(), char_type="party")


class AddCreature:
    def __init__(self):
        self.valid_commands = ["nc", "creature"]

    def execute(self, to_add, char_list):
        if to_add is not None:
            for name in to_add:
                char_list[name.strip()] = character.Character(name.title().strip(), char_type="creature")


class AddCreatureGroup:
    def __init__(self):
        self.valid_commands = ["ncg", "creaturegroup"]

    def execute(self, name, char_list, amount):
        if amount is not None and char_list is not None:
            for x in range(int(amount)):
                char_name = f"{name[0]}{x+1}"
                char_list[char_name] = character.Character(char_name.title(),
                                                               char_type="creature", group_type=name[0])


class SetGroup:
    def __init__(self):
        self.valid_commands = ["group", "grp", "g"]

    def execute(self, name, char_input):
        if len(char_input) > 1:
            for char in char_input.values():
                char.group = name



class GetGroups:
    def __init__(self):
        self.valid_commands = ["group", "grp", "g"]

    def get_all_from_groups(self, char_list, items):
        temp_items = []
        temp_chars = {}
        for item in items:
            for char in char_list.values():
                if char.group.lower() == item.lower():
                    temp_chars[char.name.lower()] = char
                    temp_items.append(char.name.lower())
        return temp_items, temp_chars


class GetType:
    def __init__(self):
        self.valid_commands = ["party", "creatures"]

    def get_all_from_types(self, char_list, items):
        temp_chars = ({name: char for name, char in char_list.items() if char.type in items})
        temp_items = ([name for name, char in temp_chars.items() if char.type in items])
        return temp_items, temp_chars


# ----------------------- SAVING AND LOADING ---------------------------

class SaveParty:
    def __init__(self):
        self.valid_commands = ["sp", "saveparty"]

    def execute(self, file_input=None, characters={}):
        if file_input is not None:
            file_name = file_input.lower()
        else:
            file_name = input("Enter party name: ").lower()
        save_data.save_party(file_name, characters)


class LoadParty:
    def __init__(self):
        self.valid_commands = ["lp", "loadparty"]

    def execute(self, file_input=None, characters={}):
        if file_input is not None:
            file_name = file_input.lower()
        else:
            file_name = input("Enter party name: ").lower()
        save_data.load_party(file_name,characters)


class LoadCombatFile:
    def __init__(self):
        self.valid_commands = ["load"]

    def execute(self, file_input=None):
        if file_input is None:
            file_name = input("Enter file name: ").lower()
        else:
            file_name = file_input
        if save_data.does_file_exists(file_name):
            file_to_load = save_data.load_file(file_name)
            return file_to_load
        else:
            print("file not found")
            return None


class SaveCombatFile:
    def __init__(self):
        self.valid_commands = ["save"]

    def execute(self, file_input, save_data_file):
        if file_input is None:
            file_name = input("Enter file name: ").lower()
        else:
            file_name = file_input
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





