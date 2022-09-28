import requests
import telebot

token = '2062328204:AAExyf0hNiXoT38pGqSn_ID4qB-PjGHM4kE'
bot = telebot.TeleBot(token, parse_mode='HTML')

def _upload_img(url_img):
    url = "https://api.imgur.com/3/image"
    payload={'image': url_img}
    files=[]
    headers = {
    'Authorization': 'Client-ID 306f7cc6448a694'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.text)

# Handles all sent documents and audio files
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file = bot.get_file(message.photo[-1].file_id)
    print('https://api.telegram.org/file/bot'+token+'/'+file.file_path)
    _upload_img('https://api.telegram.org/file/bot'+token+'/'+file.file_path)

if __name__=='__main__':
    bot.infinity_polling()