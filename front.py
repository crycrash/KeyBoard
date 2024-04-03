import tkinter
import tkinter.messagebox as mb
from tkinter import *
from back import skan_codes, coordinates_counting, value_code, take_text
import time


class KeyboardView:
    def __init__(self):
        self.window = Tk()
        self.pointer = 0
        self.red_cliks = []
        self.text = None

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
        button_start.bind("<Button-1>", self.keyboard_start_game)
        button_start.pack(anchor=S)

    def keyboard_start_game(self, event):
        self.window.withdraw()
        play_window = Toplevel()
        play_window.protocol("WM_DELETE_WINDOW", lambda: self.window.destroy())

        play_window.title("Игра")
        play_window.geometry("900x700")

        text_play = take_text()
        keys = {}
        self.place_key(play_window, keys)
        self.paint_text(text_play, play_window)
        play_window.bind("<Key>", lambda e: self.coloring_answer(e, text_play, play_window, keys))

    def green_button_press(self, keys, code, play_window, text):
        while self.red_cliks:
            keys[self.red_cliks.pop()].config(bg="orange")
        keys[skan_codes(code.char)].config(bg="green")
        play_window.update()
        self.pointer += 1
        time.sleep(0.1)
        keys[skan_codes(code.char)].config(bg="orange")
        if self.pointer == len(text):
            self.message_box(play_window)

    def rad_button_press(self, keys, code):
        try:
            keys[skan_codes(code)].config(bg="red")
            self.red_cliks.append(skan_codes(code))
        except KeyError:
            print("okay")

    def message_box(self, play_window):
        answer = mb.askyesno(title="Поздравляем!", message="Хотите сыграть еще раз?")
        if answer:
            self.pointer = 0
            self.red_cliks = []
            play_window.destroy()
            self.window.deiconify()
        else:
            play_window.destroy()
            self.window.destroy()

    def coloring_answer(self, code, text, play_window, keys):
        for wid in play_window.winfo_children():
            if isinstance(wid, Button):
                if text[self.pointer] == code.char:
                    self.edit_text(self.pointer + 1, 1, code.char)
                    self.green_button_press(keys=keys, code=code,
                                            play_window=play_window,
                                            text=text)
                    return
                else:
                    self.rad_button_press(keys, code.char)

    def paint_text(self, text1, play_window):
        self.text = Text(play_window, height=4, width=60, font='Arial 15')
        self.text.tag_configure("odd", background="green")
        self.text.insert("end", text1)
        self.text.place(x=10, y=200)
        self.text.configure(state=tkinter.DISABLED)
        play_window.update()

    def place_key(self, play_window, keys):
        for i in range(2, 54):
            if (i != 14) and (i != 15) and (i != 28) and (i != 29) and (i != 42):
                btn = Button(play_window, bd=5, font=("", 15), bg="orange",
                             text=value_code(i))
                coordinate_x, coordinate_y = coordinates_counting(i)
                btn.place(x=coordinate_x, y=coordinate_y, width=50, height=50)
                keys[i] = btn
            else:
                continue
        self.key_space(play_window, keys)

    def key_space(self, play_window, keys):
        btn = Button(play_window, bd=5, font=("", 15), bg="orange",
                     text=value_code(57))
        coordinate_x, coordinate_y = coordinates_counting(57)
        btn.place(x=coordinate_x, y=coordinate_y, width=80, height=50)
        keys[57] = btn

    def edit_text(self, length, wid, char):
        self.text.configure(state=tkinter.NORMAL)
        tag = "odd"
        self.text.replace(str(wid) + '.' + str(length - 1), str(wid) + '.' + str(length), char, tag)
        self.text.configure(state=tkinter.DISABLED)


a = KeyboardView()
a.start_window()
