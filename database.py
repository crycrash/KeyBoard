import json
from datetime import datetime

class DataBase:
    def __init__(self):
        self.data = None
        self.file_path = 'database.json'
        self.load_data()

    def load_data(self):
        try:
            with open(self.file_path, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {'Users': []}

    def save_data(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file, indent=4)

    def close_database(self):
        pass  # No need to close a JSON file

    def insert_statistic(self, name, data, speed, mistakes, score):
        new_entry = {
            'username': name,
            'data': data,
            'speed': speed,
            'mistakes': mistakes,
            'score': score
        }
        self.data['Users'].append(new_entry)
        self.save_data()

    def choosing_usernames(self):
        usernames = {user['username'] for user in self.data['Users']}
        return list(usernames)

    def count_number_of_records(self, username):
        count = sum(1 for user in self.data['Users'] if user['username'] == username)
        return count

    def return_latest_name(self):
        if not self.data['Users']:
            return None
        latest_entry = min(self.data['Users'], key=lambda x: datetime.strptime(x['data'], '%Y-%m-%d'))
        return latest_entry

    def delete_latest_name(self, name):
        for user in self.data['Users']:
            if user['username'] == name:
                self.data['Users'].remove(user)
                self.save_data()

    def personal_statistic(self, name):
        user_data = []
        for user in self.data['Users']:
            if user['username'] == name:
                user_data.append(user)

        return user_data
