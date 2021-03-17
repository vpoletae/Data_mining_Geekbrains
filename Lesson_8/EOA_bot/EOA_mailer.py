import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from datetime import datetime
import os

PATH_TO = os.path.dirname(os.path.abspath(__file__))
docs_folder = 'docs'
archive_folder = 'Archive'

def create_head():
    today = datetime.strftime(datetime.date(datetime.today()), '%d %m %Y')
    send_from = '' #fill
    send_to_list = ['', ''] #fill
    subject = f'EOA отчёт {today}'
    return send_from, send_to_list, subject

def create_body(sender, email, doc_type, eoa_date, file_date,
                eoa_party, file_party, the_closest_ratio, ratio):
    text = '''Добрый день!

Ниже представлен отчёт по результатам анализа EOA:

    Отправитель: {0}
    E-mail: {1}
    ________________________________________________
    Тип документа: {2}
    Дата (EOA): {3}
    Дата уведомления: {4}
    Контрагент (EOA): {5}
    Контрагент (проверяемый): {6}
    Точность совпадения (%): {7}
    % совпадения заказа: {8}
    ------------------------------------------------

Исходный pdf-файл во вложении

Спасибо!
    '''.format(sender, email, doc_type, eoa_date, file_date,
                eoa_party, file_party, the_closest_ratio, ratio)
    return text

def send_mail(send_to_list, subject, send_from, text, eoa_file):
    COMMASPACE = ', '
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to_list)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    attachment = MIMEBase('application', "octet-stream")
    attachment.set_payload(open(os.path.join(PATH_TO, docs_folder,
                                archive_folder, eoa_file), "rb").read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment', filename=eoa_file)
    msg.attach(attachment)

    smtp = smtplib.SMTP('', 25) #fill
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()
