# Заменить на свои идентификаторы и переименовать файл в const.py

ADMIN_ID = 'My_Telegram_ID'

OWM_TOKEN = 'My_OpenWeatherMap_token'

TGRAM_TOKEN = 'My_Telegram_token'

OWM_URL = ''.join(['https://api.openweathermap.org/data/2.5/weather?q={city}&appid=',
                   OWM_TOKEN, '&units=metric&lang=ua'])

TGRAM_URL = ''.join(['https://api.telegram.org/bot', TGRAM_TOKEN, '/{method}'])

LAST_UPDATE_ID_FILE = 'last_update_id.txt'

COMMANDS = {
    '/start': 'Здравствуйте!\nВведите название города',
    '/stop': 'До свидания!',
    '/turnoff': 'Бот остановлен. Обработка сообщений прекращена.'
}
