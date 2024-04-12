import sqlite3


class DataBase:
    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        data TEXT NOT NULL,
        speed INTEGER,
        mistakes INTEGER,
        score INTEGER
        )
        ''')
        self.connection.commit()

    def close_database(self):
        self.connection.close()

    def insert_statistic(self, name, data, speed, mistakes, score):
        self.cursor.execute('INSERT INTO Users (username, data, speed, mistakes, score) VALUES (?, ?, ?, ?, ?)',
                            (str(name), str(data), speed, mistakes, score))
        self.connection.commit()

    def choosing_usernames(self):
        self.cursor.execute('SELECT DISTINCT username FROM Users')

        return self.cursor.fetchall()

    def count_number_of_records(self, username):
        self.cursor.execute(f'SELECT COUNT(*) FROM Users WHERE username = (?)', username)
        return self.cursor.fetchall()[0]

    def return_latest_name(self):
        self.cursor.execute(f'SELECT * FROM Users ORDER BY data ASC LIMIT 1')
        return self.cursor.fetchall()[0]

    def delete_latest_name(self, name):
        print(name)
        self.cursor.execute('DELETE FROM Users WHERE username = (?)', (name,))
        self.connection.commit()

    def personal_statistic(self, name):
        self.cursor.execute(f'SELECT * FROM Users WHERE username = (?)', (name,))
        return self.cursor.fetchall()
