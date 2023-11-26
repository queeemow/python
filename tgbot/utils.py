import re
from pytube import YouTube
from instascrape import Reel
import instaloader
import requests
import time
from config import BOT_TOKEN
from telethon import TelegramClient
import os
os.environ["IMAGEIO_FFMPEG_EXE"] = "./ffmpeg/ffmpeg"
from moviepy.editor import VideoFileClip

class Convert: #Проверка ссылки - ЮТЮБ ИНСТА

    def __init__(self) -> None:
        pass

    def is_YT_link(self, message):
        return len(re.findall('https://youtu.+', str(message))) > 0

class DLYouTube:
    MAX_FILESIZE = 52428800 #Максимальный размер файла в байтах(50мб) - ограничение телеграма
    path = None #Путь до папки с загруженными выидео
    url = None #Ссылка на видео
    vid = None #Объект экземпляр класса Ютюб
    vid_resolution = None #Выбранное Разрешение видоса
    available_resolutions = set() #Все доступные разрешения видоса
    file_name = None #Название файла без пути
    api_id = '26238569' #Тема для DL_big_files
    api_hash = 'cdd8366b4ad5d3308a75e4e88b3540e8'#Тема для DL_big_files
    phone = '+79312494456'#Тема для DL_big_files
    current_video = [] # Названия разбитых маленьких видосов, если основное видео весит больше МАКС_ФАЙЛСАЙЗ

    def __init__(self, url) -> None: # При создании объекта, передается введенная в чат пользователем ссылка на видео в качестве url
        try: #Создаю папку если ее нет во внешней директории с именем видеос
            os.mkdir('./videos') 
        except:
            pass
        self.path = os.path.abspath('./videos')
        self.url = url
        self.vid = YouTube(self.url)
        self.file_name = fr'{self.vid.title.split()[0]}_{self.vid_resolution}.mp4' #Имя файла - первое слово из заголовка(тайтл)_разрешение видео_.мп4
        self.all_resolutions() #Автоматический вызов функции, определяющей возможные разрешения для видео при создании экземпляра класса
        pass
        
    def set_res(self, res = '720p'): #Если разрешение не указано, то по дефолту устанавливается 720п
        self.vid_resolution = res
        self.file_name = fr'{self.vid.title.split()[0]}_{self.vid_resolution}.mp4'

    def getpath(self): #Инкапсуляция
        return self.path
    
    def get_filename(self):#Инкапсуляция
        return self.file_name
    
    def get_current_video_names(self):#Инкапсуляция
        return self.current_video

    def all_resolutions(self):#Инкапсуляция
        for v in self.vid.streams.filter(file_extension='mp4'):
            try:
                self.available_resolutions.append(re.findall(".+vcodec.+acodec.+", str(v))[0])
            except:
                break
            self.available_resolutions = sorted((self.available_resolutions))
        pass
    
    def DL_big_files(self): #НЕ РАБОТАЕТ!!!!!!!!!!!!!!!!!!!!
        entity = 'NMFYBot' #имя сессии - все равно какое'
        client = TelegramClient(entity, self.api_id, self.api_hash)
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(self.phone) #при первом запуске - раскомментить, после авторизации для избежания FloodWait советую закомментить
            client.sign_in(self.phone, input('Enter code: '))
        client.start()

        msg = client.send_file(
                           BOT_TOKEN,
                           self.path,
                           caption="suka",
                           file_name= self.file_name,
                           use_cache=False,
                           part_size_kb=512
        )
        client.disconnect()
        return msg
    
    def is_big_filesize(self):#Проверка является ли файл большим(превышает ли лимит телеграма и надо ли его делить на маленькие)
        return self.vid.streams.get_by_resolution(self.vid_resolution).filesize > self.MAX_FILESIZE 

    def video_split(self): #Деление файла на маленькие
        divide_into_count = self.vid.streams.get_by_resolution(self.vid_resolution).filesize//self.MAX_FILESIZE + 1
        print('divide into count = ', divide_into_count)
        print("SIZE OF FILE = ", self.vid.streams.get_by_resolution(self.vid_resolution).filesize)
        print('mocha1')
        current_duration = VideoFileClip(self.path+'/'+self.file_name).duration
        print('gavno2')
        single_duration = current_duration/divide_into_count
        i = 0
        while current_duration >= single_duration:
            clip = VideoFileClip(self.path+'/'+self.file_name).subclip(current_duration-single_duration, current_duration)
            current_duration = current_duration - single_duration
            self.current_video.append(f"{self.file_name[:-4]}_{divide_into_count}.mp4") #Добавляю в список текущий файл, так как первым будет файл с конца видео
            print(self.current_video[i])
            clip.to_videofile(self.current_video[i], codec="libx264", temp_audiofile='temp-audio.m4a', remove_temp=True, audio_codec='aac')
            os.rename('/Users/glebkuimov/hw1/python/'+self.current_video[i], self.path + '/' + self.current_video[i]) #Переношу микровидос получившийся в папку со всеми видео
            divide_into_count = divide_into_count - 1
            i = i + 1
        self.current_video.sort() #Сортирую в порядке возрастания, чтобы в мейне в цикле их в правильном порядке отослать пользователю
        pass

    def download(self): #Скачать видос 
        print('download method start')
        self.file_name = fr'{self.vid.title.split()[0]}_{self.vid_resolution}.mp4'
        print("filename = ", self.file_name)
        self.vid.streams.get_by_resolution(self.vid_resolution).download(self.path, self.file_name)
        print("Download method end")
        pass

