import json
import requests
import time
import os
from pprint import pprint
from const import *


def main():
    # Считываем из файла ID последнего обработанного сообщения
    last_update_id = 0
    if os.path.exists(LAST_UPDATE_ID_FILE):
        with open(LAST_UPDATE_ID_FILE) as file:
            data = file.readline()
            if data:
                last_update_id = int(data)

    # Получаем на сервере Telegram все сообщения, оставленные за последние 24 часа
    url = TGRAM_URL.format(method='getUpdates')
    response = requests.get(url)
    json_data = json.loads(response.text)

    pprint(json_data)

    # Просматриваем сообщения в хронологическом порядке и обрабатываем те, у которых Update_ID больше,
    # чем ID последнего обработанного сообщения
    message_data = dict()
    for item in json_data.get('result'):
        if last_update_id < item.get('update_id'):

            # Получаем необходимые параметры сообщения
            chat_id = item.get('message').get('chat').get('id')
            text = item.get('message').get('text')
            last_update_id = item.get('update_id')

            # Записываем в файл Update_ID текущего сообщения
            with open(LAST_UPDATE_ID_FILE, 'w') as file:
                file.write(str(last_update_id))

            print(chat_id, text, last_update_id)

            # Формируем ответ на сообщение
            message_data['chat_id'] = chat_id
            if COMMANDS.get(text):
                message_data['text'] = COMMANDS[text]
            else:
                url = OWM_URL.format(city=text)
                response = requests.get(url)
                json_data = json.loads(response.text)

                pprint(json_data)

                if json_data.get('cod') != 200:
                    message_data['text'] = f'Ошибка: {json_data.get("message")}'
                else:
                    message_data['text'] = json_data

            # Отвечаем на сообщение
            url = TGRAM_URL.format(method='sendMessage')
            response = requests.get(url, message_data)
            json_data = json.loads(response.text)

            pprint(json_data)

    time.sleep(3)

    #
    #     def get_weather(city):
    #         city='Kharkiv'
    #         url_weather = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={owm_token}'
    #         response = requests.get(url_weather)
    #         if response.status_code == 200:
    #             json_data = json.loads(response.text)
    #         else:
    #             json_data = f'Ошибка при получении данных: код {response.status_code}'
    #         return json_data
    #

    # dict_weather = dict()
    # dict_weather['link'] = json_data[0]['MobileLink']
    # dict_weather['сейчас'] = {'temp': json_data[0]['Temperature']['Value'], 'sky': json_data[0]['IconPhrase']}
    # for i in range(len(json_data): 1:):
    # time = 'через' + str(i) + 'ч'
    # dict_weather[time] = {'temp': json_data[i]['Temperature']['Value'], 'sky': json_data[i]['IconPhrase']}


if __name__ == "__main__":
    main()
