#Jason Wei
#Compress all images in a folder with subfolders
#jason.20@dartmouth.edu

#Fetch all the arguments from the command line
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input_big_folder", type=str, help="input folder")
parser.add_argument("--compression_factor", type=float, default=8)
parser.add_argument("--output_big_folder", type=str, help="output_folder")
args = parser.parse_args()
input_big_folder = args.input_big_folder
output_big_folder = args.output_big_folder
compression_factor = args.compression_factor
assert input_big_folder is not None
assert output_big_folder is not None

#Get the paths to the images
import os
from os import listdir
from os.path import isfile, join, isdir

import numpy as np
from scipy.misc import imsave
from PIL import Image
Image.MAX_IMAGE_PIXELS=1e10
from random import randint
import time
from scipy.stats import mode
import cv2

import skimage.measure
from skimage.transform import rescale, rotate

#get subfolders
def get_subfolder_paths(folder):
	subfolder_paths = [join(folder, f) for f in listdir(folder) if (isdir(join(folder, f)) and '.DS_Store' not in f)]
	if join(folder, '.DS_Store') in subfolder_paths:
		subfolder_paths.remove(join(folder, '.DS_Store'))
	subfolder_paths = sorted(subfolder_paths)
	return subfolder_paths

#create an output folder if it does not already exist
def confirm_output_folder(output_folder):
	if not os.path.exists(output_folder):
	    os.makedirs(output_folder)

#get '17asdfasdf2d_0_0.jpg' from 'train_folder/train/o/17asdfasdf2d_0_0.jpg'
def basename(path):
	return path.split('/')[-1]

#Compressing a single folder:
def compress_folder(input_folder, output_folder, compression_factor):

	#load the image names from the input folder
	image_names = [f for f in listdir(input_folder) if isfile(join(input_folder, f))]
	if '.DS_Store' in image_names:
		image_names.remove('.DS_Store')
	image_names = [x for x in image_names if ('T.' not in x and 'tif' not in x)]
	image_names = sorted(image_names)
	print(len(image_names), "images found in ", input_folder)

	#Get all the crops
	start_time = time.time()

	for i, image_name in enumerate(image_names):
		image_path = join(input_folder, image_name)

		try:
		
			print("loading", image_path)
			image = cv2.imread(image_path)
			print("loaded image from", image_path, "with shape", image.shape, "compressing by", compression_factor)

			if not compression_factor == 1:
				image = rescale(image, 1/compression_factor)
				image = np.rint(image*256)

			imsave(join(output_folder, image_name), image)
			print(i, "/", len(image_names), "saved")

		except:
			print("too large", image_path)

	total_time = time.time() - start_time
	print('total time for', input_folder, "is", total_time)

if __name__ == "__main__":

	subfolders = get_subfolder_paths(input_big_folder)
	for input_folder in subfolders:

		output_folder = join(output_big_folder, basename(input_folder))
		confirm_output_folder(output_folder)

		compress_folder(input_folder, output_folder, compression_factor)











