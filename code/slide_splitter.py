import os
from os import listdir
from os.path import isfile, join, isdir
import cv2
from scipy.misc import imsave
import skimage.measure
from skimage.transform import rescale, rotate
import numpy as np

alphabet = 'abcdefghijklmnopqrstuv'

#get '17asdfasdf2d_0_0.jpg' from 'train_folder/train/o/17asdfasdf2d_0_0.jpg'
def basename(path):
	return path.split('/')[-1]

#get full image paths
def get_image_paths(folder):
	image_paths = [join(folder, f) for f in listdir(folder) if isfile(join(folder, f))]
	if join(folder, '.DS_Store') in image_paths:
		image_paths.remove(join(folder, '.DS_Store'))
	image_paths = sorted(image_paths)
	return image_paths

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
def save_clean(image, output_path, border_width):

	#get the new image
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
	print(output_path, image.shape)
	imsave(output_path, image)

################################
######### actual stuff #########
################################

#split a single image
def split_slide(image_path, output_folder, num_row, num_col, keep_all):

	image = cv2.imread(image_path)

	#trim the image
	image = image[	:min(image.shape[0], int(image.shape[0]/num_row)*num_row),
			 		:min(image.shape[1], int(image.shape[1]/num_col)*num_col), 
			 		:]
	
	x_len = image.shape[1]
	y_len = image.shape[0]
	x_incre = int(image.shape[1]/num_col)
	y_incre = int(image.shape[0]/num_row)

	#saving the image
	counter = 0
	name = basename(image_path)

	#save all the pieces
	if keep_all:
		for y_begin in range(0, y_len, y_incre):
			for x_begin in range(0, x_len, x_incre):

				part = image[y_begin:y_begin+y_incre, x_begin:x_begin+x_incre, :]
				outpath = output_folder + '/' + name.split('.')[0] + str(alphabet[counter]) + '.png' 
				save_clean(part, outpath, border_width=224)
				counter += 1
	
	#only take the top right piece
	else:
		part = image[0:y_incre, 0:x_incre, :]
		outpath = outpath = output_folder + '/' + name.split('.')[0] + str(alphabet[counter]) + '.png' 
		save_clean(part, outpath, border_width=224)

#split an entire folder
def split_slide_folder(input_folder, output_folder, num_row, num_col, keep_all=True):

	image_paths = get_image_paths(input_folder)
	for image_path in image_paths:
		split_slide(image_path, output_folder, num_row, num_col, keep_all)

def split_slide_big_folder(input_big_folder, output_folder, keep_all):

	subfolder_paths = get_subfolder_paths(input_big_folder)
	for subfolder_path in subfolder_paths:
		num_col = int(basename(subfolder_path).split('x')[0])
		num_row = int(basename(subfolder_path).split('x')[1])
		split_slide_folder(subfolder_path, output_folder, num_row, num_col, keep_all)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input_big_folder", type=str, help="input master folder")
parser.add_argument("--output_folder", type=str, help="output folder")
args = parser.parse_args()

#input_big_folder = '/Users/jasonwei/Desktop/clean_vcpps_8x/need_split/first_grids'
#output_folder = '/Users/jasonwei/Desktop/clean_vcpps_8x/need_split/second_outputs'

if __name__ == '__main__':

	confirm_output_folder(args.output_folder)
	split_slide_big_folder(args.input_big_folder, args.output_folder, keep_all=True)


