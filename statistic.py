class Stat:
    def __init__(self):
        self.count_of_symbol = 0
        self.speed = 0
        self.mistakes = 0

    def count_speed(self, time):
        self.speed = (self.count_of_symbol // time) * 60

    def count_stat(self, time):
        self.count_speed(time)
        return (self.speed*10) - (self.mistakes*50)
