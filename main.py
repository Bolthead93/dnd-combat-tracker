import commands
import art
import display
import party_manager
import save_data
import combat_manager
import os
import copy

party_name = ""
characters_list = {}
notes = []


def display_help():
    print(art.create_banner("HELP"))
    print(art.text_help)


def party_mode():
    # set up the party manager
    party = party_manager.PartyManager()
    party.characters = characters_list
    party.name = party_name
    party.notes = notes
    # save the party file once initialised
    save_data.save_party(f"{party.name}", party.party_data)

    party_display = display.PartyLogger()
    hide_help = True

    in_party = True
    while in_party:

        party.push_data()
        save_data.save_party(party.name, party.party_data)
        party_display.update(party)

        if not hide_help:
            display_help()
            hide_help = True

        # take user input
        user_input = input("\nWhat do you want to do? ").lower()
        command = commands.CommandInput(user_input, party.characters)

        # Check for group or type and alter command.items to match
        if command.items is not None:
            if "party" in command.items or "creatures" in command.items:
                command.items, command.characters = (commands.GetType().
                                                     get_all_from_types(party.characters, command.items))
            if command.mod in commands.GetGroups().valid_commands:
                command.items, command.characters = (commands.GetGroups().
                                                     get_all_from_groups(party.characters, command.items))

        # Group
        if command.command in commands.SetGroup().valid_commands:
            commands.SetGroup().execute(command.mod, command.characters)

        if user_input == "combat":
            party.characters = combat_mode(party.characters)

        # Creation
        elif command.command in commands.AddPlayer().valid_commands:
            commands.AddPlayer().execute(command.items, party.characters)

        # Actions
        elif command.command in commands.ActionAdd().valid_commands:
            commands.ActionAdd().execute(command.characters)
        elif command.command in commands.ActionOverwrite().valid_commands:
            commands.ActionOverwrite().execute(command.characters)
        elif command.command in commands.ActionRemoveFirst().valid_commands:
            commands.ActionRemoveFirst().execute(command.characters)
        elif command.command in commands.ActionRemoveLast().valid_commands:
            commands.ActionRemoveLast().execute(command.characters)

        # Buffs
        elif command.command in commands.BuffAdd().valid_commands:
            commands.BuffAdd().execute(command.characters)
        elif command.command in commands.BuffRemove().valid_commands:
            commands.BuffRemove().execute(command.characters)
        elif command.command in commands.BuffRemoveAll().valid_commands:
            commands.BuffRemoveAll().execute(command.characters)

        # Conditions
        elif command.command in commands.CondAdd().valid_commands:
            commands.CondAdd().execute(command.characters)
        elif command.command in commands.CondRemove().valid_commands:
            commands.CondRemove().execute(command.characters)
        elif command.command in commands.CondRemoveAll().valid_commands:
            commands.CondRemoveAll().execute(command.characters)

        # Health
        elif command.command in commands.SetHealth().valid_commands:
            commands.SetHealth().execute(command.characters, command.mod)
        elif command.command in commands.SetMaxHealth().valid_commands:
            commands.SetMaxHealth().execute(command.characters, command.mod)
        elif command.command in commands.SetTempHealth().valid_commands:
            commands.SetTempHealth().execute(command.characters, command.mod)

        # AC
        elif command.command in commands.SetAC().valid_commands:
            commands.SetAC().execute(command.characters, command.mod)

        # Inventory
        elif command.command in commands.SetAmmo().valid_commands:
            commands.SetAmmo().execute(command.characters, command.mod)

        # Remove
        elif command.command in commands.RemoveCharacter().valid_commands:
            commands.RemoveCharacter().execute(party.characters, command.characters)

        # Save and Load
        elif command.command in commands.SaveParty().valid_commands:
            commands.SaveParty().execute(command.mod, party.characters)
        elif command.command in commands.LoadParty().valid_commands:
            commands.LoadParty().execute(command.mod, party.characters)

        elif "help" == command.command:
            print("should unhide")
            hide_help = False

        elif command.command.isnumeric():
            party.remove_note(int(command.command) - 1)
        elif command.items is None and command.mod is None:
            party.notes.append(command.command)


