#Jason Wei
#Compress all images in a single folder
#jason.20@dartmouth.edu

#Fetch all the arguments from the command line
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input_folder", type=str, help="input folder")
parser.add_argument("--compression_factor", type=float, help="how much to compress each side of the image by")
parser.add_argument("--output_folder", type=str, help="output_folder")
args = parser.parse_args()
input_folder = args.input_folder
output_folder = args.output_folder
compression_factor = args.compression_factor
assert input_folder is not None
assert output_folder is not None
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
import gc

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

#compress a reasonable size image
def compress_reasonable_image(image_path, output_path, compression_factor, i):

	#load the image with cv2
	#print("loading", image_path)
	image = cv2.imread(image_path)
	#print("cv2 loaded", image_path, "of", image.shape, "compressing by", compression_factor)
	
	#compress the image
	image = rescale(image, 1/compression_factor)
	image = np.rint(image*256)

	#save it
	imsave(output_path, image)
	print(i, image_path, "successfully saved")


def compress_large_image(image_path, output_path, compression_factor, i):

	#print("loading", image_path)
	#open the image
	foo = Image.open(image_path)
	#print("PIL loaded", image_path, "of", foo.size, "compressing by", compression_factor)

	#calculate the new dimensions
	orig_x = foo.size[0]
	orig_y = foo.size[1]
	new_x = int(orig_x/compression_factor)
	new_y = int(orig_y/compression_factor)

	#compress the image
	foo = foo.resize((new_x,new_y),Image.ANTIALIAS)
	foo.save(output_path)
	print(i, image_path, "successfully saved")

	#clear the memory
	foo = None
	gc.collect()

#Compressing a single folder:
def compress_folder(input_folder, output_folder, compression_factor):

	assert compression_factor != 1 #please don't do this.

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
		output_path = join(output_folder, image_name)

		try: #first try with CV2
			compress_reasonable_image(image_path, output_path, compression_factor, i)
		
		except:

			gc.collect()

			try: #now try with pillow
				compress_large_image(image_path, output_path, compression_factor, i)

			except:
				print("BROKEN", image_path)

		#print(i, "/", len(image_names), "saved")

	total_time = time.time() - start_time
	print('total time for', input_folder, "is", total_time)


if __name__ == "__main__":

	compress_folder(input_folder, output_folder, compression_factor)
