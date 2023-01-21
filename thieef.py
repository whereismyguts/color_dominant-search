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


RENDER_TEMPLATE = """
<img width="200" height="200" src="{}" style="display:inline"/>
<div style="background-color: rgb({},{},{}); width: 200; height:200; display:inline-block"> </div>
<br>
"""


def dist(c1, c2):
    point1 = np.array(c1)
    point2 = np.array(c2)
    euclidean_distance = np.linalg.norm(point1 - point2)
    return euclidean_distance


def analyze_image(main_image_name, images_folder, top, backup_filename=None):
    print('Input data:')
    print('main_image_name:', main_image_name)
    print('images_folder:', images_folder)
    print('top:', top)
    print('backup_filename:', backup_filename)

    color_thief = ColorThief(main_image_name)
    main_dominant_color = color_thief.get_color(quality=1)

    if backup_filename and os.path.exists(backup_filename):
        with open(backup_filename, 'rb') as f:
            image_by_color = pickle.load(f)
    else:
        image_by_color = dict()

        for i, image_path in enumerate(os.listdir(images_folder)):
            try:
                image_path = os.path.join(images_folder, image_path)
                color_thief = ColorThief(image_path)
                dominant_color = color_thief.get_color(quality=1)
                image_by_color[dominant_color] = image_by_color.get(
                    dominant_color, []
                ) + [image_path]
            except Exception as e:
                print(e)

            if i % 100 == 0:
                print(i, 'images processed')

        if backup_filename:
            with open(backup_filename, 'wb') as f:
                pickle.dump(image_by_color, f)

    keys = list(image_by_color.keys())
    keys = sorted(keys, key=lambda x: dist(x, main_dominant_color))

    html = '<html><body>' + \
        RENDER_TEMPLATE.format(main_image_name, *main_dominant_color)

    for key in keys[:top]:
        # print(key, image_by_color[str(key)], dist(key, main_dominant_color))
        for image_path in image_by_color[key]:
            html += RENDER_TEMPLATE.format(
                image_path, *key
            )
            break  # show only one image per color

    result_name = 'result_{}_top_{}_{}.html'.format(
        main_image_name.split('/')[-1],
        top,
        datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
    )
    html += '</body></html>'
    with open(result_name, 'w') as f:
        f.write(html)

    print('-' * 20)
    print(result_name, 'saved')
    print('-' * 20)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--main_image_name', type=str,
        default='cases/puff.png'
    )
    parser.add_argument(
        '--images_folder', type=str,
        default='images'
    )  # images_full
    parser.add_argument(
        '--top', type=int,
        default=10
    )
    parser.add_argument(
        '--backup_filename', type=str,
        default='image_by_color.pickle'
    )
    args = parser.parse_args()
    return args


if __name__ == '__main__':

    args = parse_args()

    # testing:
    # for image_num in [103, 1003, 4003, 5004]:
    #     analyze_image(
    #         'images_full/{}.png'.format(image_num),
    #         'images',
    #         top=10,
    #         backup_filename='test.pickle'
    #     )
    # sys.exit(0)

    analyze_image(
        main_image_name=args.main_image_name,
        images_folder=args.images_folder,
        top=args.top,
        backup_filename=args.backup_filename
    )
