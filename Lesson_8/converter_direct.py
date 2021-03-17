import PyPDF2
import os
import re

PATH = r'C:\Users\vpoletae\Desktop\customs_pdf_extractor'
invoices_templates = 'direct'

files = os.listdir(os.path.join(PATH, invoices_templates))

pdf_files = []
for file in files:
    if file.endswith('pdf'):
        pdf_files.append(file)

print(len(pdf_files))

with open('invoices_direct.txt', 'a', encoding='UTF8') as f:
    for file in pdf_files:
        pl = open(os.path.join(PATH, invoices_templates, file), 'rb')
        plread = PyPDF2.PdfFileReader(pl)

        for page in range(plread.numPages):
            page_text = plread.getPage(page)
            text = page_text.extractText()
            f.write(text)

with open('invoices_direct.txt', 'r', encoding='UTF8') as f:
    text = f.read()

pattern = re.compile(r'[A-Z]{3}\d{4}\w+')
sn_invoices = pattern.findall(text)

print(len(sn_invoices))
print(sn_invoices[:10])

with open('to_check.txt', 'r', encoding='UTF8') as f:
    sns = f.readlines()

to_check_list = []
for sn in sns:
    to_check_list.append(sn.strip())

to_check_list_set = set(to_check_list)
invoices_clean_set = set(sn_invoices)

intersected = invoices_clean_set.intersection(to_check_list_set)
print(intersected)

intersected_list = list(intersected)
with open('intersected_direct.txt', 'w', encoding='UTF8') as f:
    f.writelines(intersected_list)
