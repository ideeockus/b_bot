import json
import time
from html.parser import HTMLParser
try:
    import requests
except ImportError:
    print('установите библиотеку requests')

def log(log_msg):
    with open("simplevk.log", 'a') as log_file:
        log_file.write(log_msg)

class vk:
    app_id = ''
    user_id = ''
    access_token = ''
    v = '5.101'
    proxy_dict = ""


    def authorize(self, app_id, login, password, scope, v, proxy_dict = ""):
        self.app_id = app_id
        self.v = v
        self.proxy_dict = proxy_dict if proxy_dict!="" else self.proxy_dict
        with requests.Session() as vk_session:
            log("proxy_dict "+str(proxy_dict))
            r = vk_session.get('https://oauth.vk.com/authorize?client_id='+app_id+'&display=page&redirect_uri=https://vk.com&scope='+scope+'&response_type=token&v='+v, proxies=proxy_dict)
            p = vkParser()
            p.feed(r.text)
            p.close()
            p.login_data['email'] = login
            p.login_data['pass'] = password
            
            if p.method == 'get':
                r = vk_session.get(p.url, params=p.login_data, proxies=proxy_dict)
            elif p.method == 'post':
                r = vk_session.post(p.url, data=p.login_data, proxies=proxy_dict)
            if r.url.find('access_token=') >= 0:
                self.access_token = r.url.partition('access_token=')[2].split('&')[0]
                self.user_id = r.url.partition('user_id=')[2]
            else:
                p = vkParser()
                p.feed(r.text)
                p.close()
                if p.method == 'get':
                    r = vk_session.get(p.url, proxies=proxy_dict)
                if p.method == 'post':
                    r = vk_session.post(p.url, proxies=proxy_dict)
                self.access_token = r.url.partition('access_token=')[2].split('&')[0]
                self.user_id = r.url.partition('user_id=')[2]
            if not self.user_id:
                raise AuthorizationError('Неправильный логин или пароль')
                
                
                
    def request(self, method, params=''):
        access_param = '&access_token='+str(self.access_token) if self.access_token else ''
        api_request = requests.get('https://api.vk.com/method/'+method+'?'+params+access_param+'&v='+str(self.v))
        return api_request.json()


    def encode_cyrilic(self, text):
        return str(text.encode("utf-8")).replace("\\x", "%")[2:-1]
        
        
        
class vkParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.login_data = {}
        self.method = "GET"
        self.url = ""
        
    def handle_starttag(self, tag, atribs):
        attrs = {}
        for attr in atribs:
            attrs[attr[0]] = attr[1]
        if tag == 'form':
            self.url = attrs['action']
            if 'method' in attrs:
                self.method = attrs['method']
        elif tag == 'input' and 'name' in attrs:
            self.login_data[attrs['name']] = attrs['value'] if 'value' in attrs else ""
            
            
            
class AuthorizationError(Exception):
    def __init__(self, value):
        self.value = value


