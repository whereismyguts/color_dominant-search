import json
import requests
import os
# from items import data
folder = 'images_full'
os.makedirs(folder, mode=0o777, exist_ok=True)
import base64
# cp1251:
data = json.loads(open('items.json', 'r', encoding='utf-8').read())

for i, (key, item) in enumerate(data['result']['items'].items()):

    icon = item['icon_url']

    image_url = 'https://community.akamai.steamstatic.com/economy/image/{}'.format(
        icon)

    filename = folder + '/' + str(i) + '.png'
    if os.path.exists(filename):
        continue
    try:
        with open(filename, 'wb') as f:
            f.write(requests.get(image_url).content)
    except Exception as e:
        print(filename)
        print(image_url)
        raise e

    if i % 100 == 0:
        print(i, len(data['result']['items']))

# print(json.dumps(item, indent=4))
