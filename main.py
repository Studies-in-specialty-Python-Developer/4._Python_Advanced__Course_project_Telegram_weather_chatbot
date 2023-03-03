import telebot
import requests


def main():
    with open('Telegram_token.txt', encoding='utf-8') as f:
        telegram_token = f.read()
    with open('OpenWeatherMap_token.txt', encoding='utf-8') as f:
        owm_token = f.read()

    bot = telebot.TeleBot(telegram_token)

    city = 'Kharkiv'
    api_request = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={owm_token}'
    response = requests.get(api_request)
    if response.status_code == 200:
        weather = response.text
    else:
        weather = f'Ошибка при получении данных: код {response.status_code}'
    print(weather)


if __name__ == "__main__":
    main()
