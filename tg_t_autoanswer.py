from telethon import TelegramClient, sync, events
import pandas
import time
import datetime
import random
import requests
import asyncio

# настройки пожилые
type = 'tg_autoanswer'
data_url = 'https://raw.githubusercontent.com/colorfulpaintofapriltoday/data/main/tg_bot_data.csv'

# собираем нужную информацию
bot_data = pandas.read_csv(data_url)
api_id = bot_data.loc[bot_data['name'] == type]['data1'].values.item()
api_hash = bot_data.loc[bot_data['name'] == type]['data2'].values.item()
tgraph_url = bot_data.loc[bot_data['name'] == type]['data3'].values.item()

# инициализируем клиент
# app = pyrogram.Client(api_id=api_id, api_hash=api_hash, session_name='tg_autoanswer')
app = TelegramClient('tg_t_autoanswer', api_id, api_hash)

# словарь для юзверов
user_id_list = []

def send_debug(text):
    random_id = random.randint(100000, 1000000000)
    r = requests.get('https://api.vk.com/method/messages.send', params={
        'v': 5.124,
        'peer_id': 189890658,
        'access_token': '4f70fc26088f18a767cb107f55a31d2c01aa50952c2064af16c55d66b874e3167a3c2f95331cd8fb8a9ba',
        'message': text,
        'random_id': random_id
    }).json()

def log(text):
    local_time = str(datetime.datetime.now()).split(' ')[1].split('.')[0]
    log_text = f"[{local_time}] {text}"
    send_debug(log_text)
    print(log_text)

def get_answer(text, tgraph_url):

    # тарифы
    if text == '1':
        answer = ['😏', '👧Тариф «Школьницы»\n'
                 'Что сюда входит?\n'
                 'Сливы школьниц (от 13-и лет), их домашние фото, видео соло и с партнерами, сливы переписок, адреса страниц ВК и Инстаграм\n' 
                 'Сколько стоит?\n'
                 '350 RUB\n\n'
                 '💦Тариф «Вписки»\n'
                 'Что сюда входит?\n'
                 'Сливы со вписок, фото и видео горячих девочек, у которых на уме сами знаете что)\n'
                 'Сколько стоит?\n'
                 '250 RUB\n\n'
                 '😲Тариф «Всё вместе»\n'
                 'Что сюда входит?\n'
                 'Тариф «Школьницы» и тариф «Вписки»\n'
                 'Сколько стоит?\n'
                 '500 RUB (экономите 100 RUB😉)']

    # гарантии  и пруфы
    elif text == '2':
        answer = ['Замените запятую на точку: ', tgraph_url.replace('telegra.ph', 'telegra,ph')]

    # как получить доступ
    elif text == '3':
        answer = ["😊", 'Чтобы получить доступ к приватке, оплатите её с помощью киви или карты.\n\n'
                 '⚠️Не оставляйте никаких комментариев к платежу, иначе он не засчитается!\n\n'
                 'Реквизиты СБЕР: 5228 6005 6958 9916\n'
                 'Ссылка для QIWI: http://qiwi.com/n/WONAS944\n\n'
                 '❗После этого выберите пункт с подтверждением оплаты (чтобы нам пришло уведомление) и следуйте инструкции.']

    # я оплатил, что дальше?
    elif text == '4':
        answer = ['💖',
                'Огромное спасибо, что помогаете нам разиваться!\n\n'
                 'Чтобы получить доступ к каналу(ам), отправьте сюда скриншот/чек оплаты и время по МСК, когда был совершен перевод.\n\n'
                 'Мы получим уведомление, проверим оплату (в среднем это занимает около 30 минут) и в этом диалоге отправим вам ссылку(и).']
    else:
        answer = ['👋', 'Привет!\n'
                        'Я бот-автоответчик 🤖 \n'
                        'Я не понимаю слов, только цифры.\n\n'
                        'Если хочешь что-то узнать, просто напиши цифру:\n'
                        '1 — тарифы\n'
                        '2 — гарантии и пруфы\n'
                        '3 — как получить доступ?\n'
                        '4 — я оплатил, что дальше?']
    return answer

def repolling():
    try:
        log('Запускаю машину')
        app.start()
        app.run_until_disconnected()
    except:
        log('Перезапускаю тачку')
        app.start()
        app.run_until_disconnected()
        time.sleep(15)
        repolling()

# ответ на сообщения
@app.on(events.NewMessage(outgoing=False))
async def handler(event):
    # добавляем юзера
    user_id = event.message.peer_id.user_id
    if user_id not in user_id_list:
        user_id_list.append(user_id)

        # отправляем в лог
        users_amount = len(user_id_list)
        text_debug = F"(NEW_USER) user_id: {user_id}, users_amount: {users_amount}"
        log(text_debug)

    # отправляем текст в лог
    msg_text = event.message.raw_text
    text_debug = f"(MESSAGE) user_id: {user_id}, text: {msg_text}"
    log(text_debug)

    # отвечаем
    answer = get_answer(msg_text, tgraph_url=tgraph_url)
    await asyncio.sleep(0.5)
    for msg in answer:
        await event.reply(msg)
        await asyncio.sleep(0.5)
# запускаем бота
try:
    repolling()
except:
    repolling()

# запускаем бота
try:
    repolling()
except:
    repolling()

# ответ на сообщения
# @app.on_message(pyrogram.filters.text & pyrogram.filters.private)
# def echo(client, message):
#
#     # добавляем юзера
#     user_id = message.chat.id
#     if user_id not in user_id_list:
#         user_id_list.append(user_id)
#
#         # отправляем в лог
#         users_amount = len(user_id_list)
#         text_debug = F"(NEW_USER) user_id: {user_id}, users_amount: {users_amount}"
#         log(text_debug)
#
#     # отправляем текст в лог
#     username = message.chat.username
#     text_debug = f"(MESSAGE) user_id: {user_id}, username: {username}, text: {message.text}"
#     log(text_debug)
#
#     # находим ответ и отвечаем
#     answer = get_answer(message.text, tgraph_url=tgraph_url)
#     try:
#         for a in answer:
#             time.sleep(2)
#             message.reply_text(a)
#             time.sleep(2)
#     except:
#         log('Ошибка при отправке, сплю')
#         time.sleep(10)

