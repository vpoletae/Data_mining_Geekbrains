import os
import re
import shutil
from pprint import pprint

PATH_TO = os.path.dirname(os.path.abspath(__file__))

FILE = 'concatenated_file.txt'

CAP_RUS = ['А','Б','В','Г','Д','Е','Ё','Ж','З','И',
            'Й','К','Л','М','Н','О','П','Р','С','Т',
            'У','Ф','Х','Ц','Ч','Ш','Щ','Ъ','Ы','Ь',
            'Э','Ю','Я',]

LATYN = ['a','b','c','d','e','f','g','h',
        'i','j','k','l','m','n','o','p',
        'q','r','s','t','u','v','w','x',
        'y','z']

SPEC_SYMBOLS = ['.', ',', '(', ')', '|']

TRASH_LIST = ['The', 'Placing', 'Мутагвее', 'т', 'оп', 'ад']

METRICS = ['Клики', 'Показы'] #add
texts = []
text = 0
with open(os.path.join(PATH_TO, FILE), 'r', encoding='UTF8') as f:
    for line in f:
        if line[0] in CAP_RUS:
            texts.append(text)
            text = line.strip()
        else:
            text = text + ' ' + line.strip()
    else:
        pass

services = texts[1:]
services_clean = []
all_digits = []
all_metrics = []
for service in services:
    clean = []
    digits = []
    metrics = []
    duplicates = []
    service_list = service.split(' ')
    for word in service_list:
        if word:
            if word[0] in LATYN:
                pass
            elif word[0].isdigit() == True and word[-1].isdigit() == True:
                if word in digits:
                    pass
                else:
                    digits.append(word)
            elif word in SPEC_SYMBOLS or word in TRASH_LIST or word[0] in SPEC_SYMBOLS:
                pass
            elif word in METRICS:
                metrics.append(word)
            else:
                if word in duplicates:
                    pass
                else:
                    duplicates.append(word)
                    clean.append(word)
        else:
            pass
    clean_text = ' '.join(clean)
    all_digits.append(digits)
    all_metrics.append(metrics)
    services_clean.append(clean_text)

for i in services_clean:
    print(i)
for i in all_digits:
    print(i)
for i in all_metrics:
    print(i)
