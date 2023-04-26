""" Модуль реализует функционал Telegram чат-бота, сообщающего погоду в заданном городе.
Погодные условия запрашиваются с сайта OpenWeatherMap.org по API"""

import json
import time
import os
import asyncio
from typing import Tuple
from aiohttp import ClientSession

from const import ADMIN_ID, OWM_URL, TGRAM_URL, LAST_UPDATE_ID_FILE, COMMANDS


async def get_messages() -> dict:
    """ Получает список сообщений с сервера Telegram за последние 24 часа
    Returns:
        dict - словарь с последними сообщениями в чат-боте"""
    async with ClientSession() as session:
        url = TGRAM_URL.format(method='getUpdates')
        async with session.get(url=url) as response:
            messages = await response.text()
    return json.loads(messages)


async def get_weather(city: str) -> Tuple[str, dict]:
    """ Получает текущую погоду для заданного города с сервера OpenWeatherMap.org с помощью API
    Arguments:
        city: str - запрашиваемый город
    Returns:
        str - запрашиваемый город
        dict - погодные условия в запрашиваемом городе"""
    async with ClientSession() as session:
        url = OWM_URL.format(city=city)
        async with session.get(url=url) as response:
            weather = await response.text()
    return city, json.loads(weather)


async def send_message(params: dict) -> str:
    """ Посылает пользователю сообщение в Telegram с ответом на запрос погоды в заданном городе
    Arguments:
        params: dict - текст пункта меню с номером
    Returns:
        str - служебное сообщение чат-бота на ответ пользователю"""
    async with ClientSession() as session:
        url = TGRAM_URL.format(method='sendMessage')
        async with session.get(url=url, params=params) as response:
            result = await response.text()
    return result


async def main():
    """ Основная функция, которая реализует функционал Telegram чат-бота, сообщающего погоду в заданном городе"""

    # Считываем из файла ID последнего обработанного сообщения
    last_update_id = 0
    if os.path.exists(LAST_UPDATE_ID_FILE):
        with open(LAST_UPDATE_ID_FILE, encoding='utf-8') as file:
            data = file.readline()
            if data:
                last_update_id = int(data)
    last_update_id_old = last_update_id

    turn_on = True
    while turn_on:
        # Получаем на сервере Telegram все сообщения, оставленные за последние 24 часа,
        # просматриваем их в хронологическом порядке и добавляем в список сообщений для обработки те из них,
        # у которых update_id больше, чем last_update_id
        tasks = [asyncio.create_task(get_messages())]
        messages = await asyncio.gather(*tasks)
        mess_queue = []
        for current_message in messages[0].get('result'):
            if current_message.get('update_id') > last_update_id:
                mess_queue.append(current_message)

        # Получаем текст сообщения и, если это не служебная команда, добавляем в множество запрошенных городов
        cities = set()
        for mess in mess_queue:
            text = mess.get('message').get('text')
            if not COMMANDS.get(text):
                cities.add(text)

        # Получаем погоду с OpenWeatherMap.org для всех городов из множества
        weather = {}
        if cities:
            tasks.clear()
            for city in cities:
                tasks.append(asyncio.create_task(get_weather(city)))
            weather = dict(await asyncio.gather(*tasks))

        # Формируем ответы на сообщения из списка новых сообщений
        response_data = []
        for mess in mess_queue:
            # Получаем необходимые параметры сообщения
            chat_id = mess.get('message').get('chat').get('id')
            text = mess.get('message').get('text')
            last_update_id = mess.get('update_id')
            user_id = mess.get('message').get('from').get('id')

            # Формируем ответ на сообщение
            current_response = {'chat_id': chat_id,
                                'user_id': user_id}
            if COMMANDS.get(text):
                if text == '/turnoff':
                    if str(user_id) == ADMIN_ID:
                        turn_on = False
                        current_response['text'] = 'Чат-бот выключен'
                    else:
                        current_response['text'] = 'Извините, у Вас нет прав администратора'
                else:
                    current_response['text'] = COMMANDS.get(text)
            else:
                city_weather = weather.get(text)
                if city_weather.get('cod') == 200:
                    current_response['text'] = f'--->  {city_weather.get("name")}, ' \
                                               + f'{city_weather.get("sys").get("country")},  ' \
                                               + f'широта: {city_weather.get("coord").get("lat")}, ' \
                                               + f'долгота: {city_weather.get("coord").get("lon")}\n' \
                                               + str(city_weather.get("weather")[0].get("description")).capitalize() \
                                               + f'\nТемпература: {city_weather.get("main").get("temp")} С\n' \
                                               + f'Давление: {city_weather.get("main").get("pressure")} мбар\n' \
                                               + f'Облачность: {list(city_weather.get("clouds").values())[0]} %\n' \
                                               + f'Ветер: скорость {city_weather.get("wind").get("speed")} м/с, ' \
                                               + f'направление {city_weather.get("wind").get("deg")} градусов'
                if city_weather.get('cod') == '404':
                    current_response['text'] = f'Ошибка {city_weather.get("cod")}: ' \
                                               + f'{city_weather.get("message")} (город не найден)\n' \
                                               + 'Введите название города'
                if city_weather.get('cod') not in [200, 404, '404']:
                    current_response['text'] = f'Ошибка сети, код: {city_weather.get("cod")}\n' \
                                               + 'Попробуйте сделать запрос позже'
            response_data.append(current_response)

        # Отправляем пользователям ответы на сообщения
        if response_data:
            tasks.clear()
            for current_data in response_data:
                tasks.append(asyncio.create_task(send_message(current_data)))
            await asyncio.gather(*tasks)

        # Записываем в файл Update_ID последнего сообщения
        if last_update_id > last_update_id_old:
            with open(LAST_UPDATE_ID_FILE, 'w', encoding='utf-8') as file:
                file.write(str(last_update_id))
            last_update_id_old = last_update_id

        time.sleep(0.5)


if __name__ == "__main__":
    asyncio.run(main())
