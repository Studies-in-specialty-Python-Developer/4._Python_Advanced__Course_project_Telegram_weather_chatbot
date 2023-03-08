OWM_TOKEN = 'My_OpenWeatherMap_token'
TGRAM_TOKEN = 'My_Telegram_token'
OWM_URL = ''.join(['https://api.openweathermap.org/data/2.5/weather?q={city}&appid=', OWM_TOKEN, '&units=metric'])
TGRAM_URL = ''.join(['https://api.telegram.org/bot', TGRAM_TOKEN, '/{method}'])
LAST_UPDATE_ID_FILE = 'last_update_id.txt'
COMMANDS = {
    '/start': 'Здравствуйте!\nВведите название города',
    '/stop': 'До свидания!',
    '/stopbot': 'Бот остановлен. Обработка сообщений прекращена.'
}