import json
import requests
import os
import sys
# from items import data
folder = 'images_full'
os.makedirs(folder, mode=0o777, exist_ok=True)
import base64
# cp1251:
input_data = json.loads(open('items.json', 'r', encoding='utf-8').read())

output_data = list()

for i, (key, item) in enumerate(input_data['result']['items'].items()):

    icon = item['icon_url']
    name = item['market_name']
    image_url = 'https://community.akamai.steamstatic.com/economy/image/' + icon
    image_filename = folder + '/' + str(i) + '.png'

    try:
        if not os.path.exists(image_filename):
            with open(image_filename, 'wb') as f:
                f.write(requests.get(image_url).content)

        output_data.append(dict(
            name=name,
            image_url=image_url,
            image_filename=image_filename,
        ))

    except Exception as e:

        print(image_url)
        raise e

    if i % 100 == 0:
        print(i, len(input_data['result']['items']))

with open('images_data.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(output_data, indent=4, ensure_ascii=False))

# print(json.dumps(item, indent=4))
