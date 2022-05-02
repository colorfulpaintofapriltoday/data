import threading
import requests
import time
import pandas
import random
from random import randint
import pandas
import os

# отправка сообщения
def send_message(text, peer_id, access_token, username, proxies):
    random_id = random.randint(100000, 1000000000)
    r = requests.get('https://api.vk.com/method/messages.send', proxies=proxies, params={
        'v': 5.124,
        'peer_id': peer_id,
        'access_token': access_token,
        'message': text,
        'random_id': random_id
    }).json()
    if 'error' in r and r['error']['error_code'] == 14:
        time.sleep(10*60)

# откладка через группу вк
def send_debug(text):
    random_id = random.randint(100000, 1000000000)
    r = requests.get('https://api.vk.com/method/messages.send', params={
        'v': 5.124,
        'peer_id': 189890658,
        'access_token': '3f713846ca1182c6e163a63eb6b5572bb6c0815f58d04f5723f79f614f041899ab1e448bdebd11ce2729e',
        'message': text,
        'random_id': random_id
    }).json()

# чат №1
def send_anon_cb1(address, access_token, vk_username, proxies):
    peer_id = -140876144
    send_message('!c', peer_id, access_token, vk_username, proxies)
    time.sleep(2)
    send_message('!н', peer_id, access_token, vk_username, proxies)
    time.sleep(2)

    # делаем сообщение и пишем его
    msg = gen_cb_msgs(address)
    send_message(msg, peer_id, access_token, vk_username, proxies)
    time.sleep(2)

    time.sleep(10)

# чат №2
def send_anon_cb2(address, access_token, vk_username, proxies):
    peer_id = -190262367
    send_message('!стоп', peer_id, access_token, vk_username, proxies)
    time.sleep(2)
    send_message('!поиск', peer_id, access_token, vk_username, proxies)
    time.sleep(2)

    # делаем сообщение и пишем его
    msg = gen_cb_msgs(address)
    send_message(msg, peer_id, access_token, vk_username, proxies)
    time.sleep(2)

    time.sleep(10)

# чат №3
def send_anon_cb3(address, access_token, vk_username, proxies):
    peer_id = -132834409

    send_message('!стоп', peer_id, access_token, vk_username, proxies)
    time.sleep(2)

    r = requests.get('https://api.vk.com/method/messages.getHistory', proxies=proxies, params={
        'v': 5.124,
        'peer_id': peer_id,
        'access_token': access_token,
        'count': 1
    }).json()
    if 'response' in r:
        message_text = r['response']['items'][0]['text']
        if 'возраст' in message_text:
            send_message('18', peer_id, access_token, vk_username, proxies)

    send_message('!новый', peer_id, access_token, vk_username, proxies)
    time.sleep(2)

    # делаем сообщение и пишем его
    msg = gen_cb_msgs(address)
    send_message(msg, peer_id, access_token, vk_username, proxies)
    time.sleep(2)

    time.sleep(10)


# чат №4
def send_anon_cb4(address, access_token, vk_username, proxies):
    peer_id = -71729358
    send_message('!стоп', peer_id, access_token, vk_username, proxies)
    time.sleep(2)
    send_message('!мж', peer_id, access_token, vk_username, proxies)
    time.sleep(2)

    # делаем сообщение и пишем его
    msg = gen_cb_msgs(address)
    send_message(msg, peer_id, access_token, vk_username, proxies)
    time.sleep(2)

    time.sleep(10)

# чат №5
def send_anon_cb5(address, access_token, vk_username, proxies):
    peer_id = -66678575
    send_message('!стоп', peer_id, access_token, vk_username, proxies)
    time.sleep(2)
    send_message('!мж', peer_id, access_token, vk_username, proxies)
    time.sleep(2)

    # делаем сообщение и пишем его
    msg = gen_cb_msgs(address)
    send_message(msg, peer_id, access_token, vk_username, proxies)
    time.sleep(2)

    time.sleep(10)

# чекаем бан ботов
def is_all_banned(access_token, vk_username, proxies):
    data = {'cb1': False, 'cb2': False, 'cb3': False, 'cb4': False, 'cb5': False}
    cb1 = True
    cb2 = False
    cb3 = False
    cb4 = False
    cb5 = False

    # первый бот
    r = requests.get('https://api.vk.com/method/messages.getHistory', proxies=proxies, params={
        'v': 5.124,
        'peer_id': -140876144,
        'access_token': access_token,
        'count': 1
    }).json()
    message_text = r['response']['items'][0]['text']
    if 'решить капчу' in message_text:
        cb1 = True
    else:
        cb2 = False
    data['cb1'] = cb1

    # второй бот
    b_request = requests.get('https://api.vk.com/method/groups.getById', proxies=proxies, params={
        'v': 5.124,
        'group_id': 190262367,
        'access_token': access_token,
        'fields': 'ban_info'
    }).json()
    if 'ban_info' in b_request['response'][0]:
        cb2 = True
    data['cb2'] = cb2

    # третий бот
    c_request = requests.get('https://api.vk.com/method/messages.getHistory', proxies=proxies, params={
        'v': 5.124,
        'peer_id': -132834409,
        'access_token': access_token,
        'count': 10
    }).json()
    for item in c_request['response']['items']:
        if '⛔ Вы заблокированы за нарушение правил чата до' in item['text']:
            cb3 = True
    data['cb3'] = cb3

    # четвертый бот
    d_request = requests.get('https://api.vk.com/method/messages.getHistory', proxies=proxies, params={
        'v': 5.124,
        'peer_id': -71729358,
        'access_token': access_token,
        'count': 10
    }).json()
    for item in d_request['response']['items']:
        if 'чата по жалобе' in item['text'] or 'отмечен системой' in item['text'] or 'заблокированы' in item['text']:
            cb4 = True
    data['cb4'] = cb4

    # пятый бот
    e_request = requests.get('https://api.vk.com/method/messages.getHistory', proxies=proxies, params={
        'v': 5.124,
        'peer_id': -66678575,
        'access_token': access_token,
        'count': 10
    }).json()
    for item in e_request['response']['items']:
        if 'заблокированы за нарушение' in item['text']:
            cb5 = True
    data['cb5'] = cb5

    return data

