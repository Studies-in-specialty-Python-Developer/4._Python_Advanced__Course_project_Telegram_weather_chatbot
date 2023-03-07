import json
import requests
import time
import os
from pprint import pprint
from const import *


def main():
    last_update_id = 0
    if os.path.exists(LAST_UPDATE_ID_FILE):
        with open(LAST_UPDATE_ID_FILE) as file:
            data = file.readline()
            if data:
                last_update_id = int(data)
    url = TGRAM_URL.format(method='getUpdates')
    response = requests.get(url)
    json_data = json.loads(response.text)
    pprint(json_data)
    message_data = dict()
    for item in json_data.get('result'):
        if last_update_id < item.get('update_id'):
            chat_id = item.get('message').get('chat').get('id')
            text = item.get('message').get('text')
            last_update_id = item.get('update_id')
            with open(LAST_UPDATE_ID_FILE, 'w') as file:
                file.write(str(last_update_id))

            print(chat_id, text, last_update_id)

            message_data['chat_id'] = chat_id
            if text == '/start':
                message_data['text'] = 'Здравствуйте!\nВведите название города'

            url = OWM_URL.format(city='Kharkiv')
            response = requests.get(url)
            json_data = json.loads(response.text)
            if json_data.get('cod') != 200:
                message_data['message'] = f'Ошибка: {json_data.get("message")}'

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
