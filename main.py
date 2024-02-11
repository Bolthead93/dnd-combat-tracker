import copy

import character
import modifiers
import os
import art
import pickle
import save_data

characters = {}
notes = []
hide_hints = True
round_number = 1
highest_round = 1
encounter_name = ""
save_data_file = save_data.SaveFile()


def display_help():
    print(art.create_banner("HELP"))
    print(art.text_help)


def get_file_name():
    return f"{encounter_name}-{round_number}"


def display_notes():
    if len(notes) > 0:
        print(art.create_banner("NOTES"))
        for n in notes:
            note_index = notes.index(n)
            print(f"{note_index + 1}. {str().join(n)}")
        print("\n")


def remove_note(note_index):
    if len(notes) > note_index >= 0:
        notes.remove(notes[note_index])


def update_display():
    os.system("cls")
    art.make_combat_title(encounter_name)
    print(art.create_banner(f"--- ROUND {round_number} / {highest_round} ---"))

    display_notes()

    if len(characters) > 0:
        print(art.create_banner("--- PLAYERS--- "))
    for char in characters:
        if characters[char].type == "player":
            print(characters[char].get_info())
            if characters[char].check_finished_modifiers():
                print(characters[char].get_finished_modifiers())

    if len(characters) > 0:
        print("\n")
        print(art.create_banner("--- CREATURES ---"))
    for char in characters:
        if characters[char].type == "creature":
            print(characters[char].get_info())
            if characters[char].check_finished_modifiers():
                print(characters[char].get_finished_modifiers())


def load_file(file):
    global characters
    global notes
    global round_number
    global highest_round
    global encounter_name
    global save_data_file
    save_data_file = file
    encounter_name = file.encounter_name
    highest_round = file.highest_round
    characters = file.round_data[file.highest_round].characters
    round_number = file.highest_round
    notes = file.notes


def save_file(file):
    file = save_data_file
    file.round_data[round_number] = save_data.RoundData(round_number, characters)
    file.encounter_name = encounter_name
    file.highest_round = highest_round
    file.notes = notes


def write_to_file():
    # with open(f"{encounter_name}.txt", "a") as text_file:
    #     text_file.write("\n\n")
    #     text_file.write((art.create_banner(f"{encounter_name.upper()} - ROUND {round_number}")))
    #     text_file.write("\n")
    #     if len(notes) > 0:
    #         text_file.write(art.create_banner("NOTES"))
    #         text_file.write("\n")
    #         for n in notes:
    #             note_index = notes.index(n)
    #             text_file.write(f"{note_index + 1}. {str().join(n)}")
    #         text_file.write("\n")
    #     if len(characters) > 0:
    #         text_file.write(art.create_banner("PLAYERS"))
    #         text_file.write("\n")
    #     for char in characters:
    #         if characters[char].type == "player":
    #             text_file.write(characters[char].get_info())
    #             text_file.write("\n")
    #     text_file.write(art.create_banner("CREATURES"))
    #     text_file.write("\n")
    #     for char in characters:
    #         if characters[char].type == "creature":
    #             text_file.write(characters[char].get_info())
    #             text_file.write("\n")
    return


def get_command(command_input):
    """returns a list which includes the command, and then a list of items to modify"""
    commands_list = command_input.split(sep=",")
    return commands_list[0]


def get_command_items(command_input):
    """return a list of items to perform the command on"""
    commands_list = command_input.split(sep=",")
    if len(commands_list) > 1:
        items_in_list = [com.strip() for com in commands_list[1:]]
        return items_in_list
    else:
        return []


def save_load_party(command_input):
    directory = f"{os.getcwd()}\\saved_files\\"
    if not os.path.exists(directory):
        os.makedirs(directory)

    if command_input == "sp":
        party_name = input("Enter party name: ").lower()
        temp_characters = {}
        for char in characters:
            if characters[char].type == "player":
                temp_characters[char] = characters[char]
        with open(f"{directory}P-{party_name}.pkl", "wb") as f:
            pickle.dump(temp_characters, f)

    elif command_input == "lp":
        party_name = input("Enter party name to load: ").lower()
        with open(f"{directory}P-{party_name}.pkl", "rb") as f:
            temp_characters = pickle.load(f)
        for char in temp_characters:
            if temp_characters[char].type == "player":
                characters[char] = temp_characters[char]


def get_valid_character_list(item_list):
    valid_list = []
    for char in item_list:
        if char in characters:
            valid_list.append(char)
    return valid_list