def combat_mode(characters):

    # set up the combat manager
    combat = combat_manager.CombatManager()
    combat.characters.update(characters)
    # load in existing encounter or create a new one
    player_input = input("Enter an encounter name or type 'load': ").lower()
    if player_input in commands.LoadCombatFile().valid_commands:
        player_input = input("Enter encounter name: ")
        if save_data.does_file_exists(player_input):
            combat.name = player_input
            combat.combat_data = commands.LoadCombatFile().execute(player_input)
            combat.pull_data()
        else:
            print("file not found")
            return(characters)
    else:
        combat.name = player_input
    # update the display
    combat_display = display.CombatLogger()

    hide_help = True
    command = commands.CommandInput("", "")
    in_combat = True

    while in_combat:
        combat.sort_initiative()
        combat.push_data()
        save_data.save_file(combat.name, combat.combat_data)
        combat_display.update(combat)


        # show hints if the command was to un-hide
        if not hide_help:
            hide_help = True
            display_help()

        # for deving and checking what command is outputting
        # if len(command.command) != None:
        #     print(f"last command: {command.command, command.items, command.characters, command.mod}")

        # take user input
        user_input = input("\nWhat do you want to do? ").lower()
        command = commands.CommandInput(user_input, combat.characters)

        # Check for group or type and alter command.items to match
        if command.items is not None:
            if "party" in command.items or "creatures" in command.items:
                command.items, command.characters = (commands.GetType()
                                                     .get_all_from_types(combat.characters, command.items))
            if command.mod in commands.GetGroups().valid_commands:
                command.items, command.characters = (commands.GetGroups()
                                                     .get_all_from_groups(combat.characters, command.items))

        # Group
        if command.command in commands.SetGroup().valid_commands:
            commands.SetGroup().execute(command.mod, command.characters)

        # Creation
        if command.command in commands.AddPlayer().valid_commands:
            commands.AddPlayer().execute(command.items, combat.characters)
        elif command.command in commands.AddCreature().valid_commands:
            commands.AddCreature().execute(command.items, combat.characters)
        elif command.command in commands.AddCreatureGroup().valid_commands:
            commands.AddCreatureGroup().execute(command.items, combat.characters, command.mod)

        # Actions
        elif command.command in commands.ActionAdd().valid_commands:
            commands.ActionAdd().execute(command.characters)
        elif command.command in commands.ActionOverwrite().valid_commands:
            commands.ActionOverwrite().execute(command.characters)
        elif command.command in commands.ActionRemoveFirst().valid_commands:
            commands.ActionRemoveFirst().execute(command.characters)
        elif command.command in commands.ActionRemoveLast().valid_commands:
            commands.ActionRemoveLast().execute(command.characters)

        # Buffs
        elif command.command in commands.BuffAdd().valid_commands:
            commands.BuffAdd().execute(command.characters)
        elif command.command in commands.BuffRemove().valid_commands:
            commands.BuffRemove().execute(command.characters)
        elif command.command in commands.BuffRemoveAll().valid_commands:
            commands.BuffRemoveAll().execute(command.characters)

        # Conditions
        elif command.command in commands.CondAdd().valid_commands:
            commands.CondAdd().execute(command.characters)
        elif command.command in commands.CondRemove().valid_commands:
            commands.CondRemove().execute(command.characters)
        elif command.command in commands.CondRemoveAll().valid_commands:
            commands.CondRemoveAll().execute(command.characters)

        # Health
        elif command.command in commands.SetHealth().valid_commands:
            commands.SetHealth().execute(command.characters, command.mod)
        elif command.command in commands.SetMaxHealth().valid_commands:
            commands.SetMaxHealth().execute(command.characters, command.mod)
        elif command.command in commands.SetTempHealth().valid_commands:
            commands.SetTempHealth().execute(command.characters, command.mod)

        # AC
        elif command.command in commands.SetAC().valid_commands:
            commands.SetAC().execute(command.characters, command.mod)

        # Inventory
        elif command.command in commands.SetAmmo().valid_commands:
            commands.SetAmmo().execute(command.characters, command.mod)

        # Initiative
        elif command.command in commands.SetInitiative().valid_commands:
            commands.SetInitiative().execute(command.characters, command.mod)
        elif command.command == "setinit":
            combat.set_initiative()
            combat.turn = 0
            combat.sort_initiative()

        # Remove
        elif command.command in commands.RemoveCharacter().valid_commands:
            commands.RemoveCharacter().execute(combat.characters, command.characters)

        # Save and Load
        elif command.command in commands.SaveParty().valid_commands:
            commands.SaveParty().execute(command.mod, combat.characters)
        elif command.command in commands.LoadParty().valid_commands:
            commands.LoadParty().execute(command.mod, combat.characters)

        elif command.command in commands.SaveCombatFile().valid_commands:
            combat.push_data()
            commands.SaveCombatFile().execute(command.mod, combat.combat_data)
        elif command.command in commands.LoadCombatFile().valid_commands:
            combat.combat_data = commands.LoadCombatFile().execute(command.mod)
            combat.pull_data()

        # Rounds
        elif command.command in commands.NextRound().valid_commands:
            commands.NextRound().execute(combat)
        elif command.command in commands.RedoRound().valid_commands:
            commands.RedoRound().execute(combat)
        elif command.command in commands.UndoRound().valid_commands:
            commands.UndoRound().execute(combat)

        elif command.command in commands.NextTurn().valid_commands:
            commands.NextTurn().execute(combat)
        elif command.command in commands.PreviousTurn().valid_commands:
            commands.PreviousTurn().execute(combat)

        # End
        elif command.command in commands.EndCombat().valid_commands:
            commands.EndCombat().execute(combat)
            combat.dump_round_characters()
            return combat.characters

        elif "help" == command:
            hide_help = False

        elif command.command.isnumeric():
            combat.remove_note(int(command.command) - 1)
        elif command.items is None and command.mod is None:
            combat.notes.append(command.command)


# start up the game to create or load a party
waiting_for_input = True
file_found = True
while waiting_for_input:
    os.system("cls")
    print(art.logo)
    print(art.info)
    if not file_found:
        print("\nFile not found")
    start_command = input("\nType a new party name or 'load' one: ").lower()
    if start_command == "load":
        file_name = input("Enter file name: ").lower()
        if save_data.does_file_exists(f"P-{file_name}"):
            loaded_party = save_data.load_party(file_name)
            characters_list = loaded_party.characters
            notes = loaded_party.notes
            party_name = loaded_party.name
            waiting_for_input = False
        else:
            file_found = False
    else:
        party_name = start_command
        waiting_for_input = False

party_mode()