# yt = DLYouTube('https://youtu.be/IUicoBcRiCo?si=l8_zRX8ix8dKy0ai')
# yt.set_res('720p')
# # yt.download()
# print(yt.is_big_filesize())
# yt.video_split()

# print(yt.DL_big_files())
class DLIGReels: #Допиливаю класс для скачки рилзов из инсты
    path = None
    url = None
    vid = None
    file_name = None
    headers = None
    session_id = '18c01b02e46-1f5d5f'

    def __init__(self, url) -> None:
        self.url = url
        self.path = '/Users/glebkuimov/hw1/python/videos/'
        print('URL ====  '+self.url)

        self.vid = Reel(self.url)
        self.define_headers()
        pass

    def define_headers(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43",
            "cookie":f'sessionid={self.session_id};'
            }
            
    def downloadIG(self):
        self.file_name = f'IgReel_{int(time.time())}'
        print('ok1')
        self.vid.scrape(headers = self.headers)
        print('ok2')
        self.vid.download(fp = f'{self.path+self.file_name}.mp4')
        pass



# ig = DLIGReels('https://www.instagram.com/reel/Czo-wWHJAIJ/?utm_source=ig_web_copy_link')
# L = instaloader.Instaloader()
# print("dsuka")
# # Provide the URL of the reel
# reel_url = 'https://www.instagram.com/reel/Czo-wWHJAIJ/?utm_source=ig_web_copy_link'

# # Extract the reel's shortcode from the URL
# shortcode = reel_url.split("/")[-2]
# print(shortcode)
# print(shortcode)
# print(shortcode)
# print(shortcode)
# # Fetch the reel
# reel = instaloader.Post.from_shortcode(L.context, shortcode)

# # Download the reel video
# L.download_post(reel, target=f"{reel.owner_username}_reel")


# available_resolutions = []
# yt = YouTube('https://youtu.be/u5xil0Ofhbs?si=dJwmQjjfHIaChnJU')
# for v in yt.streams.filter(file_extension='mp4'):
#     try:
#         available_resolutions.append(re.findall(".+vcodec.+acodec.+", str(v))[0])
#     except:
#         break
#     available_resolutions = sorted((available_resolutions))
# print(available_resolutions)