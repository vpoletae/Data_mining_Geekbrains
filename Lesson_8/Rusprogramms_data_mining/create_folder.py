import os
import shutil

addendums_folder = r'C:\Old_laptop_data_migration\RUSPROGRAMMS\Addendums'
liza_folder = r'C:\Old_laptop_data_migration\RUSPROGRAMMS\Liza_folder'
tania_folder = r'C:\Old_laptop_data_migration\RUSPROGRAMMS\Tania_folder'

liza_docs = os.listdir(liza_folder)
for doc in liza_docs:
    if 'addendum' in doc.lower():
        shutil.move(os.path.join(liza_folder, doc),
                    os.path.join(addendums_folder, doc))

for d, dirs, files in os.walk(tania_folder):
    for doc in files:
        if 'addendum' in doc.lower() and doc.endswith('pdf') and 'act' not in doc.lower() and 'amendment' not in doc.lower():
        	path_from = os.path.join(d,doc)
        	shutil.move(os.path.join(path_from),
                        os.path.join(addendums_folder, doc))
