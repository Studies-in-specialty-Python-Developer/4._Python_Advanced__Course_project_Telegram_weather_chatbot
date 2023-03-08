import json
import time
import os
import requests
# from pprint import pprint
from const import ADMIN_ID, OWM_URL, TGRAM_URL, LAST_UPDATE_ID_FILE, COMMANDS


def main():
    # Считываем из файла ID последнего обработанного сообщения
    last_update_id = 0
    if os.path.exists(LAST_UPDATE_ID_FILE):
        with open(LAST_UPDATE_ID_FILE, encoding='utf-8') as file:
            data = file.readline()
            if data:
                last_update_id = int(data)

    turn_on = True
    while turn_on:
        # Получаем на сервере Telegram все сообщения, оставленные за последние 24 часа
        url = TGRAM_URL.format(method='getUpdates')
        response = requests.get(url, timeout=None)
        mess_queue = json.loads(response.text)

        # Просматриваем сообщения в хронологическом порядке и обрабатываем те, у которых Update_ID больше,
        # чем ID последнего обработанного сообщения
        response_data = {}
        for mess in mess_queue.get('result'):
            if last_update_id < mess.get('update_id'):

                # Получаем необходимые параметры сообщения
                chat_id = mess.get('message').get('chat').get('id')
                text = mess.get('message').get('text')
                last_update_id = mess.get('update_id')
                user_id = mess.get('message').get('from').get('id')

                # Формируем ответ на сообщение
                response_data['chat_id'] = chat_id
                if COMMANDS.get(text):
                    response_data['text'] = COMMANDS[text]
                    if text == '/turnoff':
                        if str(user_id) == ADMIN_ID:
                            turn_on = False
                        else:
                            response_data['text'] = 'Извините, у Вас нет прав администратора'
                else:
                    url = OWM_URL.format(city=text)
                    response = requests.get(url, timeout=None)
                    if response.status_code in [200, 404]:
                        json_data = json.loads(response.text)
                        if json_data.get('cod') == 200:
                            response_data['text'] = f'{json_data.get("name")}, {json_data.get("sys").get("country")}' \
                                                    + f'\nТемпература: {json_data.get("main").get("temp")} С, ' \
                                                    + f'давление: {json_data.get("main").get("pressure")} мбар, ' \
                                                    + f'облачность: {list(json_data.get("clouds").values())[0]} %'
                        else:
                            response_data['text'] = f'Ошибка {json_data.get("cod")}: {json_data.get("message")}\n' \
                                                    + 'Введите название города'
                    else:
                        response_data['text'] = f'Ошибка сети, код: {response.status_code}\n' \
                                                + 'Попробуйте сделать запрос позже'

                # Отвечаем на сообщение
                url = TGRAM_URL.format(method='sendMessage')
                response = requests.get(url, response_data, timeout=None)

                # Записываем в файл Update_ID текущего сообщения
                with open(LAST_UPDATE_ID_FILE, 'w', encoding='utf-8') as file:
                    file.write(str(last_update_id))

        time.sleep(0.5)


if __name__ == "__main__":
    main()
