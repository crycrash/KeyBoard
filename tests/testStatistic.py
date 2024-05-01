import unittest
from repository import Repository
from datetime import date
from statistic import Stat


class TestStat(unittest.TestCase):
    def setUp(self):
        self.stat = Stat("databaseTest.json")

    def test_initialization(self):
        self.assertEqual(self.stat.count_of_symbol, 0)
        self.assertEqual(self.stat.speed, 0)
        self.assertEqual(self.stat.mistakes, 0)
        self.assertEqual(self.stat.score, 0)
        self.assertIsNone(self.stat.repository)
        self.assertIsNotNone(self.stat.path)

    def test_count_speed(self):
        self.stat.count_of_symbol = 100
        self.stat.count_speed(60)
        self.assertEqual(self.stat.speed, 60)

        self.stat.count_of_symbol = 120
        self.stat.count_speed(60)
        self.assertEqual(self.stat.speed, 120)

    def test_count_stat(self):
        self.stat.count_of_symbol = 100
        self.stat.mistakes = 5
        self.stat.count_stat(60)
        self.assertEqual(self.stat.score, 350)

        self.stat.count_of_symbol = 120
        self.stat.mistakes = 10
        self.stat.count_stat(60)
        self.assertEqual(self.stat.score, 700)

    def test_enter_statistics(self):
        name = "TestUser"
        self.stat.speed = 100
        self.stat.mistakes = 5
        self.stat.score = 950
        self.stat.enter_statistics(name)

        repository = Repository('databaseTest.json')
        stats = repository.personal_statistic(name)
        self.assertTrue(stats)

    def test_output_usernames(self):
        usernames = self.stat.output_usernames()
        self.assertEqual(len(usernames), 1)

        repository = Repository('databaseTest.json')
        repository.insert_statistic("TestUser", str(date.today()), 100, 5, 950)

        usernames = self.stat.output_usernames()
        self.assertEqual(usernames, ["TestUser"])

    def test_output_count_records(self):
        # No records for the username
        count = self.stat.output_count_records("TestUser")
        self.assertIsNotNone(count)

        # Insert a record
        repository = Repository('databaseTest.json')
        repository.insert_statistic("TestUser", str(date.today()), 100, 5, 950)

        # Check if the count is returned correctly
        count = self.stat.output_count_records("TestUser")
        self.assertEqual(count, 1)

    def test_latest_name(self):
        name = self.stat.latest_name()
        self.assertIsNotNone(name)

        # Insert a record
        repository = Repository('databaseTest.json')
        repository.insert_statistic("TestUser", str(date.today()), 100, 5, 950)

        # Get the latest name and then delete it
        name = self.stat.latest_name()
        self.assertEqual(name, "TestUser")

    def test_user_statistic_array(self):
        # No statistics for the user
        array_statistic = self.stat.user_statistic_array("TestUser")
        self.assertEqual(len(array_statistic), 2)

        # Insert a record
        repository = Repository('databaseTest.json')
        repository.insert_statistic("TestUser", str(date.today()), 100, 5, 950)

        # Check if the statistics are returned correctly
        array_statistic = self.stat.user_statistic_array("TestUser")
        self.assertIsNotNone(array_statistic)
