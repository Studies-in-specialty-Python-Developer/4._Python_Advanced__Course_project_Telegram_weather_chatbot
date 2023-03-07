OWM_TOKEN = '692f04b9abc71bb676ab2ad0e8583fb0'
TGRAM_TOKEN = '5951472826:AAFbfKoAvSqJ8jWyi41NwkzUUR7eAabniSg'
OWM_URL = ''.join(['https://api.openweathermap.org/data/2.5/weather?q={city}&appid=', OWM_TOKEN,'&units=metric'])
TGRAM_URL = ''.join(['https://api.telegram.org/bot', TGRAM_TOKEN, '/{method}'])
LAST_UPDATE_ID_FILE = 'last_update_id.txt'
