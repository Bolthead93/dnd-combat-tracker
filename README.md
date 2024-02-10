A tool to help you remember who's got what in the middle of combat. Add players and creatures to the lists, using commands you can add buffs, debuffs, and descriptions As you finish a turn of combat, use the 'n' command to advanced the round, automatically updating stats.

HOW TO USE:

    - Input a command followed by names to create or edit characters, all commands are to be split by a comma(,).
    - For example, to create players, type 'np,jim,bing' to create 2 new players with the names 'jim' and 'bing'.
    - Take notes by just typing the note.
     - You can multi-edit players, creatures, or groups, for example:
        - 'hp,zombie1,zombie2,zombie3' and then typing a value, will set the HP of all of these to that value.
        - Alternatively, if you made 3 zombies using the group command, you can type 'hp,group,zombie'.

COMMANDS:

    - Add new player (nc,[PLAYER NAME]) - adds player(s) to the players list.
    - Add new creature (nc,[CREATURE NAME]) - adds a creature to the creatures list.
    - Add new creature group (ncg,[CREATURE NAME],[AMOUNT TO ADD]) - add a group of creatures with the same name,
        for example 'ncg,zombies,6' will add 6 zombies, they will become part of a group called 'zombies'.
    - Edit Player/Creature  [COMMAND],[NAME(s)] - edit a character(s) info, replace [COMMANDS] with the below commands.
        Edit Commands:
            - Actions: Action Add (a), Action Overwrite (ao), Action Remove First (arf), Action Remove Last (arl).
                Updates the description of a player, good for tracking basic info like 'readying a spell'.
            - Buffs: Add Buff (b), Remove Buff (br), Remove All Buffs (bra).
                Add or Remove buffs, this will ask you for a name and duration,
                use a positive number ('10') for the tracker to count it down, or use
                a negative number to count up ('-4' will start counting up from 4).
            - Conditions: Add Condition (c), Remove Condition (cr), Remove All Condition (cra).
                Uses the same system as buffs.
            - Health: (hp) - you will be prompted to set, increase, or decrease health by typing a number.
            - Temp Health (hpt) - same as the health input.
            - Health Max (hpm) - set the max HP. when setting 'hp' the first time, this will be set to that value.
            - Set AC (ac) - set the AC for characters.
            -Remove from list (remove,[NAME]) - 'remove,jimothy' will remove jimothy from the list.
    - Edit Groups ([COMMAND],group,[GROUP NAME]) - change info for all creatures in a group.
        Useful for setting info on enemies of the same type, e.g. 'hp,group,zombies' '22' to set all to 22 HP.
    - Add to Group (group,[GROUP NAME],[NAME],[NAME]..) - tag existing character/creatures with a group name.
    - Next round [N] - Progress to the next round, buffs and conditions will be calculated.
    - Save/Load (save) (load) - this will save the current encounter, or load an encounter at the latest round.
    - Round Reverse (rr) / Round Forward (rf) - step backwards and forwards through turns.
    - Save/Load Party [SP] / [LP] - saves the players list, loads players list.
        Saving and Loading is useful for setting up groups that you'll use often.
    - Take a note - submit any text to add a note, submit the notes number to remove the related note.
    - Show Help [HELP] - show this help information.
    - End Combat [END] - closes the combat tracker and saves out the log to a text file.
