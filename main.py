# Напишите программу, с помощью которой можно искать информацию на Википедии с помощью консоли.
# 1. Спрашивать у пользователя первоначальный запрос.
# 2. Переходить по первоначальному запросу в Википедии.
# 3. Предлагать пользователю три варианта действий:
# листать параграфы текущей статьи;
# перейти на одну из связанных страниц — и снова выбор из двух пунктов:
# - листать параграфы статьи;
# - перейти на одну из внутренних статей.
# выйти из программы.

import tkinter as tk
from tkinter import messagebox as infobox

from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


# Для сообщений об ошибках
def warning_box(message_text):
    console = tk.Tk()
    console.withdraw()
    infobox.showwarning(message=message_text)
    console.destroy()


err_state: bool = False
browser: webdriver = webdriver.Chrome()

try:
    browser.get('https://ru.wikipedia.org/wiki/Заглавная_страница')
except WebDriverException:
    err_state = True
    warning_box('Похоже отсутствует Сеть')

# Проверяем по заголовку, если нет выходим из программы
if "Википедия" not in browser.title:
    if not err_state:
        warning_box('Что-то пошло не так: Я не смог открыть википедию')
    browser.quit()

else:

    print('+---------------------------------------------------------------------+')
    print('| Сегодня нам предстоит погружение в пучины Википедии.                |')
    print('| Схема работы такая: Вы спрашиваете, а я ищу информацию в википедии. |')
    print('+---------------------------------------------------------------------+\n')

    while True:

        user_request = input('Что Вы хотите узнать? ')
        search_box = browser.find_element(By.ID, "searchInput")

        if user_request != '':
            search_box.send_keys(user_request)
            search_box.send_keys(Keys.RETURN)
            break

    print('+---------------------------------------------------------------------+')
    print('| Сейчас вы можете:                                                   |')
    print('+---------------------------------------------------------------------+')
    print('| 1. Листать параграфы текущей статьи;                                |')
    print('| 2. Перейти на одну из связанных страниц.                            |')
    print('+---------------------------------------------------------------------+\n')

    user_request = input('Выберите (1/2): ')

    if user_request == '1':
        print('\nДля показа следующего параграфа нажмите любую клавишу\n')

        paragraphs = browser.find_elements(By.TAG_NAME, "p")
        for paragraph in paragraphs:
            print(paragraph.text, end='')
            input('')

    elif user_request == '2':
        print()

        rel_pages = []
        for element in browser.find_elements(By.TAG_NAME, "div")
        # Чтобы искать атрибут класса
        cl = element.get.attribute("class")
        if cl == "hatnote navigation-not-searchable":
            hatnotes.append(element)

        print(hatnotes)
        hatnote = random.choice(hatnotes)

        # Для получения ссылки мы должны найти на сайте тег "a" внутри тега "div"
        link = hatnote.find_element(By.TAG_NAME, "a").get.attribute("href")
        browser.get(link)