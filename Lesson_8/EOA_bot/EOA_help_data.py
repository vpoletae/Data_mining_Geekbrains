import os
import pandas as pd
from collections import defaultdict
import difflib
from difflib import SequenceMatcher
import transliterate

PATH = os.path.dirname(os.path.abspath(__file__))
FILE = 'EOA_bookings.xlsx'

LATYN = ['a','b','c','d','e','f','g','h',
        'i','j','k','l','m','n','o','p',
        'q','r','s','t','u','v','w','x',
        'y','z']

def create_df():
    '''
    D - creates df from initial excel db, dropna, remove UNKNOWN
    I - xlsx
    O - dataframe
    '''
    df = pd.read_excel(os.path.join(PATH, FILE))
    df_upd = df.dropna(axis='index', how='any', subset=['ERP Deal ID'])
    df_upd = df_upd[df_upd['ERP Deal ID'] != 'UNKNOWN']
    df_upd.reset_index(inplace=True)
    return df_upd

# accounts_unique = df_upd['End Customer Site Name'].unique() #?

def create_did_party_pids_dict(df_upd):
    '''
    D - converts df to a {(did, party):[pids]}
    I - df
    O - dict
    '''
    did_party_pids_dict = defaultdict(list)
    for index in range(df_upd.shape[0]):
        did = df_upd.loc[index, 'ERP Deal ID']
        party = df_upd.loc[index, 'End Customer Site Name']
        pid = df_upd.loc[index, 'Product ID']
        did_party_pids_dict[(did, party)].append(pid)
    return did_party_pids_dict

def count_similarity(x, word):
    '''
    D - counts Damerau-Levenstein distance
    I - str
    O - str
    '''
    return round(SequenceMatcher(None, str(x).lower(), str(word).lower()).ratio(), 2)

def create_accounts_dates_df(df_upd):
    '''
    D - creates df of unique accounts and dates of bookings
    I - df
    O - df
    '''
    accounts_dates = df_upd[['End Customer Site Name', 'Date Booked']].drop_duplicates()
    accounts_dates.reset_index(inplace=True)
    return accounts_dates

def find_the_closest(accounts, word):
    '''
    D - finds an account from accounts_df with the highest similarity ratio
    I - df, str
    O - df
    '''
    accounts['Ratio'] = accounts['End Customer Site Name'].apply(lambda x: count_similarity(x, word))
    the_closest_account_date_df = accounts.sort_values(by='Ratio', ascending=False)[['End Customer Site Name', 'Date Booked', 'Ratio']]
    the_closest_account_date_df.reset_index(inplace=True)
    the_closest_account = the_closest_account_date_df.loc[0, 'End Customer Site Name']
    the_closest_date = the_closest_account_date_df.loc[0, 'Date Booked']
    the_closest_ratio = str(float(the_closest_account_date_df.loc[0, 'Ratio']) * 100) + '%'
    return the_closest_account, the_closest_date, the_closest_ratio

def translate(name):
    '''
    D - transliterate company name if written in Russian
    I - str
    O - str
    '''
    if name[0].lower() in LATYN or name[-2].lower() in LATYN: # checks first and random symbol
        translated = name
    else:
        translated = transliterate.translit(name, reversed=True)
    return translated
