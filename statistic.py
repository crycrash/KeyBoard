from repository import Repository
from datetime import date


class Stat:
    def __init__(self, path):
        """Инициализация статистики"""
        self.count_of_symbol = 0
        self.speed = 0
        self.mistakes = 0
        self.score = 0
        self.repository = None
        self.path = path

    def count_speed(self, time):
        """Подсчет скорости"""
        self.speed = (self.count_of_symbol // time) * 60

    def count_stat(self, time):
        """Высчитывание статистики"""
        self.count_speed(time)
        self.score = (self.speed*10) - (self.mistakes*50)
        return self.score

    def enter_statistics(self, name):
        """Выбор статистики"""
        self.repository = Repository(self.path)
        self.repository.insert_statistic(name, str(date.today()), self.speed, self.mistakes, self.score)

    def output_usernames(self):
        """Вывод имен"""
        self.repository = Repository(self.path)
        arr = self.repository.choosing_usernames()
        return arr

    def output_count_records(self, name):
        """Вывод записи"""
        self.repository = Repository(self.path)
        count = self.repository.count_number_of_records(name)
        return count

    def latest_name(self):
        """Последнее имя"""
        self.repository = Repository(self.path)
        name = self.repository.return_latest_name()['username']
        self.repository.delete_latest_name(name)
        return name

    def user_statistic_array(self, name):
        """Статистика пользователя"""
        self.repository = Repository(self.path)
        array_statistic = self.repository.personal_statistic(name)
        return array_statistic
