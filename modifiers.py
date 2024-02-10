class Modifier:
    def __init__(self, name="name", dur=0):
        self.name = name.title()
        self.duration = int(dur)
        if self.duration > 0:
            self.counter = -1
            self.style = " - "
        elif self.duration <= 0:
            self.counter = 1
            self.duration *= -1
            self.style = " + "

    def duration_count(self):
        self.duration += self.counter

    def format_buff_info(self):
        """returns the buff and info as a string like 'name + 4'"""
        buff_name = str(self.name)
        buff_duration = str(self.duration)
        return buff_name + self.style + buff_duration
