from database import DataBase
from datetime import date
class Stat:
    def __init__(self):
        self.count_of_symbol = 0
        self.speed = 0
        self.mistakes = 0
        self.score = 0
        self.data_base = None

    def count_speed(self, time):
        self.speed = (self.count_of_symbol // time) * 60

    def count_stat(self, time):
        self.count_speed(time)
        self.score = (self.speed*10) - (self.mistakes*50)
        return self.score

    def enter_statistics(self, name):
        self.data_base = DataBase()
        self.data_base.insert_statistic(name, str(date.today()), self.speed, self.mistakes, self.score)
        self.data_base.close_database()

    def output_usernames(self):
        self.data_base = DataBase()
        arr = self.data_base.choosing_usernames()
        self.data_base.close_database()
        return arr

    def output_count_records(self, name):
        self.data_base = DataBase()
        count = self.data_base.count_number_of_records(name)
        self.data_base.close_database()
        return count