import json
import time

import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver


def finder(url):
    """Это функция поиска информации(и проверки на соответствие) по ссылке передаваемой с главной страницы"""
    global spans_tag, td_list, soup, matches, money_result
    global vacancies
    
    try:
        driver = webdriver.Chrome()  # Открываем Firefox
        driver.maximize_window()
        driver.get(url)  # Открываем страницу
        time.sleep(3)  # пауза на прогрузку страницы

        soup = BeautifulSoup(driver.page_source, 'html.parser')  # Получаем готовый html и парсим его
        td_list = soup.find('div', class_='g-user-content')  # Получаем описание вакансии(обязанности и требования)
        try:
            spans_tag = td_list.find_all('span', class_='')
        except Exception as e:
            print(f"{e}")
    except Exception as e:
        print(f'We have problrm,not connect new page to parse: {e}')

    try:

        for text in spans_tag:
            pattern = re.compile(r'\b(Django|Flask)\b', re.IGNORECASE)  #Linux - для тестов использовал,больше вариантов
            try:
                matches = pattern.findall(str(text))

            except Exception as e:
                print(f'Ошибка с ключевыми словами: {e} ')

            if matches:
                template = {}   #словарь со значениями
                print("Найденные ключевые слова:", matches)
                new_url = url
                template['url'] = new_url
                #print(new_url)   # 'link': url,

                money = ((soup.find('div', class_='vacancy-title').find('span','bloko-header-section-2 bloko-header-section-2_lite')))
                try:
                    if money is None:
                        money_result = f'Vacance don`t show prace'
                        template['cash'] = money_result
                    else:
                        money_result = money.text
                        template['cash'] = money_result
                except Exception as e:
                    print(f'Vacanci don`t have price|money')

                name_company = ((soup.find('div', class_='wrapper--FVo3cUofDgv3zkHBdMP1').find('a','bloko-link bloko-link_kind-tertiary')))    # 'name_company'
                try:
                    name_company_result = name_company.text
                    template['name_company'] = name_company_result
                except Exception as e:
                    name_company_result = f'Company no name'
                    template['name_company'] = name_company_result

                company_city = ((soup.find('div', class_='wrapper--FVo3cUofDgv3zkHBdMP1').find('a','bloko-link bloko-link_kind-tertiary bloko-link_disable-visited')))
                try:
                    company_city_result = company_city.text   # 'city'
                    template['city'] = company_city_result
                except Exception as e:
                    company_city_result = f'Company don`t show address'
                    template['city'] = company_city_result

                #json информацию о каждой вакансии - ссылка, вилка зп, название компании, город.


                if matches :    #если у нас файл существует,то
                    file = {'work': [{}]}
                    try:
                        with open("data.json", encoding='utf-8') as json_file:  # читаем  файл
                            data = json.load(json_file)  # заганяем данные в файл
                            data['work'].append(template)
                            with open('data.json', 'w', encoding='utf-8') as outfile:
                                json.dump(data, outfile, ensure_ascii=False, indent=4)
                        print('try')
                    except Exception as e:
                        with open("data.json", "a+", encoding='utf-8') as json_file:
                            #print(json.dumps(file, ensure_ascii=False, indent=4))  #показать что пишем в первый раз
                            json.dump(file, json_file, ensure_ascii=False, indent=4)
                        print('except')


                #очистить переменную перед выходом
                template.clear()
            else:
                continue


    except Exception as e:
        print(f'problem to parse tag :{e}')

