import os
import re
import shutil

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

services_detailed = re.compile(r'((ИТОГО|Итого).+(USD|RUB))(.+)(ИТОГО|Итого)')

def read_file():
    texts = []
    text = 0
    with open(os.path.join(PATH_TO, FILE), 'r', encoding='UTF8') as file:
        data = file.read()
        result = re.search(services_detailed, data)
        if result:
            services_full = result.group(1)
            for line in services_full:
                if line[0] in CAP_RUS:
                    texts.append(text)
                    text = line.strip()
                else:
                    text = text + ' ' + line.strip()
        else:
            print('+'*60)
            print(result)
            print('+'*60)
    return texts

def extract_services_metrics_figures(texts):
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
    return services_clean
    # return services_clean, all_digits, all_metrics
# data = read_file()

# place = re.complile(r'(место).*(услуги):\s*.{20}')'
# total_price
# party
# date
# services
