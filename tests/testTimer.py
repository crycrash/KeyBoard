import unittest
import tkinter as tk
from timer import TimerApp

class TestTimerApp(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()

    def test_initialization(self):
        app = TimerApp(self.root)
        self.assertIsInstance(app, TimerApp)
        self.assertIsNone(app.time_label)
        self.assertEqual(app.all_time, 0)
        self.assertFalse(app.timer_running)

    def test_pack_label(self):
        app = TimerApp(self.root)
        app.pack_label(50, 50)
        self.assertIsInstance(app.time_label, tk.Label)
        self.assertEqual(app.time_label.winfo_x(), 0)
        self.assertEqual(app.time_label.winfo_y(), 0)

    def test_start_timer(self):
        app = TimerApp(self.root)
        app.pack_label(50, 50)
        app.start_timer()
        self.assertTrue(app.timer_running)

    def test_stop_timer(self):
        app = TimerApp(self.root)
        app.pack_label(50, 50)
        app.start_timer()
        app.stop_timer()
        self.assertFalse(app.timer_running)

    def tearDown(self):
        self.root.destroy()
