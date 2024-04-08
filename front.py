import tkinter
import tkinter.messagebox as mb
from tkinter import *
from back import skan_codes, coordinates_counting, value_code, take_text
from timer import TimerApp
from statistic import Stat
import time


class KeyboardView:
    def __init__(self):
        self.window = Tk()
        self.pointer = 0
        self.red_cliks = []
        self.text = None
        self.timer = None
        self.keys = {}
        self.name = ''
        self.stat_game = None

    def start_window(self):
        self.window.title("Привет!")
        name_window = Label(self.window, text="Клавиатурный тренажер", fg="white", font=("Arial Bold", 50), bg="blue")
        name_window.pack(anchor=N)
        self.window.geometry("900x700")
        self.window.configure(background="blue")
        self.start_button()
        self.window.mainloop()

    def start_button(self):
        button_start = Button(self.window,
                              text="Давай играть",
                              width=30, height=5,
                              bg='white', fg="black"
                              )
        button_start.bind("<Button-1>", self.window_asc_name)
        button_start.pack(anchor=S)
        button_statistic = Button(self.window,
                                  text="Cтатистика",
                                  width=30, height=5,
                                  bg='white', fg="black"
                                  )
        button_statistic.bind("<Button-1>", self.window_statistic)
        button_statistic.pack(anchor=S)

    def window_asc_name(self, event):
        self.window.withdraw()
        play_window = Toplevel()
        play_window.protocol("WM_DELETE_WINDOW", lambda: self.window.destroy())
        label = Label(play_window, text="Введите имя")
        label.pack(anchor=S)
        play_window.title("Введите свое имя")
        button = self.continue_button(play_window)
        self.remind_name(play_window, button)
        play_window.geometry("900x700")

    def remind_name(self, play_window, button):
        name = Text(play_window, height=1, width=60, font='Arial 15', wrap="word")
        name.pack(anchor=S)
        self.save_button(play_window, name, button)
        play_window.update()

    def save_name(self, name, button, play_window, event):
        expected_name = name.get("1.0", "end")
        if expected_name != '\n':
            self.name = expected_name[:len(expected_name) - 1]
            button.config(state=NORMAL)
            button.bind("<Button-1>", lambda e: self.keyboard_start_game(play_window, e))
        print(self.name)

    def continue_button(self, play_window):
        button_continue = Button(play_window,
                                 text="Продолжить",
                                 width=30, height=5,
                                 bg='white', fg="black",
                                 )
        button_continue.config(state=DISABLED)

        button_continue.pack(anchor=S)
        return button_continue

    def save_button(self, play_window, name, button):
        button_save = Button(play_window,
                             text="Сохранить имя",
                             width=30, height=5,
                             bg='white', fg="black"
                             )
        button_save.bind("<Button-1>", lambda e: self.save_name(name, button, play_window, e))
        button_save.pack(anchor=S)

    def keyboard_start_game(self, window_ex, event):
        window_ex.destroy()
        play_window = Toplevel()
        play_window.protocol("WM_DELETE_WINDOW", lambda: self.window.destroy())

        play_window.title("Игра")
        play_window.geometry("900x700")

        text_play = take_text()

        self.place_key(play_window)
        self.paint_text(text_play, play_window)
        self.timer = self.place_timer(play_window)
        self.place_pause(play_window)
        self.stat_game = Stat()
        play_window.bind("<Key>", lambda e: self.coloring_answer(e, text_play, play_window))

    def green_button_press(self, code, play_window, text):
        while self.red_cliks:
            self.keys[self.red_cliks.pop()].config(bg="orange")
        self.keys[skan_codes(code.char)].config(bg="green")
        play_window.update()
        self.pointer += 1
        time.sleep(0.1)
        self.keys[skan_codes(code.char)].config(bg="orange")
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
                btn = Button(play_window, bd=5, font=("", 15), bg="orange",
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
        btn = Button(play_window, bd=5, font=("", 15), bg="orange",
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
        stat_window = Toplevel()
        stat_window.protocol("WM_DELETE_WINDOW", lambda: self.window.destroy())
        stat_window.geometry("900x700")
        self.stat_game = Stat()
        array_of_usernames = self.stat_game.output_usernames()
        i = 0
        while array_of_usernames:
            name = array_of_usernames.pop()
            count = self.stat_game.output_count_records(name)
            button = Button(stat_window,
                            text=name,
                            width=30, height=5,
                            bg='white', fg="black",
                            )
            print(count)
            label = Label(stat_window, text=count, width=30, height=5,
                            bg='pink', fg="black")
            label.grid(row=i, column=1)
            button.grid(row=i, column=0)
            i+=1


a = KeyboardView()
a.start_window()
