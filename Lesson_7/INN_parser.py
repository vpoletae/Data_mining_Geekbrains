from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import os
import re

# Задача: Есть несколько сотен тысяч наименований компаний.
#         Необходимо для каждого найти ИНН
# На входе: Есть массив данных, который предварительно "нарезан" на
#           более мелкие txt файлы. Подаются на вход в цикле
# На выходе: Файлы с найденными ИНН записываются в отдельную папку
# Принцип: Эмулируется работа поисковых запросов в Яндекс (или Гугл)
#          ИНН выхватывается из описания под ссылкой в поисковой выдаче
#          Анализируются первые 3 ссылки (на предмет наличия ИНН) - refs_count
# Замечания: Дополнительно все данные выводятся на печать (вместе с ошибками)
#            В силу относительной простоты кода функционал оформлен в одном цикле
#            На перспективу, скорее всего, объединю в пакет вместе с этапами
#            препроцессинга и последующего анализа (перепишу под возможный импорт)
#            обход бана обходится через time.sleep()

web_path = 'https://yandex.ru/search/?lr=213&text='
#web_path = 'https://www.google.ru/search?newwindow=1&sxsrf=ACYBGNQ9Kkz6tZVvFEi8Of8XB1FhNHvzIQ%3A1570430365400&ei=nd2aXdmQGMbKwAKM-Y-wDA&q='

driver_path_chrome = 'chromedriver.exe'
PATH_FROM = 'from'
PATH_TO = 'to'

refs_count = 3
stop_word = re.compile('ИНН.+?\d+')
search_criteria = ' ИНН'

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(driver_path_chrome, chrome_options=options)

files_to_scrap = os.listdir(PATH_FROM)
counter = 1

for file in files_to_scrap:
      text_list = []
      with open(os.path.join(PATH_FROM, file), 'r', encoding='UTF-8') as file:
            file_lines = len(file.readlines())
            file.seek(0)
            for i in range(file_lines):
                  company = file.readline().strip()
                  driver.get(web_path + (company + search_criteria))
                  for i in range(refs_count):
                        try:
                              drv_obj = driver.find_element_by_xpath(
                                    "//li[@class='serp-item'][@data-cid={0}] \
                                    /div/h2[@class='organic__title-wrapper typo typo_text_l typo_line_m']".format(i))
                              text_value = drv_obj.text
                              if len(re.findall(stop_word, text_value.upper())) != 0:
                                    text_list.append(company + '::' + text_value)
                                    print(company + '::' + text_value)
                                    break
                              else:
                                    pass
                        except NoSuchElementException:
                              print('Selenium error occured!')
                              continue
                        except ConnectionAbortedError:
                              print('Connection error occured!')
                              continue
                        except TimeoutException:
                              print('Timeout error occured!')
                              continue

            with open(os.path.join(PATH_TO, f'cut_{counter}.txt'), 'w', encoding='UTF-8') as f:
                  for i in text_list:
                        f.write(i + '\n')
            counter += 1
driver.quit()
