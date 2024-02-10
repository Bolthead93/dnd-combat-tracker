class Character:
    def __init__(self, name="name", hp=0, char_type="player", group_type="none"):
        self.name = name
        self.hp = 0
        self.max_hp = 0
        self.ac = 0
        self.temp_hp = 0
        self.actions = []
        self.buffs = []
        self.conditions = []
        self.type = char_type
        self.group = group_type


    def set_hp(self, amount):
        if not amount.isnumeric():
            mod = amount[0]
            value = int(amount[1:])
        else:
            mod = ""
            value = int(amount)

        if "-" in mod:
            self.temp_hp -= value
            if self.temp_hp < 0:
                self.hp += self.temp_hp
                self.temp_hp = 0
        elif "+" in mod:
            self.hp += value
            if self.hp > self.max_hp:
                self.hp = self.max_hp
        else:
            self.hp = value
            if self.max_hp == 0:
                self.max_hp = self.hp

    def set_temp_hp(self, amount):
        if amount.isnumeric():
            self.temp_hp = int(amount)

    def set_max_hp(self, amount):
        if amount.isnumeric():
            self.max_hp = int(amount)
            if int(amount) < self.hp:
                self.set_hp(amount)

    def set_ac(self, amount):
        if amount.isnumeric():
            self.ac = int(amount)

    def apply_buff(self, new_buff):
        buff_exists = False
        current_buff = None
        for buff in self.buffs:
            if buff.name.lower() == new_buff.name.lower():
                current_buff = buff
                buff_exists = True
        if not buff_exists:
            self.buffs.append(new_buff)
        elif buff_exists and new_buff.duration > current_buff.duration:
            self.remove_buff(current_buff.name)
            self.buffs.append(new_buff)

    def apply_condition(self, new_cond):
        cond_exists = False
        current_cond = None
        for cond in self.conditions:
            if cond.name.lower() == new_cond.name.lower():
                current_cond = cond
                cond_exists = True
        if not cond_exists:
            self.conditions.append(new_cond)
        elif cond_exists and new_cond.duration > current_cond.duration:
            self.remove_condition(current_cond.name)
            self.conditions.append(new_cond)

    def get_buffs(self):
        """returns the buffs as a nice list"""
        nice_buff_list = []
        for b in self.buffs:
            nice_buff_list.append(b.format_buff_info())
        return nice_buff_list

    def get_conditions(self):
        """returns the conditions as a nice list"""
        nice_cond_list = []
        for c in self.conditions:
            nice_cond_list.append(c.format_buff_info())
        return nice_cond_list

    def count_round(self):
        self.clear_inactive_buffs()
        self.clear_inactive_conditions()
        for buff in self.buffs:
            buff.duration_count()
        for cond in self.conditions:
            cond.duration_count()

    def remove_buff(self, buff_name):
        """remove a single buff by name"""
        for buff in self.buffs:
            if buff.name.lower() == buff_name.lower():
                self.buffs.remove(buff)

    def remove_condition(self, cond_name):
        """remove a single condition by name"""
        for cond in self.conditions:
            if cond.name.lower() == cond_name.lower():
                self.conditions.remove(cond)

    def remove_all_buffs(self):
        self.buffs = []

    def remove_all_conditions(self):
        self.conditions = []

    def check_finished_modifiers(self):
        """return true if there is any buffs ending this turn"""
        for buff in self.buffs:
            if buff.duration == 0:
                return True
        for cond in self.conditions:
            if cond.duration == 0:
                return True

    def get_finished_modifiers(self):
        finished_buffs = []
        finished_conditions = []
        for buff in self.buffs:
            if buff.duration == 0:
                finished_buffs.append(buff.name)
        for cond in self.conditions:
            if cond.duration == 0:
                finished_conditions.append(cond.name)
        if len(finished_buffs) == 0:
            end_buffs = ""
        else:
            end_buffs = f"Buffs ending: {str(", ").join(finished_buffs)},"
        if len(finished_conditions) == 0:
            end_conds = ""
        else:
            end_conds = f"Conditions ending: {str(", ").join(finished_conditions)}"
        return f"{end_buffs}{end_conds}"

    def clear_inactive_buffs(self):
        for buff in self.buffs:
            if buff.duration <= 0:
                self.buffs.remove(buff)

    def clear_inactive_conditions(self):
        for cond in self.conditions:
            if cond.duration <= 0:
                self.conditions.remove(cond)

    def add_action(self, action):
        self.actions.append(action)

    def remove_action(self, index):
        if len(self.actions) > 0:
            self.actions.remove(self.actions[index])
        if len(self.actions) == 0:
            self.actions.append("idle")

    def get_info(self):

        hp = ""
        if self.hp != 0:
            hp = f"HP: {self.hp}/{self.max_hp}, "
        if self.temp_hp > 0:
            hp = f"HP: {self.hp}/{self.max_hp}(+{self.temp_hp}), "

        ac = ""
        if self.ac > 0:
            ac = f" AC: {self.ac}, "

        actions = ""
        if len(self.actions) > 0:
            actions = f"Actions: {self.actions}, "

        buffs = ""
        if len(self.buffs) > 0:
            buffs = f"Buffs: {self.get_buffs()},"

        conditions = ""
        if len(self.conditions) > 0:
            conditions = f"Conditions: {self.get_conditions()}"

        return f"{self.name}, {ac} {hp} {actions} {buffs} {conditions}"
