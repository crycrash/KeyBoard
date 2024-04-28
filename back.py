import random

dict_codes = {"1": 2, "2": 3, "3": 4, "4": 5, "5": 6,
              "6": 7, "7": 8, "8": 9, "9": 10, "0": 11,
              "-": 12, "=": 13, "й": 16,
              "ц": 17, "у": 18, "к": 19, "е": 20, "н": 21,
              "г": 22, "ш": 23, "щ": 24, "з": 25, "х": 26,
              "ъ": 27, "ф": 30, "ы": 31, "в": 32, "а": 33,
              "п": 34, "р": 35, "о": 36, "л": 37, "д": 38,
              "ж": 39, "э": 40, "ё": 41, "'\'": 43, "я": 44,
              "ч": 45, "с": 46, "м": 47, "и": 48, "т": 49,
              "ь": 50, "б": 51, "ю": 52, ".": 53, " ": 57,
              'Back_Space': 58, 'Tab': 59, 'Caps_Lock': 60,
              'Return': 61, 'Shift_L': 62, 'Shift_R': 63,
              'fn': 64, 'Control_L': 65, 'Alt_L': 66,
              'Win_L': 67, 'Win_R': 68, 'Alt_R': 69, 'Left': 70,
              'Up': 71, 'Down': 72, 'Right': 73, "!": 2, "'": 3, "№": 4, ";": 5, "%": 6,
              ":": 7, "?": 8, "*": 9, "(": 10, ")": 11,
              "_": 12, "+": 13,"/": 43, ",": 53, '\n':61}

dict_shift = {"!": 2, "'": 3, "№": 4, ";": 5, "%": 6,
              ":": 7, "?": 8, "*": 9, "(": 10, ")": 11,
              "_": 12, "+": 13, "Й": 16,
              "Ц": 17, "У": 18, "К": 19, "Е": 20, "Н": 21,
              "Г": 22, "Ш": 23, "Щ": 24, "З": 25, "Х": 26,
              "Ъ": 27, "Ф": 30, "Ы": 31, "В": 32, "А": 33,
              "П": 34, "Р": 35, "О": 36, "Л": 37, "Д": 38,
              "Ж": 39, "Э": 40, "Ё": 41, "/": 43, "Я": 44,
              "Ч": 45, "С": 46, "М": 47, "И": 48, "Т": 49,
              "Ь": 50, "Б": 51, "Ю": 52, ",": 53}


def coordinates_counting(num):
    """Подсчет координаты клавиши(ПЕРЕДЕЛАТЬ)"""
    if num <= 13 or num == 41 or num == 58:
        coordinate_y = 350
        coordinate_x = (900 // 13) * (remainder(num, 13) - 1)
        if num == 41:
            coordinate_x = 0
        if num == 58:
            coordinate_x = 897

    elif num <= 27 or num == 59:
        coordinate_y = 400
        coordinate_x = (900 // 13) * (remainder(num, 14) - 2) + 105
        if num == 59:
            coordinate_x = 0

    elif (num <= 43 and num != 41) or num == 60 or num == 61:
        coordinate_y = 450
        coordinate_x = (900 // 13) * (remainder(num, 29)) + 45
        if num == 43:
            coordinate_y = 400
            coordinate_x = (900 // 13) * 12 + 105
        elif num == 60:
            coordinate_x = 0
        elif num == 61:
            coordinate_x = 880

    elif num <= 56 or num == 62 or num == 63:
        coordinate_y = 500
        coordinate_x = (900 // 13) * (remainder(num, 43)) + 75
        if num == 62:
            coordinate_x = 0
        if num == 63:
            coordinate_x = 850
    else:
        coordinate_x = (900 // 13) * (remainder(num, 64))
        coordinate_y = 550
        if num == 57:
            coordinate_x = 297
        if num == 64:
            coordinate_x = 0
        if num == 68:
            coordinate_x += 358
        if num == 69:
            coordinate_x += 380
        if num == 70:
            coordinate_x += 370
            coordinate_y += 25
        if num == 71:
            coordinate_x += 370
        if num == 72:
            coordinate_x += 302
            coordinate_y += 25
        if num == 73:
            coordinate_x += 307
            coordinate_y += 25

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
    return list(dict_shift.keys())[list(dict_shift.values()).index(num)]


def return_shift_name(key):
    return dict_shift[key]
