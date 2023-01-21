from ast import main
from copyreg import pickle
from colorthief import ColorThief
import json
import numpy as np
import argparse
import os
import pickle
import datetime
import sys

DEFAULT_TOP = 10
DEFAULT_BACKUP_FILENAME = 'backup.pickle'
DEFAULT_INPUT_JSON = 'images_data.json'
DEFAULT_MAIN_IMAGE_NAME = 'cases/puff.png'


def eucldist(c1, c2):
    point1 = np.array(c1)
    point2 = np.array(c2)
    euclidean_distance = np.linalg.norm(point1 - point2)
    return euclidean_distance


def analyze_image(main_image_name, input_json, top, backup_filename=None):
    print('Input data:')
    print('main_image_name:', main_image_name)
    print('input_json:', input_json)
    print('top:', top)
    print('backup_filename:', backup_filename)

    with open(input_json, 'r', encoding='utf-8') as f:
        images_data = json.loads(f.read())[:300]

    color_thief = ColorThief(main_image_name)
    main_dominant_color = color_thief.get_color(quality=1)

    if backup_filename and os.path.exists(backup_filename):
        with open(backup_filename, 'rb') as f:
            image_by_color = pickle.load(f)
    else:
        image_by_color = dict()

        images_data_len = len(images_data)
        for i, image_data in enumerate(images_data):
            try:
                color_thief = ColorThief(image_data['image_filename'])
                dominant_color = color_thief.get_color(quality=1)

                # # backup structure:
                #
                # image_by_color = {
                #     (R,G,B): [
                #         {
                #             "name": "Name | Property",
                #             "image_url": "https://...",
                #             "image_filename": "path/to/image.png"
                #             # "distance": 0.5 - will be added down below
                #         },
                #         ...
                #     ],
                #     ...
                # }
                # # #

                image_by_color[dominant_color] = image_by_color.get(
                    dominant_color, []
                ) + [image_data]

            except Exception as e:
                print(e)

            if i % 100 == 0:
                print('{}/{} images processed'.format(i, images_data_len))

            if backup_filename:
                with open(backup_filename, 'wb') as f:
                    pickle.dump(image_by_color, f)

    keys = list(image_by_color.keys())

    # keys = sorted(keys, key=lambda x: dist(x, main_dominant_color))
    for key in keys:
        distance = eucldist(key, main_dominant_color)
        for img_data in image_by_color[key]:
            img_data['distance'] = distance

    keys = sorted(keys, key=lambda x: image_by_color[x][0]['distance'])

    keys = keys[:top]  # cut top for performance
    results = [image_by_color[key] for key in keys]

    # flatten results:
    results = [item for sublist in results for item in sublist]
    return results[:top]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--main_image_name', type=str,
        default=DEFAULT_MAIN_IMAGE_NAME
    )
    parser.add_argument(
        '--input_json', type=str,
        default=DEFAULT_INPUT_JSON
    )  # images_full
    parser.add_argument(
        '--top', type=int,
        default=DEFAULT_TOP
    )
    parser.add_argument(
        '--backup_filename', type=str,
        default=DEFAULT_BACKUP_FILENAME
    )
    args = parser.parse_args()
    return args


if __name__ == '__main__':

    # # # Testing:
    # for image_num in [103, 1003, 4003, 5004]:
    #     analyze_image(
    #         'images_full/{}.png'.format(image_num),
    #         'images',
    #         top=10,
    #         backup_filename='test.pickle'
    #     )
    # sys.exit(0)
    # # #

    args = parse_args()
    result = analyze_image(
        main_image_name=args.main_image_name,
        input_json=args.input_json,
        top=args.top,
        backup_filename=args.backup_filename
    )

    print(json.dumps(result, indent=2))
