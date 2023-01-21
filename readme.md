# Image Similarity Search

This script takes an input image and finds the most dominant color of the image. Then it searches for other images in a given folder that have a similar color and generates an HTML file that shows the input image and the similar images.


## Installing requirements
`python -m pip install colorthief numpy`

## Usage
`python thieef.py --main_image_name path/to/input/image --images_folder path/to/images/folder --top N --backup_filename backup.pickle`

## Output
`result_input_image_name_top_N_timestamp.html`
Contains the input image and the similar images, sorted by color similarity
