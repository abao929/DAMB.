import argparse, os
from skimage.io import imread, imsave
from skimage.transform import resize
from skimage import img_as_ubyte
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
            imsave(img_path, img_as_ubyte(scaled_img))

def parse_args():
    parser = argparse.ArgumentParser(description="resize images runner")
    parser.add_argument('-d', help="path to folder")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    data_path = args.d

    # check the args input
    assert os.path.exists(args.d)

    resize_images(data_path)
