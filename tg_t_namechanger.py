from telethon import TelegramClient, events, sync
from telethon.tl.functions.messages import GetHistoryRequest
from telethon import functions, types
import pandas
import vk
import datetime
import time
import random
import requests

# отправка пожилой информации
def log(text):
    local_time = str(datetime.datetime.now()).split(' ')[1].split('.')[0]
    log_text = f"[{local_time}] {text}"
    print(log_text)

# рандомное имя
def generate_name():
    f_str = 'кнгзхвпрлдсмт'
    ff_str = 'kngzhvprldsmt'
    s_str = 'уеаои'
    ss_str = 'ueaoi'

    result_ru = ''
    result_en = ''
    for i in range(4):
        index_f = random.randint(0, len(f_str)-1)
        index_s = random.randint(0, len(s_str)-1)

        result_ru += f_str[index_f] + s_str[index_s]
        result_en += ff_str[index_f] + ss_str[index_s]
    result_list = [result_ru, result_en]
    return result_list

# запуск бота
def repolling(app):
    try:
        log('Запускаю машину')
        app.start()
        # app.run_until_disconnected()
    except:
        log('Перезапускаю тачку')
        app.start()
        # app.run_until_disconnected()
        time.sleep(15)
        repolling(app)

# получаем прикол для юзания приколов
def get_app():
    type = 'tg_t_namechanger'
    data_url = 'https://raw.githubusercontent.com/colorfulpaintofapriltoday/data/main/tg_bot_data.csv'

    # собираем нужную информацию
    bot_data = pandas.read_csv(data_url)
    api_id = bot_data.loc[bot_data['name'] == type]['data1'].values.item()
    api_hash = bot_data.loc[bot_data['name'] == type]['data2'].values.item()

    app = TelegramClient(type, api_id, api_hash)
    return app

def write_name(text):
    file = open('cb_name.txt', 'w')
    file.write(text)
    file.close()

def update_name(app, i):
    try:
        name_list = generate_name()
        chat_info = app.get_dialogs()
        time.sleep(1)

        if len(chat_info) != 0:
            pinned_list = []
            for dialog in chat_info:
                if dialog.pinned:
                    pinned_list.append(dialog.id)

            chat_id = pinned_list[i]

            # app.set_chat_title(chat_id=chat_id, title=name_list[0])

            app(functions.channels.EditTitleRequest(
                channel=chat_id,
                title=name_list[0]))

            time.sleep(1)

            # messages = app.get_history(chat_id=chat_id)
            posts = app(GetHistoryRequest(
                peer=chat_id,
                limit=100,
                offset_date=None,
                offset_id=0,
                max_id=0,
                min_id=0,
                add_offset=0,
                hash=0))
            time.sleep(1)

            # m_id = messages[0]['message_id']
            m_id = posts.messages[0].id

            # app.delete_messages(chat_id=chat_id, message_ids=m_id)
            app(functions.channels.DeleteMessagesRequest(
                channel=chat_id,
                id=[m_id]
            ))

            time.sleep(1)

            write_name(name_list[0])

            log(f'сменил имя на {name_list[0]}')
    except:
        log('Ошибка')
        return False

def main():
    i = 0
    app = get_app()
    repolling(app=app)
    while True:
        update_name(app=app, i=i)
        i = 1 - i
        time_to_sleep = random.randint(5, 7)
        time.sleep(time_to_sleep*60)

main()