def edit_characters(command_input, item_input):
    character_list = get_valid_character_list(item_input)
    if len(character_list) == 0:
        print("skipped")
        return
    if command_input in ["a", "ao", "arf", "arl"]:
        action_name = input("Enter the action: ")
        for char in character_list:
            char_to_edit = char
            if "a" == command_input:
                characters[char_to_edit].add_action(action_name)
            elif "ao" == command_input:
                characters[char_to_edit].actions = [action_name]
            elif "arf" == command_input:
                characters[char_to_edit].remove_action(0)
            elif "arl" == command_input:
                characters[char_to_edit].remove_action(-1)
    elif command_input in ["b", "br", "bra"]:
        buff_duration = 0
        if "b" == command_input:
            buff_name = input("Buff name: ").lower()
            buff_duration = input("Buff duration: ")
        elif "br" == command_input:
            buff_name = input("Buff name: ").lower()
        for char in character_list:
            char_to_edit = char
            if "b" == command_input:
                new_buff = modifiers.Modifier(buff_name, buff_duration)
                characters[char_to_edit].apply_buff(new_buff)
            elif "br" == command_input:
                characters[char_to_edit].remove_buff(buff_name)
            elif "bra" == command_input:
                characters[char_to_edit].remove_all_buffs()
    elif command_input in ["c", "cr", "cra"]:
        cond_duration = 0
        if "c" == command_input:
            condition = input("Condition name: ").lower()
            cond_duration = input("Condition duration: ")
        elif "cr" == command_input:
            condition = input("Condition name: ").lower()
        for char in character_list:
            char_to_edit = char
            if "c" == command_input:
                new_cond = modifiers.Modifier(condition, cond_duration)
                characters[char_to_edit].apply_condition(new_cond)
            elif "cr" == command_input:
                characters[char_to_edit].remove_condition(condition)
            elif "cra" == command_input:
                characters[char_to_edit].remove_all_conditions()
    elif command in ["hp", "hpt", "hpm"]:
        if "hp" == command_input:
            health_input = input("Set(#), increase(+#), or decrease(-#):")
            for char in character_list:
                characters[char].set_hp(health_input)
        elif "hpt" == command_input:
            temp_health = input("Set temp health: (hp decrease will deduct from this first) ")
            for char in character_list:
                characters[char].set_temp_hp(temp_health)
        elif "hpm" == command:
            hp_max = input("Enter new max HP: ")
            for char in character_list:
                characters[char].set_max_hp(hp_max)
    elif "ac" == command:
        ac_input = input("Enter AC: ")
        for char in character_list:
            characters[char].set_ac(ac_input)
    elif "remove" == command_input:
        for char in character_list:
            if char in characters:
                del characters[char]


def group_characters(items_input):
    if len(items_input) > 1:
        group_name = items_input[0]
        things_to_group = items_input[1:]
        for char in things_to_group:
            characters[char].group = group_name.lower()


def get_all_of_type(items_input):
    temp_list = []
    if "party" in items_input:
        for char in characters:
            if characters[char].type == "player":
                temp_list.append(char)
    if "creatures" in items_input:
        for char in characters:
            if characters[char].type == "creature":
                temp_list.append(char)
    if "group" in items_input:
        groups_to_edit = items_input[1:]
        for group in groups_to_edit:
            for char in characters:
                if characters[char].group.lower() == group.lower():
                    temp_list.append(char)
    return temp_list


# initial screen to display
waiting_for_input = True
file_found = True
while waiting_for_input:
    os.system("cls")
    print(art.logo)
    print(art.info)
    if not file_found:
        print("\nFile note found")
    start_command = input("\nEnter an encounter name, or type 'load' to open a file: ").lower()
    if start_command == "load":
        file_name = input("Enter file name: ").lower()
        if save_data.does_file_exists(file_name):
            file_to_load = save_data.load_file(file_name)
            load_file(file_to_load)
            waiting_for_input = False
        else:
            file_found = False
    else:
        save_data_file.encounter_name = start_command
        encounter_name = save_data_file.encounter_name
        waiting_for_input = False



# the trackers main loop
in_combat = True
while in_combat:

    update_display()
    if not hide_hints:
        hide_hints = True
        display_help()

    # take user input
    user_input = input("\nWhat do you want to do? ").lower()
    command = get_command(user_input)
    items = get_command_items(user_input)

    # check for these inputs as secondary commands
    if "party" in items or "creatures" in items or "group" in items:
        items = get_all_of_type(items)

    # create a new player or players from the items in the list
    if "np" == command:
        for item in items:
            name = item.lower()
            characters[name] = character.Character(name.title(), char_type="player")
    # create a new creature or creatures from the items in the list
    elif "nc" == command:
        for item in items:
            name = item.lower()
            characters[name] = character.Character(name.title(), char_type="creature")

    elif "ncg" == command:
        if len(items) == 2 and items[1].isnumeric():
            for x in range(int(items[1])):
                creature_name = items[0] + str(x + 1)
                characters[creature_name] = character.Character(creature_name.title(),
                                                                char_type="creature", group_type=items[0])
        else:
            print("invalid command")

    elif "group" == command:
        group_characters(items)

    # if the command is to edit characters
    elif command in ("a", "ao", "arl", "arf", "b", "br", "bra", "c", "cr", "cra", "hp", "hpt", "hpm", "ac", "remove"):
        edit_characters(command, items)

    # save or load the player party
    elif command in ["sp", "lp"]:
        save_load_party(command)

    # count the next round and change the stats
    elif "n" == command:
        round_characters = {}
        for each_char in characters:
            new_char = copy.deepcopy(characters[each_char])
            round_characters[each_char] = new_char
        save_data_file.round_data[round_number] = save_data.RoundData(round_number, round_characters)
        round_number += 1
        save_file(save_data_file)
        highest_round = round_number
        for char in characters:
            characters[char].count_round()

    elif "rf" == command:
        if round_number + 1 <= highest_round:
            round_number += 1
            characters = save_data_file.round_data[round_number].characters

    elif "rr" == command:
        save_data_file.round_data[round_number] = save_data.RoundData(round_number, characters)
        if round_number > 1:
            round_number -= 1
            characters = save_data_file.round_data[round_number].characters

    elif "load" == command:
        file_name = input("Enter file name: ").lower()
        if save_data.does_file_exists(file_name):
            file_to_load = save_data.load_file(file_name)
            load_file(file_to_load)

    elif "save" == command:
        sf_name = input("Enter a file name: ").lower()
        save_file(save_data_file)
        save_data.save_file(sf_name, save_data_file)

    elif "end" == command:
        sf_name = encounter_name.lower()
        save_file(save_data_file)
        save_data.save_file(sf_name, save_data_file)
        in_combat = False

    elif "help" in command:
        hide_hints = False

    elif command.isnumeric():
        remove_note(int(command) - 1)
    else:
        notes.append(user_input)
