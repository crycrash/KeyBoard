import unittest
from repository import Repository
import json


class TestRepository(unittest.TestCase):
    def setUp(self):
        self.file_path = "test_data.json"
        self.repo = Repository(self.file_path)

    def tearDown(self):
        self.repo.data = {'Users': []}
        self.repo.save_data()

    def test_initialization(self):
        self.assertIsNotNone(self.repo.data)
        self.assertEqual(self.repo.file_path, self.file_path)

    def test_load_data(self):
        with open(self.file_path, 'w') as file:
            json.dump(
                {'Users': [{'username': 'TestUser',
                            'data': '2024-05-01', 'speed': 100, 'mistakes': 5, 'score': 950}]},
                file)

        self.repo.load_data()
        self.assertEqual(len(self.repo.data['Users']), 1)
        self.assertEqual(self.repo.data['Users'][0]['username'], 'TestUser')

    def test_save_data(self):
        self.repo.data['Users'] = [
            {'username': 'TestUser', 'data': '2024-05-01', 'speed': 100, 'mistakes': 5, 'score': 950}]
        self.repo.save_data()

        with open(self.file_path, 'r') as file:
            saved_data = json.load(file)
            self.assertEqual(len(saved_data['Users']), 1)
            self.assertEqual(saved_data['Users'][0]['username'], 'TestUser')

    def test_insert_statistic(self):
        self.repo.insert_statistic('TestUser', '2024-05-01', 100, 5, 950)

        self.assertEqual(len(self.repo.data['Users']), 1)
        self.assertEqual(self.repo.data['Users'][0]['username'], 'TestUser')

    def test_choosing_usernames(self):
        self.repo.insert_statistic('TestUser1', '2024-05-01', 100, 5, 950)
        self.repo.insert_statistic('TestUser2', '2024-05-02', 110, 6, 960)
        self.repo.insert_statistic('TestUser1', '2024-05-03', 120, 7, 970)

        usernames = self.repo.choosing_usernames()
        self.assertEqual(len(usernames), 2)
        self.assertIn('TestUser1', usernames)
        self.assertIn('TestUser2', usernames)

    def test_count_number_of_records(self):
        self.repo.insert_statistic('TestUser1', '2024-05-01', 100, 5, 950)
        self.repo.insert_statistic('TestUser2', '2024-05-02', 110, 6, 960)
        self.repo.insert_statistic('TestUser1', '2024-05-03', 120, 7, 970)

        count = self.repo.count_number_of_records('TestUser1')
        self.assertEqual(count, 2)

    def test_return_latest_name(self):
        self.repo.insert_statistic('TestUser1', '2024-05-01', 100, 5, 950)
        self.repo.insert_statistic('TestUser2', '2024-05-02', 110, 6, 960)
        self.repo.insert_statistic('TestUser1', '2024-05-03', 120, 7, 970)

        latest_name = self.repo.return_latest_name()
        self.assertEqual(latest_name['username'], 'TestUser1')

    def test_delete_latest_name(self):
        self.repo.insert_statistic('TestUser1', '2024-05-01', 100, 5, 950)
        self.repo.insert_statistic('TestUser2', '2024-05-02', 110, 6, 960)
        self.repo.insert_statistic('TestUser1', '2024-05-03', 120, 7, 970)

        self.repo.delete_latest_name('TestUser1')

        latest_name = self.repo.return_latest_name()
        self.assertEqual(latest_name['username'], 'TestUser2')

    def test_personal_statistic(self):
        self.repo.insert_statistic('TestUser1', '2024-05-01', 100, 5, 950)
        self.repo.insert_statistic('TestUser2', '2024-05-02', 110, 6, 960)
        self.repo.insert_statistic('TestUser1', '2024-05-03', 120, 7, 970)

        user_statistic = self.repo.personal_statistic('TestUser1')
        self.assertEqual(len(user_statistic), 2)
        self.assertEqual(user_statistic[0]['username'], 'TestUser1')
        self.assertEqual(user_statistic[1]['username'], 'TestUser1')
