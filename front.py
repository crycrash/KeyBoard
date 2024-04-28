import tkinter
import tkinter.messagebox as mb
from tkinter import *
from keyboard._keyboard_event import KEY_DOWN, KEY_UP

import keyboard

from back import (skan_codes, coordinates_counting, value_code,
                  take_text, place_statistic_name, size_button, return_shift_key, return_shift_name)
from timer import TimerApp
from statistic import Stat
import time


class KeyboardView:
    def __init__(self):
        """Инициация стартового окна"""
        self.offset = 1
        self.window = Tk()
        self.pointer = 0
        self.red_cliks = []
        self.text = None
        self.timer = None
        self.keys = {}
        self.name = ''
        self.stat_game = None
        self.offset_height = 1
        self.flag_shift = 0

    def start_window(self):
        """Отображение стартового окна и кнопок"""
        self.window.title("Привет!")
        name_window = Label(self.window, text="Клавиатурный тренажер", fg="white", font=("Arial Bold", 50), bg="blue")
        name_window.pack(anchor=N)
        self.window.geometry("900x700")
        self.window.configure(background="blue")
        self.start_buttons()
        self.window.mainloop()

    @staticmethod
    def return_standard_button(text, window):
        """Cоздание базовой кнопки"""
        button = Button(window,
                        text=text,
                        width=30, height=5,
                        bg='white', fg="black"
                        )
        return button

    def start_buttons(self):
        """Помещение стартовых кнопок на экран"""
        button_start = self.return_standard_button("Игра", self.window)
        button_start.bind("<Button-1>", self.window_asc_name)
        button_start.pack(anchor=S)
        button_statistic = self.return_standard_button("Статистика", self.window)
        button_statistic.bind("<Button-1>", self.window_statistic)
        button_statistic.pack(anchor=S)

    def standard_window(self, text):
        """Создание базового окна"""
        play_window = Toplevel()
        play_window.protocol("WM_DELETE_WINDOW", lambda: self.window.destroy())
        play_window.title(text)
        play_window.geometry("1000x900")
        return play_window

    def window_asc_name(self, event):
        """Окно на котором запоминается имя пользователя"""
        self.window.withdraw()
        play_window = self.standard_window("Введите имя")
        label = Label(play_window, text="Введите имя")
        label.pack(anchor=S)
        button = self.continue_button(play_window)
        self.remind_name(play_window, button)

    def remind_name(self, play_window, button):
        """Поле ввода имени"""
        name = Text(play_window, height=1, width=60, font='Arial 15', wrap="word")
        name.pack(anchor=S)
        self.save_button(play_window, name, button)
        play_window.update()

    def save_button(self, play_window, name, button):
        """Кнопка сохранения имени"""
        button_save = self.return_standard_button("Сохранить имя", play_window)
        button_save.bind("<Button-1>", lambda e: self.save_name(name, button, play_window, e))
        button_save.pack(anchor=S)

    def save_name(self, name, button, play_window, event):
        """Сохранение имени"""
        expected_name = name.get("1.0", "end")
        if expected_name != '\n':
            self.name = expected_name[:len(expected_name) - 1]
            button.config(state=NORMAL)
            button.bind("<Button-1>", lambda e: self.keyboard_start_game(play_window, e))

    def continue_button(self, play_window):
        """Кнопка перехода к игре"""
        button_continue = self.return_standard_button("Продолжить", play_window)
        button_continue.config(state=DISABLED)
        button_continue.pack(anchor=S)
        return button_continue

    def keyboard_start_game(self, window_ex, event):
        """Окно игры"""
        window_ex.destroy()
        play_window = self.standard_window("Игра")
        text_play = take_text()
        self.place_key(play_window)
        self.paint_text(text_play, play_window)
        self.timer = self.place_timer(play_window)
        self.place_pause(play_window)
        self.stat_game = Stat()
        play_window.bind("<Key>", lambda e: self.coloring_answer(e, text_play, play_window))

    def check_flag_shift(self, code, color):
        self.keys[skan_codes(code)].config(bg=color)

    def green_button_press(self, code, play_window, text):
        """Верная клавиша"""
        while self.red_cliks:
            key_code = self.red_cliks.pop()
            try:
                self.check_flag_shift(key_code, 'black')
                print(key_code)
            except KeyError:
                self.keys[skan_codes(key_code.keysym)].config(bg="black")
        self.check_flag_shift(code, 'green')
        play_window.update()
        self.pointer += 1
        time_delay = 0.1
        time.sleep(time_delay)
        self.check_flag_shift(code, 'black')
        if self.pointer == len(text):
            self.message_box(play_window)

    def rad_button_press(self, code):
        """Неверная клавиша"""
        try:
            try:
                self.check_flag_shift(code, 'red')
            except KeyError:
                self.keys[skan_codes(code.keysym)].config(bg="red")
            finally:

                self.red_cliks.append(code)

        except KeyError:
            ...

    def message_box(self, play_window):
        """Окно после окончания игры"""
        self.timer.stop_timer()
        time_out = self.timer.all_time
        result = self.stat_game.count_stat(int(time_out))
        self.stat_game.enter_statistics(self.name)
        answer = mb.askyesno(title="Поздравляем!",
                             message="Ваше время:" + str(int(time_out)) +
                                     ". Ваши баллы:" + str(result) + ".Хотите сыграть еще раз?")
        if answer:
            self.go_to_menu(play_window)
        else:
            play_window.destroy()
            self.window.destroy()

    def shift_processing(self, event):
        if event.event_type == KEY_DOWN:
            self.on_press(event.name)

        elif event.event_type == KEY_UP:
            self.on_release(event.name)

    def coloring_answer(self, code, text, play_window):
        """Раскраска текста"""
        for wid in play_window.winfo_children():
            if isinstance(wid, Button):
                keyboard.hook(lambda e: self.shift_processing(e))
                if code.keysym == 'Shift_L' or code.keysym == 'Shift_R':
                    ...
                elif code.keysym == 'Escape':
                    self.exit_pause(play_window)
                    return
                elif text[self.pointer] == code.char:
                    if text[self.pointer] == '\r' or text[self.pointer] == '\n':
                        self.pointer += 1
                        self.offset_height += 1
                        self.offset = (-1 * self.pointer)
                    self.edit_text(self.pointer + self.offset, self.offset_height, code.char)
                    a = str(text[self.pointer])
                    a = a.lower()
                    self.green_button_press(code=a,
                                            play_window=play_window,
                                            text=text)
                    self.stat_game.count_of_symbol += 1
                    return
                else:
                    a = str(code.char)
                    a = a.lower()
                    self.rad_button_press(a)
                    self.stat_game.mistakes += 1
                    return

    def paint_text(self, text1, play_window):
        """Заливка текста зеленым"""
        self.text = Text(play_window, height=4, width=60, font='Arial 15', wrap="word")
        self.text.tag_configure("odd", background="green")
        self.text.insert("end", text1)
        self.text.place(x=10, y=200)
        self.text.configure(state=tkinter.DISABLED)
        play_window.update()

    def on_release(self, key):
        if key == 'shift' and self.flag_shift % 2 == 1:
            self.flag_shift = 0
            missed_keys = [14, 15, 28, 29, 42]
            for i in range(2, 54):
                if i not in missed_keys:
                    self.keys[i].config(text=value_code(i))
            print(2)


    def on_press(self, key):
        if key == 'shift' and self.flag_shift % 2 == 0:
            self.flag_shift = 1
            missed_keys = [14, 15, 28, 29, 42]
            for i in range(2, 54):
                if i not in missed_keys:
                    self.keys[i].config(text=return_shift_key(i))
            print(3)


    def place_key(self, play_window):
        """Размещение клавиш"""
        start_key = 2
        end_key = 74
        missing_keys = [14, 15, 28, 29, 42, 54, 55, 56]
        for i in range(start_key, end_key):
            if i not in missing_keys:
                btn = Button(play_window, bd=1, font=("", 15), bg="black", fg='white',
                             text=value_code(i))
                coordinate_x, coordinate_y = coordinates_counting(i)
                width, height = size_button(i)
                btn.place(x=coordinate_x, y=coordinate_y, width=width, height=height)
                self.keys[i] = btn
            else:
                continue

    def edit_text(self, length, wid, char):
        """Вставка зеленого цвета"""
        self.text.configure(state=tkinter.NORMAL)
        tag = "odd"
        if char == '\r':
            char = ''
        self.text.replace(str(wid) + '.' + str(length - 1), str(wid) + '.' + str(length), char, tag)
        self.text.configure(state=tkinter.DISABLED)

    @staticmethod
    def place_timer(play_window):
        """Размещение таймера"""
        timer = TimerApp(play_window)
        timer.pack_label(50, 50)
        timer.start_timer()
        return timer

    def go_to_menu(self, play_window):
        """Выход в меню"""
        self.pointer = 0
        self.red_cliks = []
        play_window.destroy()
        self.window.deiconify()

    def exit_pause(self, play_window):
        """Пауза"""
        start_time = time.time()
        self.timer.stop_timer()
        answer = mb.askyesno(title="Пауза",
                             message="Хотите продолжить?")
        end_time = time.time()
        if answer:
            self.timer.start_time = self.timer.start_time + (end_time - start_time)
            self.timer.start_timer()
        else:
            self.go_to_menu(play_window)

    def place_pause(self, play_window):
        """Размещение кнопки паузы"""
        button_pause = Button(play_window,
                              text="⏸️",
                              width=15, height=5,
                              bg='white', fg="black",
                              command=lambda: self.exit_pause(play_window)
                              )
        button_pause.place(x=600, y=50)

    def window_statistic(self, event):
        """Окно со статистикой"""
        self.window.withdraw()
        stat_window = self.standard_window("Статистика")
        self.stat_game = Stat()
        array_of_usernames = self.stat_game.output_usernames()
        row = 0
        button_back = self.button_back(self.window, stat_window)
        while array_of_usernames:

            name = array_of_usernames.pop()
            count = self.stat_game.output_count_records(name)
            button = self.button_statistic(stat_window, name)
            count_of_games = str(count)
            text = count_of_games + " игр"
            label = self.label_statistic(stat_window, text, 'pink')
            x, y = place_statistic_name(row)
            if x is None:
                self.stat_game.latest_name()
                row = 0
                x, y = place_statistic_name(row)
            label.grid(row=x, column=y + 1)
            button.grid(row=x, column=y)
            row += 1
        button_back.grid(row=6, column=3)

    def button_statistic(self, stat_window, name):
        """Кнопка статистики"""
        button = Button(stat_window,
                        text=name + " сыграл",
                        width=30, height=5,
                        bg='white', fg="black",
                        )
        button.bind("<Button-1>", lambda e: self.person_statistic(name, stat_window, e))
        return button

    def person_statistic(self, name, old_window, e):
        """Статистика пользователя"""
        old_window.withdraw()
        stat_window = self.standard_window(str(name[0]))
        self.stat_game = Stat()
        button_back = self.button_back(old_window, stat_window)
        user_stat = self.stat_game.user_statistic_array(name)
        arr_of_headers = ['Номер', 'Дата', 'Счет', 'Скорость', 'Ошибки']
        self.place_headers_table(stat_window, arr_of_headers, 0)
        row = 1
        while user_stat:
            name = user_stat.pop()
            arr_of_stat = [str(row), name['data'], name['score'], name['speed'], name['mistakes']]
            self.place_headers_table(stat_window, arr_of_stat, row)
            row += 1
        button_back.grid(row=6, column=3)

    def place_headers_table(self, window, arr_of_headers, row):
        """Размещение заголовка статистики"""
        label_number = self.label_statistic(window, arr_of_headers[0], 'aqua')
        label_data = self.label_statistic(window, arr_of_headers[1], 'pink')
        label_score = self.label_statistic(window, arr_of_headers[2], 'pink')
        label_speed = self.label_statistic(window, arr_of_headers[3], 'pink')
        label_mistakes = self.label_statistic(window, arr_of_headers[4], 'pink')

        label_number.grid(row=row, column=0)
        label_data.grid(row=row, column=1)
        label_score.grid(row=row, column=2)
        label_speed.grid(row=row, column=3)
        label_mistakes.grid(row=row, column=4)

    @staticmethod
    def label_statistic(stat_window, text, color):
        """Ячейка статистики"""
        label = Label(stat_window, text=text, width=22, height=5,
                      bg=color, fg="black")
        return label

    @staticmethod
    def button_back(window_new, window_old):
        """Кнопка перехода к прошлому окну"""
        button = Button(window_old,
                        text="Назад",
                        width=30, height=5,
                        bg='aqua', fg="black",
                        )

        def back_window(e, new_window, previous_window):
            """Закрытие старого окна"""
            new_window.deiconify()
            previous_window.destroy()

        button.bind("<Button-1>", lambda e: back_window(e, window_new, window_old))
        return button


a = KeyboardView()
a.start_window()
