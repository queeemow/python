import re

"""curl "https://onlyfans.com/api2/v2/init" ^
  -H "authority: onlyfans.com" ^
  -H "accept: application/json, text/plain, */*" ^
  -H "accept-language: en-US,en;q=0.9" ^
  -H "app-token: 33d57ade8c02dbc5a333db99ff9ae26a" ^
  -H "cookie: csrf=P3nYoaUtf3aaf0ff0489cef153b874f6ce479cd6; auth_id=237024672; sess=f69j9ud69s0n2lsk495au3nbt7; auth_uid_237024672=YtECu8IfUv2qmabwWQOhDvqIASlkKNIE; cookiesAccepted=all; cwr_u=71be000e-a138-47d3-8547-19e9344043cc; cwr_s=eyJzZXNzaW9uSWQiOiI4MDdmOGY2ZC01YWU2LTQxOWYtODkyMS0zNDk4OTc1MDM5YzEiLCJyZWNvcmQiOnRydWUsImV2ZW50Q291bnQiOjEzLCJwYWdlIjp7InBhZ2VJZCI6Ii8iLCJwYXJlbnRQYWdlSWQiOiIvbXkvcXVldWUvMjAyMy0wNy0xMyIsImludGVyYWN0aW9uIjoxMiwicmVmZXJyZXIiOiIiLCJyZWZlcnJlckRvbWFpbiI6IiIsInN0YXJ0IjoxNjg5MjY0ODkxMjIxfX0=; lang=en; c=340187067-1; fp=49d342197f964437695aa500c139f42f946a3acf; st=97bb057307df182e3e05ebac882be2c28af7e6c57160714f58fd735f9a0f6a48; ref_src=" ^
  -H "referer: https://onlyfans.com/my/notifications" ^
  -H "sec-ch-ua: ^\^"Google Chrome^\^";v=^\^"111^\^", ^\^"Not(A:Brand^\^";v=^\^"8^\^", ^\^"Chromium^\^";v=^\^"111^\^"" ^
  -H "sec-ch-ua-mobile: ?0" ^
  -H "sec-ch-ua-platform: ^\^"Windows^\^"" ^
  -H "sec-fetch-dest: empty" ^
  -H "sec-fetch-mode: cors" ^
  -H "sec-fetch-site: same-origin" ^
  -H "sign: 13681:79f49ec045b82e2823c959051aaf4b369667d830:2e7:653fe833" ^
  -H "time: 1698750762486" ^
  -H "user-agent: Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36" ^
  -H "x-bc: 49d342197f964437695aa500c139f42f946a3acd" ^
  --compressed"""

class Cookie:
    PATH_TO_FILE = None
    RAW_FILE = None
    RAW_FILE_CONTENT = None
    
    timestamp = None

    APP_TOKEN = None
    SESS = None
    AUTH_ID = None
    AUTH_UID_ = None
    USER_AGENT = None
    X_BC = None

    def __init__(self):
        pass 

    def parse(self, path):
        self.PATH_TO_FILE = path
        self.RAW_FILE = self.open_file()
        self.RAW_FILE_CONTENT = self.RAW_FILE.read()
        self.define()

    def define(self):
        self.APP_TOKEN = self._define_app_token()
        self.SESS = self.define_sess()
        self.AUTH_ID = self._define_auth_id()
        self.AUTH_UID_ = self._define_uid()
        self.USER_AGENT = self._define_user_agent()
        self.X_BC = self._define_x_bc()

    def open_file(self):
        f = open(self.PATH_TO_FILE)
        return f

    def upload_file(self):
        f = open(f"auth_{self.timestamp}.json", 'w')
        return f

    def save(self, timestamp = 0):
        self.timestamp = timestamp
        f = self.upload_file()
        f.write('{\n\t"auth": {\n\t\t"app-token": "' + self.APP_TOKEN + '",\n\t\t"sess": "' + self.SESS + '",\n\t\t"auth-id": "' + self.AUTH_ID + '",\n\t\t"auth-uid": "' + self.AUTH_UID_ + '",\n\t\t"user-agent": "' + self.USER_AGENT + '",\n\t\t"x-bc": "' + self.X_BC + '"\n\t}\n}')
        f.close()
        self.RAW_FILE.close()

        {"auth": {self.APP_TOKEN[0]: self.APP_TOKEN[1]}}
    def _define_app_token(self):
        return re.findall('app.token[^"]+', self.RAW_FILE_CONTENT)[0].split(": ")[1]

    def define_sess(self):
        return re.findall('sess[^;]+', self.RAW_FILE_CONTENT)[0].split("=")[1]

    def _define_auth_id(self):
        return re.findall('auth.id[^;]+', self.RAW_FILE_CONTENT)[0].split("=")[1]
    
    def _define_uid(self):
        return re.findall('auth.uid[^;]+', self.RAW_FILE_CONTENT)[0].split("=")[1]

    def _define_user_agent(self):
        return re.findall('user.agent[^"]+', self.RAW_FILE_CONTENT)[0].split(": ")[1]

    def _define_x_bc(self):
        return re.findall('x.bc[^"]+', self.RAW_FILE_CONTENT)[0].split(": ")[1]

if __name__ == '__main__':
    cookie = Cookie()
    cookie.parse('./example.txt')
    cookie.save()
