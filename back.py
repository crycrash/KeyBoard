import random

from config import dict_codes, dict_shift


def first_row(num):
    """Подсчет координаты клавиши в первой строке"""
    coordinate_y = 350
    coordinate_x = (900 // 13) * (remainder(num, 13) - 1)
    if num == 41:
        coordinate_x = 0
    elif num == 58:
        coordinate_x = 897
    return coordinate_x, coordinate_y


def second_row(num):
    """Подсчет координаты клавиши во второй строке"""
    coordinate_y = 400
    coordinate_x = (900 // 13) * (remainder(num, 14) - 2) + 105
    if num == 59:
        coordinate_x = 0
    return coordinate_x, coordinate_y


def third_row(num):
    """Подсчет координаты клавиши в третьей строке"""
    coordinate_y = 450
    coordinate_x = (900 // 13) * (remainder(num, 29)) + 45
    if num == 43:
        coordinate_y = 400
        coordinate_x = (900 // 13) * 12 + 105
    elif num == 60:
        coordinate_x = 0
    elif num == 61:
        coordinate_x = 880
    return coordinate_x, coordinate_y


def four_row(num):
    """Подсчет координаты клавиши в четвертой строке"""
    coordinate_y = 500
    coordinate_x = (900 // 13) * (remainder(num, 43)) + 75
    if num == 62:
        coordinate_x = 0
    elif num == 63:
        coordinate_x = 850
    return coordinate_x, coordinate_y


def five_row(num):
    """Подсчет координаты клавиши в пятой строке"""
    coordinate_x = (900 // 13) * (num - 1)
    coordinate_y = 550
    if num == 57:
        coordinate_x = 297
    elif num == 64:
        coordinate_x = 0
    elif num in {68, 69}:
        coordinate_x += 358 if num == 68 else 380
    elif num in {70, 71, 72}:
        coordinate_x += 370
        coordinate_y += 25 if num == 70 or num == 72 else 0
    elif num == 73:
        coordinate_x += 307
        coordinate_y += 25
    return coordinate_x, coordinate_y


def coordinates_counting(num):
    """Подсчет координаты клавиши"""
    if num <= 13 or num == 41 or num == 58:
        coordinate_x, coordinate_y = first_row(num)

    elif num <= 27 or num == 59:
        coordinate_x, coordinate_y = second_row(num)

    elif num <= 43 or num == 60 or num == 61:
        coordinate_x, coordinate_y = third_row(num)

    elif num <= 56 or num == 62 or num == 63:
        coordinate_x, coordinate_y = four_row(num)
    else:
        coordinate_x, coordinate_y = four_row(num)

    return coordinate_x, coordinate_y


def remainder(n, k):
    """Подсчет остатка"""
    if n % k == 0:
        return k
    else:
        return n % k


def skan_codes(code):
    """Возвращение кода клавиши"""
    if code == '\t':
        return dict_codes['Tab']
    elif code == '\r':
        return dict_codes['Return']
    return dict_codes[code]


def value_code(code):
    """Возвращение значения клавиши"""
    if code == 62 or code == 63:
        return 'shift'
    elif code == 68 or code == 67:
        return 'command'
    elif code == 66 or code == 69:
        return 'option'
    elif code == 58:
        return 'delete'
    elif code == 65:
        return 'control'
    return list(dict_codes.keys())[list(dict_codes.values()).index(code)]


def take_text():
    """Открытие текста"""
    with open("texts", "rb") as file:
        line = file.read().decode('utf-8')
        list_texts = line.split("~")
        list_texts = list_texts[::2]
        return random.choice(list_texts)


def place_statistic_name(num):
    """Размещение статистики"""
    if num <= 6:
        return num, 0
    elif num <= 12:
        return (num % 7), 3
    else:
        return None, None


def size_button(num):
    """Подсчет размера клавиши"""
    standard_size = [64, 65, 66, 69]
    if (1 <= num <= 56) or num in standard_size:
        return 60, 50
    elif num == 58 or num == 59:
        return 95, 50
    elif num == 60 or num == 61:
        return 110, 50
    elif num == 62 or num == 63:
        return 140, 50
    elif num == 67 or num == 68:
        return 85, 50
    elif 70 <= num <= 73:
        return 60, 25
    else:
        return 333, 50


def return_shift_key(num):
    """Возвращение кода заглавной буквы"""
    return list(dict_shift.keys())[list(dict_shift.values()).index(num)]
