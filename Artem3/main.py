import time

if __name__ == "__main__":
    import requests
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    import json
    from bloknot import url
    from finder import finder


    def connect(url):
        """Проверяет доступность для работы сраницы и выводит  responce"""
        headers = {'User-Agent': 'HH-User-Agent'}  # по условиям использования API HH.ru иначе бедет 404
        response = requests.get(url, headers=headers)  # headers
        return response

    try:
        if connect(url).status_code == 200:
            try:
                driver = webdriver.Chrome()  # Открываем Firefox
                driver.maximize_window()
                driver.get(url)  # Открываем страницу
                time.sleep(2)  # пауза на прогрузку страницы

                # парсим страницу для уточнения статуса по инн
                soup = BeautifulSoup(driver.page_source, 'html.parser')  # Получаем готовый html и парсим его
                td_list = soup.find_all('a', class_='serp-item__title')  # Получаем список кнопок на отклик
                for link in td_list:    #list button tag vacancies at 1 page
                    #print(link.get('href')) #take all links href
                    finder(link.get('href'))    #передаем в следующую функцию для перехода на страницу и проверку по соответствию условиям

            except Exception as e:
                print(f'Error to open browser: {e}')
        else:
            print(f'we have problem')
    except Exception as e:
        print(f'The problem is: {e}')

