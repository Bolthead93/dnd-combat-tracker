from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
#     "excludes": ["tkinter", "unittest"],
    "includes": ["commands", "character", "art", "combat_manager",
                             "display", "modifiers", "party_manager", "save_data"],
}

setup(
    name="DnD-Combat-Tracker",
    version="0.1",
    description="Organisation for DnD Combat",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base="console", target_name="DnD-Combat-Tracker")],

)
