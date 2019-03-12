
from PIL import Image
Image.MAX_IMAGE_PIXELS=1e10
import cv2

import skimage.measure
from skimage.transform import rescale, rotate
from scipy.stats import mode
from scipy.misc import imsave
import statistics
import os
from os import listdir
from os.path import isfile, join, isdir
import numpy as np

#Fetch all the arguments from the command line
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input_folder", type=str, help="input folder")
parser.add_argument("--output_folder", type=str, help="output_folder")
parser.add_argument("--border_width", type=int, default=224, help="how big the whitespace border should be")
args = parser.parse_args()
input_folder = args.input_folder
output_folder = args.output_folder
border_width = args.border_width
assert input_folder is not None
assert output_folder is not None
assert border_width is not None

#create an output folder if it does not already exist
def confirm_output_folder(output_folder):
	if not os.path.exists(output_folder):
	    os.makedirs(output_folder)

#get full image paths
def get_image_paths(folder):
	image_paths = [join(folder, f) for f in listdir(folder) if isfile(join(folder, f))]
	if join(folder, '.DS_Store') in image_paths:
		image_paths.remove(join(folder, '.DS_Store'))
	image_paths = sorted(image_paths)
	return image_paths

#get '17asdfasdf2d_0_0.jpg' from 'train_folder/train/o/17asdfasdf2d_0_0.jpg'
def basename(path):
	return path.split('/')[-1]

###########################################
########### FILTERING WHITESPACE ##########
###########################################

def is_purple_dot(r, g, b):
	rb_avg = (r+b)/2
	if r > g - 10 and b > g - 10 and rb_avg > g + 20:
		return True
	return False

def is_purple_dot_relax(r, g, b):
	rb_avg = (r+b)/2
	if r > g - 2 and b > g - 2 and rb_avg > g + 2:
		return True
	return False

def is_purple_dot_strict(r, g, b):
	rb_avg = (r+b)/2
	if r > g - 10 and b > g - 10 and rb_avg > g + 20:
		return True
	return False
	
#this is actually a better method than is whitespace, but only if your images are purple lols
def is_purple(crop, threshold=20):
	pooled = skimage.measure.block_reduce(crop, (int(crop.shape[0]/15), int(crop.shape[1]/15), 1), np.average)
	num_purple_squares = 0
	for x in range(pooled.shape[0]):
		for y in range(pooled.shape[1]):
			r = pooled[x, y, 0]
			g = pooled[x, y, 1]
			b = pooled[x, y, 2]
			if is_purple_dot(r, g, b):
				num_purple_squares += 1
	if num_purple_squares > threshold: 
		return True
	return False

def is_purple_strict(crop, threshold=20):
	pooled = skimage.measure.block_reduce(crop, (int(crop.shape[0]/15), int(crop.shape[1]/15), 1), np.average)
	num_purple_squares = 0
	for x in range(pooled.shape[0]):
		for y in range(pooled.shape[1]):
			r = pooled[x, y, 0]
			g = pooled[x, y, 1]
			b = pooled[x, y, 2]
			if is_purple_dot_strict(r, g, b):
				num_purple_squares += 1
	if num_purple_squares > threshold: 
		return True
	return False

#find how big the image is
def find_bounds(image, grid_size):

	x_incre = int(image.shape[1]/grid_size)
	y_incre = int(image.shape[0]/grid_size)

	x_grids = set()
	y_grids = set()

	for i in range(grid_size):
		for j in range(grid_size):
			x_begin = i * x_incre
			y_begin = j * y_incre
			x_end = x_begin + x_incre
			y_end = y_begin + y_incre

			crop = image[y_begin:y_end, x_begin:x_end, :]
			if is_purple(crop):
				x_grids.add(x_begin)
				x_grids.add(x_end)
				y_grids.add(y_begin)
				y_grids.add(y_end)

	return min(x_grids), min(y_grids), max(x_grids), max(y_grids)

#pad the image with some whitespace
def pad_image_with_whitespace(image, border_width):

	blank = np.full((image.shape[0]+2*border_width, image.shape[1]+2*border_width, image.shape[2]), 243)
	print(image.shape, blank.shape)
	blank[border_width:border_width+image.shape[0], border_width:border_width+image.shape[1], :] = image
	return blank

#remove extraneous whitespace
def remove_whitespace(image_path, output_folder, border_width):

	#get the new image
	image = cv2.imread(image_path)
	x_min, y_min, x_max, y_max = find_bounds(image, 20)
	image = image[y_min:y_max, x_min:x_max]

	#rotate it to landscape
	x_len = image.shape[1]
	y_len = image.shape[0]

	if y_len > x_len:
		image = np.rot90(image)

	#add the border
	image = pad_image_with_whitespace(image, border_width)

	#save the new image
	name = basename(image_path)
	outpath = output_folder + '/' + name
	imsave(outpath, image)


#main function
if __name__ == '__main__':

	image_paths = get_image_paths(input_folder)
	confirm_output_folder(output_folder)

	for image_path in image_paths:
		remove_whitespace(image_path, output_folder, border_width)

	print("finished, outputs in", output_folder)