# рандомный процент для спама
def random_rate(rate):
    value = random.randint(0, 100)
    if value < rate:
        return True
    else:
        return True

# читаем ссылку на тг
def read_name():
    try:
        file = open('cb_name.txt', 'r')
        name = file.read()
        file.close()
    except:
        name = None
    return name

# делаем заглавной с 50% шансом
def random_capitalize(text):
    a = random.randint(0, 1)
    if a == 0:
        return text.capitalize()
    else:
        return text

# генерим сообщение
def gen_cb_msgs(address):
    hi = random.choice(['привет', 'прив)', 'здравствуй', 'привки', 'привет, как зовут?', 'приветули'])
    smth = random.choice(['хочешь скину интимки шккльниц?', 'есть кое-что 18+) показать?',
                          'хочешь слив школьннц?', 'у меня есть сливы малллеток', 'у меня есть нюдсы млолеточек',
                          'у меня есть нюдсы милых шккльниц', 'хочешь фото и видосики со школьницами?',
                          'показать тебе нюдсы школьниц?', 'тебе скинуть интимки милых школьниц?'])
    search = random.choice(['вбей в теелегге', 'ищи в тиелееграме', 'найди в тиеллеграме', 'вбей в теллеге'])
    channel = random.choice(['—', '-', ':', '']) + ' ' + address

    msg = f'{hi}\n{smth}\n{search}{channel}'
    return msg

# чекаем акк
def acc_check(access_token, proxies):
    r = requests.get('https://api.vk.com/method/users.get', proxies=proxies, params={
        'v': 5.124,
        'access_token': access_token
    }).json()
    if 'error' in r and r['error']['error_code'] == 5:
        return False
    else:
        return True

# спамим
def chatbot_spam(ACC_ID):
    # proxies = {"https": "http://SNcHH1:6LhJkH@45.129.205.158:8000"}
    proxies = {"https": "http://8P9K4vNZ:e1C4vqQB@195.208.21.175:63234", 
               "http": "http://8P9K4vNZ:e1C4vqQB@195.208.21.175:63234"}

    cycles = 4
    cb1_ban = False
    cb2_ban = False
    cb3_ban = False
    cb4_ban = False
    cb5_ban = False

    # основной цикл
    time.sleep(ACC_ID*15)
    print('Запуск бота')
    while True:
        if random.randint(1, 20) == 15:
            time.sleep(60*5)

        data = pandas.read_csv('https://raw.githubusercontent.com/colorfulpaintofapriltoday/data/main/vk1.csv')
        acc_type = 'cb_vkusno'
        access_token = str(data.loc[(data['acc_id'] == ACC_ID) & (data['type'] == acc_type)]['token'].values.item())
        vk_username = data.loc[(data['acc_id'] == ACC_ID) & (data['type'] == acc_type)]['username'].values.item()

        address = read_name()
        if access_token != 'nan' and address != None:
            if not acc_check(access_token=access_token, proxies=proxies):
                send_debug(vk_username + '\n' + 'похоже, что акк отлетел')
                time.sleep(15 * 60)
            else:
                try:
                    if cycles > 6:
                        cycles = 0
                        ban_data = is_all_banned(access_token=access_token, vk_username=vk_username, proxies=proxies)
                        cb1_ban = ban_data['cb1']
                        cb2_ban = ban_data['cb2']
                        cb3_ban = ban_data['cb3']
                        cb4_ban = ban_data['cb4']
                        cb5_ban = ban_data['cb5']
                        time_to_sleep = random.randint(7, 15)
                        time.sleep(60 * time_to_sleep)
                    else:
                        if not cb1_ban and random_rate(35):
                            send_anon_cb1(address, access_token, vk_username, proxies=proxies) # Анонимный чат ВКонтакте
                        if not cb2_ban:
                            send_anon_cb2(address, access_token, vk_username, proxies=proxies) # Анонимный чат бот
                        if not cb3_ban:
                            send_anon_cb3(address, access_token, vk_username, proxies=proxies) # Студентки | Чат
                        if not cb4_ban and random_rate(50):
                            send_anon_cb4(address, access_token, vk_username, proxies=proxies) # ПОЗОРシ
                        if not cb5_ban and random_rate(50):
                            send_anon_cb5(address, access_token, vk_username, proxies=proxies) # Овсянка, сэр!
                        cycles += 1

                except Exception as e:
                    time.sleep(10)
                    print(f'ERROR:\n-----\n{str(e)}\n-----')
        else:
            print('Токена нет, сплю...')
            time.sleep(5*60)

# мэйн функтион
def main():
    # число потоков
    acc_data = pandas.read_csv('https://raw.githubusercontent.com/colorfulpaintofapriltoday/data/main/vk1.csv')
    thread_count = int(acc_data.loc[acc_data['type'] == 'cb_vkusno']['acc_id'].iloc[-1])

    # запускаем потоки
    thread_list = []
    for i in range(0, thread_count):
        th = threading.Thread(target=chatbot_spam, args=(i, ))
        thread_list.append(th)
    for th in thread_list:
        th.start()
    for th in thread_list:
        th.join()

main()
