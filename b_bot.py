import reposter
import botmemory
import simplevk
import getpass
import threading
import requests


app_id = botmemory.app_id
my_id = botmemory.my_id
access_token = botmemory.access_token
v = botmemory.api_version

#chatting = botmemory.chatting
reposting = botmemory.reposting


vk = simplevk.vk()
vk.access_token = access_token
vk.v = v
vk.app_id = app_id
vk_proxy_dict = ""
while('vk'):
    if input('Хотите использовать прокси? [y/n]')=="y":
        print("Потребуются https proxy")
        https_proxy = input("Введите прокси в формате ip:port: ")
        try:
            vk_proxy_dict = { 
                "http": https_proxy,
                "https" : https_proxy, 
                }
            requests.get("https://vk.com", proxies=vk_proxy_dict)
            vk.proxy_dict = vk_proxy_dict
        except Exception as e:
            print("Прокси не отвечают")
            if input('Продолжить без прокси?[y/n]')=="n":
                exit()

    if (access_token!="" and input('Обнаружена прошлая авторизация. Войти?[y/n]')=="y"):
        try:
            vk.user_id = vk.request('users.get')['response'][0]['id']
            print("Успешная авторизация")
            break
        except KeyError:
            print("Возникла ошибка, нужна авторизация")

    if input("Авторизоваться по паролю или токену?[p/t]")=="t":
        access_token = input("введите токен: ")
        try:
            vk.user_id = vk.request('users.get')['response'][0]['id']
            print("Успешная авторизация")
            break
        except KeyError:
            print("Возникла ошибка, нужна авторизация")

    try:
        login = input('    Login: ')
        password = getpass.getpass('    Password: ')
        vk.authorize(botmemory.app_id, login, password, 'offline+wall+friends', botmemory.api_version, vk_proxy_dict)
    except simplevk.AuthorizationError as autherr:
        print(autherr)
        continue
    if input('    Save token? [y/n]')=="y":
            botmemory.save_token(vk.access_token)
    print('Успешная авторизация')
    break

try:
    #if chatting:
    #    threading.Thread(target=chatbot.start, args=(vk,)).start()
    if reposting:
        threading.Thread(target=reposter.start, args=(vk,)).start()
except Exception as e:
    print("Error: "+str(e))
#chatbot.start(vk)
#reposter.start(vk)
#birthcongr.start()
