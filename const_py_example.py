""" Модуль содержит константы, необходимые для работы основного модуля main.py"""

# Заменить на свои идентификаторы и переименовать файл в const.py

# ID администратора Telegram чат-бота
ADMIN_ID = 'My_Telegram_ID'

# Токен для работы с API сайта OpenWeatherMap.org
OWM_TOKEN = 'My_OpenWeatherMap_token'

# Токен для работы с API Telegram
TGRAM_TOKEN = 'My_Telegram_token'

# Строка запроса информации о погоде с сайта OpenWeatherMap.org
OWM_URL = ''.join(['https://api.openweathermap.org/data/2.5/weather?q={city}&appid=',
                   OWM_TOKEN, '&units=metric&lang=','ru']) # lang 'en','ua','ru'

# Строка запроса для работы с API Telegram
TGRAM_URL = ''.join(['https://api.telegram.org/bot', TGRAM_TOKEN, '/{method}'])

# Имя файла, в который записывается ID последнего обработанного сообщения
LAST_UPDATE_ID_FILE = 'last_update_id.txt'

# Команды меню Telegram чат-бота
COMMANDS = {
    '/start': 'Здравствуйте!\nВведите название города',
    '/stop': 'До свидания!',
    '/turnoff': 'Бот остановлен, обработка запросов прекращена.'
}
