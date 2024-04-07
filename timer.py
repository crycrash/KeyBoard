import tkinter as tk
import time


class TimerApp:
    def __init__(self, root_window):
        self.start_time = time.time()
        self.root = root_window

        self.time_label = None
        self.all_time = 0
        self.timer_running = False

    def pack_label(self, coordinate_x, coordinate_y):
        self.time_label = tk.Label(self.root, text="00:00", font=("Helvetica", 24))
        self.time_label.place(x=coordinate_x, y=coordinate_y)

    def start_timer(self):
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        current_time = time.time() - self.start_time
        minutes = int((current_time % 3600) // 60)
        seconds = int(current_time % 60)

        self.time_label.config(text=f"{minutes:02}:{seconds:02}")
        self.all_time = current_time
        if self.timer_running:
            self.root.after(500, self.update_timer)

    def stop_timer(self):
        self.timer_running = False
