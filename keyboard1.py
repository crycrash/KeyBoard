import time
import tkinter.messagebox as mb
from tkinter import *

window = Tk()
dict_codes = {"!": 2, "'": 3, "№": 4, ";": 5, "%": 6,
              ":": 7, "?": 8, "*": 9, "(": 10, ")": 11,
              "-": 12, "+": 13, "й": 16,
              "ц": 17, "у": 18, "к": 19, "е": 20, "н": 21,
              "г": 22, "ш": 23, "щ": 24, "з": 25, "х": 26,
              "ъ": 27, "ф": 30, "ы": 31, "в": 32, "а": 33,
              "п": 34, "р": 35, "о": 36, "л": 37, "д": 38,
              "ж": 39, "э": 40, "ё": 41, "|": 43, "я": 44,
              "ч": 45, "с": 46, "м": 47, "и": 48, "т": 49,
              "ь": 50, "б": 51, "ю": 52, ".": 53, " ": 57}

keys = {}
pointer = 0
red_cliks = []


def start_window():
    window.title("Привет!")
    name_window = Label(window, text="Клавиатурный тренажер", fg="white", font=("Arial Bold", 50), bg="blue")
    name_window.pack(anchor=N)
    window.geometry("900x700")
    window.configure(background="blue")

    button_start = Button(window,
                          text="Давай играть",
                          width=30, height=5,
                          bg='white', fg="black"
                          )
    button_start.bind("<Button-1>", keyboard_visualizing)
    button_start.pack(anchor=S)
    window.mainloop()


def keyboard_visualizing(event):
    window.withdraw()
    play_window = Toplevel()
    play_window.protocol("WM_DELETE_WINDOW", lambda: window.destroy())

    play_window.title("Игра")
    play_window.geometry("900x700")
    text = "рплгалгмра"

    def coloring_answer(code):
        global pointer
        global red_cliks
        for wid in play_window.winfo_children():
            if isinstance(wid, Button):
                if text[pointer] == code.char:
                    while red_cliks:
                        keys[red_cliks.pop()].config(bg="orange")
                    keys[skan_codes(code.char)].config(bg="green")
                    play_window.update()
                    pointer += 1
                    time.sleep(0.2)
                    keys[skan_codes(code.char)].config(bg="orange")
                    if pointer == len(text):
                        message_box()
                    return
                else:
                    try:
                        keys[skan_codes(code.char)].config(bg="red")
                        red_cliks.append(skan_codes(code.char))
                    except KeyError:
                        continue

    place_key(play_window)
    play_window.bind("<Key>", coloring_answer)
    paint_text(text, play_window)


def message_box():
    answer = mb.askyesno(title="Поздравляем!", message="Хотите сыграть еще раз?")
    if answer:
        global pointer
        global red_cliks
        pointer = 0
        red_cliks = []
        start_window()
    else:
        window.destroy()


def place_key(play_window):
    for i in range(2, 54):
        if (i != 14) and (i != 15) and (i != 28) and (i != 29) and (i != 42):
            btn = Button(play_window, bd=5, font=("", 15), bg="orange",
                         text=list(dict_codes.keys())[list(dict_codes.values()).index(i)])
            coordinate_x, coordinate_y = coordinates_counting(i)
            btn.place(x=coordinate_x, y=coordinate_y, width=50, height=50)
            keys[i] = btn
        else:
            continue
    btn = Button(play_window, bd=5, font=("", 15), bg="orange",
                 text=list(dict_codes.keys())[list(dict_codes.values()).index(57)])
    coordinate_x, coordinate_y = coordinates_counting(57)
    btn.place(x=coordinate_x, y=coordinate_y, width=80, height=50)
    keys[57] = btn


def paint_text(text1, play_window):
    writing = Text(play_window)
    label = Label(play_window, text=text1, background="green")
    label.text = writing
    label.place(x=400, y=600)
    play_window.update()


def coordinates_counting(num):
    if num <= 13 or num == 41:
        coordinate_y = 100
        coordinate_x = (900 // 13) * (remainder(num, 13) - 1)
        if num == 41:
            coordinate_x = 23

    elif num <= 27:
        coordinate_y = 200
        coordinate_x = (900 // 13) * (remainder(num, 14) - 2)

    elif num <= 43 and num != 41:
        coordinate_y = 300
        coordinate_x = (900 // 13) * (remainder(num, 29))
        if num == 43:
            coordinate_x = (900 // 13) * 12

    else:
        coordinate_y = 400
        coordinate_x = (900 // 13) * (remainder(num, 43))
        if num == 57:
            coordinate_y = 470
            coordinate_x = 400
    return coordinate_x, coordinate_y


def remainder(n, k):
    if n % k == 0:
        return k
    else:
        return n % k


def skan_codes(code):
    return dict_codes[code]


def main():
    start_window()


if __name__ == "__main__":
    main()
