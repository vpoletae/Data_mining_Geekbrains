import pyautogui
import time
import os

# создать отдельную папку с доп. соглашениями
# открыть STDU Viewer
# пробежаться в цикле и для каждого документа
#     создать релевантную папку для jpeg
#     загрузить в STDU
#     экспортировать img в релевантную папку
#
# Для каждой папки img
#     Для каждого файла в папке
#         Через tesseract конвертировать в txt
#     Объединить все локальные txt в concatenated.txt
#
# Создать и открыть xls-файл
# Для каждого concatenated-файла:
#     Получить контрагента
#     Получить дату
#     Получить название мероприятия
#     Получить сумму итогу
#     Получить детализацию по смете
#     Записать в xls в строку данные с одного файла
jpgs_folder = r'C:\Users\vpoletae\Desktop\Rusprogramms_data_mining\jpg'
path_to_addendums = r'C:\Old_laptop_data_migration\RUSPROGRAMMS\Addendums'

STDU_VIEWER = (494, 544)
IMPORT_FILE = (1180, 553)
FILE_ENTER = (1426, 999)

FILE_BUTTON = (34, 52)
OPEN_BUTTON = (53, 79)
EXPORT_BUTTON = (87, 450)
TO_IMAGE_BUTTON = (626, 449)
OK_BUTTON = (1148, 697)

# a, b = pyautogui.size()
# x, y = pyautogui.position()
# print(x, y)

# pyautogui.click(STDU_VIEWER)
# pyautogui.click(STDU_VIEWER)
# time.sleep(1)
# pyautogui.click(IMPORT_FILE)
# pyautogui.click(IMPORT_FILE)
# time.sleep(1)

addendums = os.listdir(path_to_addendums)
for add in addendums:
    print(os.path.abspath(add))
# pyautogui.click(FILE_ENTER)
# pyautogui.typewrite('RUSPROGGRAMS')

# addendums = os.listdir()
# for add in addendums:
#     os.mkdir(path)
#     file_path = os.path.abspath(add)
