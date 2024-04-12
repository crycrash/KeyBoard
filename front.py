import tkinter
import tkinter.messagebox as mb
from tkinter import *
from back import skan_codes, coordinates_counting, value_code, take_text, place_statistic_name
from timer import TimerApp
from statistic import Stat
import time


class KeyboardView:
    def __init__(self):
        """Инициация стартового окна"""
        self.window = Tk()
        self.pointer = 0
        self.red_cliks = []
        self.text = None
        self.timer = None
        self.keys = {}
        self.name = ''
        self.stat_game = None

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
        play_window.geometry("900x700")
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

    def green_button_press(self, code, play_window, text):
        while self.red_cliks:
            self.keys[self.red_cliks.pop()].config(bg="aqua")
        self.keys[skan_codes(code.char)].config(bg="green")
        play_window.update()
        self.pointer += 1
        time.sleep(0.1)
        self.keys[skan_codes(code.char)].config(bg="aqua")
        if self.pointer == len(text):
            self.message_box(play_window)

    def rad_button_press(self, code):
        try:
            self.keys[skan_codes(code)].config(bg="red")
            self.red_cliks.append(skan_codes(code))
        except KeyError:
            ...

    def message_box(self, play_window):
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

    def coloring_answer(self, code, text, play_window):
        for wid in play_window.winfo_children():
            if isinstance(wid, Button):
                if code.keysym == 'Escape':
                    self.exit_pause(play_window)
                    return
                elif text[self.pointer] == code.char:
                    self.edit_text(self.pointer + 1, 1, code.char)
                    self.green_button_press(code=code,
                                            play_window=play_window,
                                            text=text)
                    self.stat_game.count_of_symbol += 1
                    return
                else:
                    self.rad_button_press(code.char)
                    self.stat_game.mistakes += 1
                    return

    def paint_text(self, text1, play_window):
        self.text = Text(play_window, height=4, width=60, font='Arial 15', wrap="word")
        self.text.tag_configure("odd", background="green")
        self.text.insert("end", text1)
        self.text.place(x=10, y=200)
        self.text.configure(state=tkinter.DISABLED)
        play_window.update()

    def place_key(self, play_window):
        for i in range(2, 54):
            if (i != 14) and (i != 15) and (i != 28) and (i != 29) and (i != 42):
                btn = Button(play_window, bd=5, font=("", 15), bg="aqua",
                             text=value_code(i))
                coordinate_x, coordinate_y = coordinates_counting(i)
                btn.place(x=coordinate_x, y=coordinate_y, width=50, height=50)
                self.keys[i] = btn
            else:
                continue
        self.key_space(play_window)

    def edit_text(self, length, wid, char):
        self.text.configure(state=tkinter.NORMAL)
        tag = "odd"
        self.text.replace(str(wid) + '.' + str(length - 1), str(wid) + '.' + str(length), char, tag)
        self.text.configure(state=tkinter.DISABLED)

    @staticmethod
    def place_timer(play_window):
        timer = TimerApp(play_window)
        timer.pack_label(50, 50)
        timer.start_timer()
        return timer

    def key_space(self, play_window):
        btn = Button(play_window, bd=5, font=("", 15), bg="aqua",
                     text=value_code(57))
        coordinate_x, coordinate_y = coordinates_counting(57)
        btn.place(x=coordinate_x, y=coordinate_y, width=80, height=50)
        self.keys[57] = btn

    def go_to_menu(self, play_window):
        self.pointer = 0
        self.red_cliks = []
        play_window.destroy()
        self.window.deiconify()

    def exit_pause(self, play_window):
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
        button_pause = Button(play_window,
                              text="⏸️",
                              width=15, height=5,
                              bg='white', fg="black",
                              command=lambda: self.exit_pause(play_window)
                              )
        button_pause.place(x=600, y=50)

    def window_statistic(self, event):
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
            count_of_games = str(count[0])
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
        button = Button(stat_window,
                        text=name[0] + " сыграл",
                        width=30, height=5,
                        bg='white', fg="black",
                        )
        button.bind("<Button-1>", lambda e: self.person_statistic(name, stat_window, e))
        return button

    def person_statistic(self, name, old_window, e):
        old_window.withdraw()
        stat_window = self.standard_window(str(name[0]))
        self.stat_game = Stat()
        button_back = self.button_back(old_window, stat_window)
        user_stat = self.stat_game.user_statistic_array(name[0])
        arr_of_headers = ['Номер', 'Дата', 'Счет', 'Скорость', 'Ошибки']
        self.place_headers_table(stat_window, arr_of_headers, 0)
        row = 1
        while user_stat:
            name = user_stat.pop()
            arr_of_stat = [str(row), name[2], name[5], name[3], name[4]]
            self.place_headers_table(stat_window, arr_of_stat, row)
            row += 1
        button_back.grid(row=6, column=3)

    def place_headers_table(self, window, arr_of_headers, row):
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
        label = Label(stat_window, text=text, width=22, height=5,
                      bg=color, fg="black")
        return label

    def button_back(self, window_new, window_old):
        button = Button(window_old,
                        text="Назад",
                        width=30, height=5,
                        bg='aqua', fg="black",
                        )

        def back_window(e, new_window, previous_window):
            new_window.deiconify()
            previous_window.destroy()

        button.bind("<Button-1>", lambda e: back_window(e, window_new, window_old))
        return button


a = KeyboardView()
a.start_window()
