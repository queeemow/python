import telebot
from config import BOT_TOKEN
from utils import Convert, DLYouTube
from telebot import types
import os


yt = None
bot = telebot.TeleBot(BOT_TOKEN) #Передаю объекту токен бота из конфига
@bot.message_handler(content_types=["text"])
def get_text_messages(message): #Каждый раз при получения нового сообщения срабатывает декоратор - работает асинхронно
    print("message = ", message.text)
    con = Convert()
    IS_YT_LINK = con.is_YT_link(message) #Проверка корректности ссылки
    
    if IS_YT_LINK: #Если ссылка правильная то работаем
        global yt #Чтобы можно было добраться из других функций до экземпляра без класса
        yt = DLYouTube(str(message.text))
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #кнопки для выбора разрешения видео пользователем

        # res240 = types.KeyboardButton("240p")
        res360 = types.KeyboardButton('360p')
        # res480 = types.KeyboardButton('480p')
        res720 = types.KeyboardButton('720p') #Кнопки именно такие, так как формат видео позволяет скачать видео со звуком только в 360п или 720п
        markup.add(res360, res720)
        bot.send_message(message.chat.id, text="Chose a resolution via menu: ".format(message.from_user), reply_markup=markup)
        bot.register_next_step_handler(message, chose_YT_resolution) #Бессмысленный мув
        
    else: #Если ссылка не на ютюб то нахрен, пусть снова пробует
        bot.send_message(message.from_user.id, "Send me a link to a YouTube video e.g.: https://youtu.be/IUicoBcRiCo?si=l8_zRX8ix8dKy0ai *ISNATGRAM WILL BE ADDED LATER, SOME PATIENCE PLEASE BLUD* СТЕПА НЕ ЛОХ")


def chose_YT_resolution(message): #Бессмысленный мув
    downloadYT(message) #Бессмысленный мув

def downloadYT(message): #Скачать видос
    try:
        yt.set_res(message.text) #В зависимости от выбранного разрешения весит видос по разному
        if yt.is_big_filesize():  #Если весит много то надо скачать, разбить и отправить по частям
            bot.send_message(message.from_user.id, "Downloading, Please stand by...")
            yt.download()
            bot.send_message(message.from_user.id, "Downloading complete, splitting...")
            yt.video_split()
            sendYT(message, True)
        else:
            bot.send_message(message.from_user.id, "Downloading, Please stand by...") #Если весит немного то надо скачать и отправить
            yt.download()
            sendYT(message)
    except Exception as e:
        bot.send_message(message.from_user.id, "Something went wrong! Try again with the correct download options")
        get_text_messages(message)
        print(str(e))
    pass

def sendYT(message, is_big = False): #Отправить видео
    enjoy = True #Если все отправилось хорошо то написать пользователю что все гуд
    if is_big: #Если большой видос, который разбит на маленькие
        bot.send_message(message.from_user.id, "Splitting complete, sending...")
        current_video = yt.get_current_video_names()#Получить ссылку на список со всеми именами маленьких видосов
        for name in current_video: #Перебор имен в списке с маленькими видосами
            print("______SEND BIG VIDEO_______", name)
            print("current video =    ", current_video)
            f = open(yt.getpath() + '/' + name ,"rb")
            print("ok - big")
            try:
                bot.send_document(message.chat.id,f, timeout=200)
                os.remove(yt.getpath() + '/' + name) #Сразу удаляю маленький видос после отправки
            except Exception as e:
                bot.send_message(message.from_user.id, "The video size exceeds 50MB limit, please FUCK OFF BLUD") #SHOULD NEVER BE SHOWN TO USER
                print(str(e))
                os.remove(yt.getpath() + '/' + name) #ЕЕсли не отправился тоже удаляю
                enjoy = False #Если не отправился, пишу об этом пользователю и не вывожу что все хорошо
        os.remove(yt.getpath() + '/' + yt.get_filename())#В любом случае удаляю основной видос
        if enjoy: #Все хорошо - пишу пользователю
            bot.send_message(message.from_user.id, "Enjoy!")
        
        print("______SENT_______", name)
    else: #Если видео маленькое
        f = open(yt.getpath() + '/' + yt.get_filename() ,"rb")
        print("ok - small")
        try:
            bot.send_document(message.chat.id,f, timeout=200)
            os.remove(yt.getpath() + '/' + yt.get_filename())
            bot.send_message(message.from_user.id, "Enjoy!!")
        except Exception as e:
            bot.send_message(message.from_user.id, "The video size exceeds 50MB limit, please FUCK OFF BLUD") #SHOULD NEVER BE SHOWN TO USER
            print(str(e))
            os.remove(yt.getpath() + '/' + yt.get_filename())

bot.infinity_polling(timeout=10, long_polling_timeout = 5) #Зацикленное получение сообщений от пользователя