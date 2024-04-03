import random

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


def coordinates_counting(num):
    if num <= 13 or num == 41:
        coordinate_y = 400
        coordinate_x = (900 // 13) * (remainder(num, 13) - 1)
        if num == 41:
            coordinate_x = 23

    elif num <= 27:
        coordinate_y = 450
        coordinate_x = (900 // 13) * (remainder(num, 14) - 2)

    elif num <= 43 and num != 41:
        coordinate_y = 500
        coordinate_x = (900 // 13) * (remainder(num, 29))
        if num == 43:
            coordinate_x = (900 // 13) * 12

    else:
        coordinate_y = 550
        coordinate_x = (900 // 13) * (remainder(num, 43))
        if num == 57:
            coordinate_y = 600
            coordinate_x = 400
    return coordinate_x, coordinate_y


def remainder(n, k):
    if n % k == 0:
        return k
    else:
        return n % k


def skan_codes(code):
    return dict_codes[code]


def value_code(code):
    return list(dict_codes.keys())[list(dict_codes.values()).index(code)]

def take_text():
    with open("texts", "rb") as file:
        line = file.read().decode('utf-8')
        list_texts = line.split("~")
        list_texts = list_texts[::2]
        return random.choice(list_texts)
