import os
import re
import shutil
from datetime import datetime

PATH_TO = os.path.dirname(os.path.abspath(__file__))

docs_folder = 'docs'
jpg_folder = 'jpg'
rus_folder = 'RUS'
eng_folder = 'ENG'
archive_folder = 'Archive'

FILE = 'concatenated_file.txt'

spec_symbols = ['"','«', '»', ')', '(']

# doc type patterns
pattern_order_ru = re.compile(r'([З, з]аказ).?')
pattern_treaty_ru = re.compile(r'(ДОГОВОР|договор|Договор)[^у, У]?')
pattern_spec_ru = re.compile(r'([СПЕЦИФИКАЦИЯ|спецификация|Спецификация])')
pattern_letter_ru = re.compile(r'(письм)[а-яА-Я]+')

pattern_order_eng = re.compile(r'([O, o]rder).?')
pattern_treaty_eng = re.compile(r'(agreem)[a-zA-Z]+') # adjust treaty, addendum
pattern_spec_eng = re.compile(r'([S, s]pecif)[a-zA-Z]+') # perhaps adjust
pattern_letter_eng = re.compile(r'[l, L]etter')

pattern_letter_ru_2 = re.compile(r'(Джонат)[а-я]+')
pattern_letter_ru_3 = re.compile(r'([У, у]важаем)[а-я]+')
pattern_letter_ru_4 = re.compile(r'[К, к]уда')
pattern_letter_ru_5 = re.compile(r'[О, о]\s(заказе)')
pattern_letter_ru_6 = re.compile(r'[И, и]сх')
pattern_treaty_ru_2 = re.compile(r'([КОНТРАКТ, контракт])')
pattern_treaty_eng_2 = re.compile(r'([A, a]amendment)')
pattern_treaty_eng_3 = re.compile(r'([A, a]ddendum)')
pattern_letter_eng_2 = re.compile(r'([T, t]o whom it may concern)')

letter_patterns = [pattern_letter_eng, pattern_letter_eng_2, pattern_letter_ru,
                    pattern_letter_ru_2, pattern_letter_ru_3, pattern_letter_ru_4,
                    pattern_letter_ru_5, pattern_letter_ru_6]
treaty_patterns = [pattern_treaty_ru, pattern_treaty_ru_2, pattern_treaty_eng,
                    pattern_treaty_eng_2, pattern_treaty_eng_3]
order_patterns = [pattern_order_ru, pattern_order_eng]
spec_patterns = [pattern_spec_ru, pattern_spec_eng]

# 3d party patterns
pattern_3d_party_ru = re.compile(r'(ООО|ОАО|ЗАО|АО|ПАО|ТОО)([^\,\»,\n,\”]+)(\"\s)?') # adjust
pattern_3d_party_eng = re.compile(r'(OOO|OAO|ZAO|PAO|TOO)([^\,\»,\n,\”]+)(\"\s)?') # no AO

#--------------------------------------------------------- new 3d party
pattern_3d_party_ru_2 = re.compile(r'(ООО|ОАО|ЗАО|АО|ПАО|ТОО|Компания|КОМПАНИЯ).+(именуемое в дальнейшем [\",\«]?Покупатель[\",\»]?)') #adjust
pattern_3d_party_ru_3 = re.compile(r'(от "Покупателя")\s(\w+)')
pattern_3d_party_ru_4 = re.compile(r'(от заказчика)\s(\w+)')
pattern_3d_party_ru_5 = re.compile(r'(для нужд Заказчика)\s(\w+)')
pattern_3d_party_ru_6 = re.compile(r'([П, п]окупатель\s)([^\,\»,\n,\”]+)(\"\s)?')
pattern_3d_party_eng_1 = re.compile(r'([A, a]greement with)\s(\w+)')
pattern_3d_party_eng_2 = re.compile(r'(years \()([^)]+)')
pattern_3d_party_eng_3 = re.compile(r'([CUSTOMER|Customer]\”?\:?\s)([^\,\»,\n,\”]+)(\"\s)?')

