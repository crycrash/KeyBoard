import tkinter as tk
import time


class TimerApp:
    def __init__(self, root_window):
        """Инициализация таймера"""
        self.start_time = time.time()
        self.root = root_window

        self.time_label = None
        self.all_time = 0
        self.timer_running = False

    def pack_label(self, coordinate_x, coordinate_y):
        """Установка таймера"""
        self.time_label = tk.Label(self.root, text="00:00", font=("Helvetica", 24))
        self.time_label.place(x=coordinate_x, y=coordinate_y)

    def start_timer(self):
        """Запуск таймера"""
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        """Обновление времени таймера"""
        current_time = time.time() - self.start_time
        seconds_in_hour = 3600
        seconds_in_minute = 60
        minutes = int((current_time % seconds_in_hour) // seconds_in_minute)
        seconds = int(current_time % seconds_in_minute)

        self.time_label.config(text=f"{minutes:02}:{seconds:02}")
        self.all_time = current_time
        time_update = 500
        if self.timer_running:
            self.root.after(time_update, self.update_timer)

    def stop_timer(self):
        """Остановка таймера"""
        self.timer_running = False
