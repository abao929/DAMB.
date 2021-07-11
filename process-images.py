import argparse, os
from skimage.io import imread, imsave
from skimage.transform import resize
from skimage import img_as_ubyte
from skimage.color import grey2rgb
import numpy as np

def resize_images(folder_path):
    '''
    for each image in a folder path, resizes the image to 256px x 256px.
    '''
    for filename in os.listdir(folder_path):
        if filename != '.DS_Store':
            img_path = os.path.join(folder_path, filename)
            image = imread(img_path)
            scaled_img = resize(image, (256, 256))
            if scaled_img.shape == (256, 256):
                scaled_img = grey2rgb(scaled_img)
            imsave(img_path, img_as_ubyte(scaled_img))

def parse_args():
    parser = argparse.ArgumentParser(description="resize images runner")
    parser.add_argument('-d', help="path to folder or all")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    data_path = args.d

    if data_path != 'all':
        # check the args input
        assert os.path.exists(args.d)
        resize_images(data_path)
    else:
        all_paths = ['data/rock', 'data/alternative', 'data/blues', 'data/classical',
                     'data/hip-hop', 'data/heavy-metal', 'data/edm', 'data/country',
                     'data/indie', 'data/jazz', 'data/kpop', 'data/latin',
                     'data/r-n-b', 'data/pop', 'data/metal']
        for path in all_paths:
            resize_images(path)