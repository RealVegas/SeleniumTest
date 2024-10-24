# Напишите программу, с помощью которой можно искать информацию на Википедии с помощью консоли.
# 1. Спрашивать у пользователя первоначальный запрос.
# 2. Переходить по первоначальному запросу в Википедии.
# 3. Предлагать пользователю три варианта действий:
# листать параграфы текущей статьи;
# перейти на одну из связанных страниц — и снова выбор из двух пунктов:
# - листать параграфы статьи;
# - перейти на одну из внутренних статей.
# выйти из программы.

import keyboard
import tkinter as tk
from tkinter import messagebox as infobox

from random import choice

from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


# Для сообщений об ошибках
def warning_box(message_text):
    console: tk = tk.Tk()
    console.withdraw()
    infobox.showwarning(message=message_text)
    console.destroy()

def upper_level():

    err_upper: bool = False

    try:
        browser.get('https://ru.wikipedia.org/wiki/Заглавная_страница')
    except WebDriverException:
        err_upper: bool = True
        warning_box('Похоже отсутствует Сеть')

    # Проверяем по заголовку, если нет выходим из программы
    if "Википедия" not in browser.title:
        if not err_upper:
            warning_box('Что-то пошло не так: Я не смог открыть википедию')
        browser.quit()

    print('\n+---------------------------------------------------------------------+')
    print('| Похоже там больше не было связанных страниц.                        |')
    print('| Давайте опять поищем что-нибудь интересное                          |')
    print('+---------------------------------------------------------------------+\n')

    while True:

        new_request: str = input('Что еще Вы хотите узнать? ')
        new_search: browser = browser.find_element(By.ID, "searchInput")

        if user_request != '':
            new_search.send_keys(user_request)
            new_search.send_keys(Keys.RETURN)
            option_one()


# При выборе опции 1
def option_one():

    print('\n+---------------------------------------------------------------------+')
    print('| Сейчас вы можете:                                                   |')
    print('+---------------------------------------------------------------------+')
    print('| 1. Листать страницы текущей статьи;                                 |')
    print('| 2. Перейти на одну из связанных страниц.                            |')
    print('| 3. Завершить работу.                                                |')
    print('+---------------------------------------------------------------------+\n')

    sel_request: str = input('Выберите (1/2): ')

    if sel_request == '1':

        print('\b+---------------------------------------------------------------------+')
        print('| Для прокрутки страницы вниз нажимайте любую клавишу                 |')
        print('| Введенные символы будут отображаться (я не могу отключить ввод)     |')
        print('| Опция 2 доступна в любой момент                                     |')
        print('+---------------------------------------------------------------------+\n')

        curr_url = browser.current_url
        body: webdriver = browser.find_element(By.TAG_NAME, 'body')

        while True:

            event = keyboard.read_event()

            if event.event_type == keyboard.KEY_DOWN:
                body.send_keys(Keys.PAGE_DOWN)
                if event.name == '2':
                    option_two()

    elif sel_request == '2':
        option_two()

    else:
        exit()


# При выборе опции 2
def option_two():

    print()

    # Список связанных страниц
    rel_pages = []

    # Перебор тегов div
    for div_tag in browser.find_elements(By.TAG_NAME, 'div'):
        # Ищем атрибут класса
        class_attr = div_tag.get_attribute('class')
        if class_attr == 'mw-search-result-heading':
            rel_pages.append(div_tag)

    # Выбор случайной страницы
    if len(rel_pages) == 0:
        upper_level()
    elif len(rel_pages) > 1:
        random_page = choice(rel_pages)
    else:
        random_page = rel_pages[0]

    # Переход к связанной странице
    page_link = random_page.find_element(By.TAG_NAME, 'a').get_attribute('href')
    browser.get(page_link)

    option_one()


# Основная программа
err_state: bool = False
browser: webdriver = webdriver.Chrome()

try:
    browser.get('https://ru.wikipedia.org/wiki/Заглавная_страница')
except WebDriverException:
    err_state: bool = True
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

        user_request: str = input('Что Вы хотите узнать? ')
        search_box = browser.find_element(By.ID, "searchInput")

        if user_request != '':
            search_box.send_keys(user_request)
            search_box.send_keys(Keys.RETURN)
            option_one()