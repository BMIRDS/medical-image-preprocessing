
import os
from os import listdir
from os.path import isfile, join, isdir
from random import shuffle

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

#get '17asdfasdf2d_0_0.jpg' from 'train_folder/train/o/17asdfasdf2d_0_0.jpg'
def basename(path):
	return path.split('/')[-1]

#get 'train_folder/train/o' from 'train_folder/train/o/17asdfasdf2d_0_0.jpg'
def basefolder(path):
	return '/'.join(path.split('/')[:-1])

def cut_until_n(image_paths, n):

	shuffle(image_paths)
	for image_path in image_paths[n:]:
		os.system("rm " + image_path)

#balancing class distribution so that training isn't skewed
def balance_classes(training_folder, n):

	subfolders = get_subfolder_paths(training_folder)
	subfolder_to_images = {subfolder:get_image_paths(subfolder) for subfolder in subfolders}
	subfolder_to_num_images = {subfolder:len(subfolder_to_images[subfolder]) for subfolder in subfolders}

	for subfolder in subfolder_to_images:
		image_paths = subfolder_to_images[subfolder]
		cut_until_n(image_paths, n)

	print('balanced all val classes to have', n, 'images\n')


## main

if __name__ == "__main__":

	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("--input_folder", type=str, help="input folder")
	parser.add_argument("--num_val", type=int)
	args = parser.parse_args()
	balance_classes(args.input_folder, args.num_val)