party_patterns = [pattern_3d_party_ru_6, pattern_3d_party_eng, pattern_3d_party_ru_2,
                pattern_3d_party_ru_3, pattern_3d_party_ru_4, pattern_3d_party_ru_5,
                pattern_3d_party_ru, pattern_3d_party_eng_1, pattern_3d_party_eng_2,
                pattern_3d_party_eng_3]

# date patterns
pattern_date = re.compile(r'\d{2}[\,,\\,\.]\d{2}[\,,\\.\.]\d{2,4}')
pattern_date_2 = re.compile(r'\d{2}[\",\»]?\s[А-ЯA-Zа-яa-z]{3,10}[^\n]\d{4}') #adjust
pattern_date_3 = re.compile(r'\w+\s+?\d{2}[\,,\\]\s\d{4}')

date_patterns = [pattern_date_2, pattern_date, pattern_date_3]

# pids patterns
pattern_pid = re.compile(r'[A-Z]+-[A-Z]+-\S+')

# correct
def read_file():
    '''
    D - reads concatenated txt
    I - None. Parses relevant dir
    O - text wrapper (text)
    '''
    with open(os.path.join(PATH_TO, docs_folder, FILE), 'r', encoding='UTF8') as file:
        data = file.read()
    return data

def find_doc_type(data):
    '''
    D - parses text with regex via predetermined doc_type pattern
    I - text from read_file func
    O - text or ?
    '''
    doc_type = None
    for pattern in letter_patterns:
        letter = re.findall(pattern, data)
        if letter:
            return 'Письмо'
        else:
            pass
    for pattern in treaty_patterns:
        treaty = re.findall(pattern, data)
        if treaty:
            return 'Договор'
        else:
            pass
    for pattern in spec_patterns:
        spec = re.findall(pattern, data)
        if spec:
            return 'Спецификация'
        else:
            pass
    for pattern in order_patterns:
        order = re.findall(pattern, data)
        if order:
            return 'Заказ'
        else:
            pass

def find_3d_party(data):
    '''
    D - parses text with regex via predetermined 3d party pattern
    I - text from read_file func
    O - text or ?
    '''
    # party_joined = None
    for pattern in party_patterns:
        party = re.search(pattern, data)
        if party:
            party_clean =  party.group(2)
            for i in spec_symbols:
                if i in party_clean:
                    party_clean = party_clean.replace(i, '')
            return party_clean
        else:
            pass
    return 'no 3d party mentioned'

def find_date(data):
    '''
    D - parses text with regex via predetermined date pattern
    I - text from read_file func
    O - text or ?
    '''
    # date = None
    all_dates = []
    for pattern in date_patterns:
        dates = re.findall(pattern, data)
        all_dates.extend(dates)
    if all_dates:
        date =  all_dates[0]
        for i in spec_symbols:
            if i in date:
                date = date.replace(i, '')
        return date
    else:
        return 'no date mentioned'

def find_spec(data):
    '''
    D - parses text with regex via predetermined spec pattern
    I - text from read_file func
    O - text or ?
    '''
    pids = re.findall(pattern_pid, data) # adjust
    return pids

def clean_docs(eoa_file):
    # clean jpg-folder
    jpg_files = os.listdir(os.path.join(PATH_TO, docs_folder, jpg_folder))
    for file in jpg_files:
        os.remove(os.path.join(PATH_TO, docs_folder, jpg_folder, file))
    # clean RUS-folder
    rus_files = os.listdir(os.path.join(PATH_TO, docs_folder, rus_folder))
    for file in rus_files:
        os.remove(os.path.join(PATH_TO, docs_folder, rus_folder, file))
    # remove concatenated_txt
    os.remove(os.path.join(PATH_TO, docs_folder, FILE))
    # move EOA to archive
    shutil.move(os.path.join(PATH_TO, docs_folder, eoa_file),
            os.path.join(PATH_TO, docs_folder, archive_folder, eoa_file))

def eoa_text_parse():
    data = read_file()
    doc_type = find_doc_type(data)
    party = find_3d_party(data)
    date = find_date(data)
    pids = find_spec(data)
    return doc_type, party, date, pids
