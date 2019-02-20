
import os
from os import listdir
from os.path import isfile, join, isdir

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

def duplicate_until_n(image_paths, n):

	num_dupls = n - len(image_paths)

	print('balancing', basefolder(image_paths[0]), 'by duplicating', num_dupls)

	for i in range(num_dupls):
		this_round = int(i / len(image_paths)) + 2
		idx = i % len(image_paths)
		image_path = image_paths[idx]
		dupl_path = basefolder(image_path) + '/' + '_'.join(basename(image_path).split('_')[:-2]) + 'dup' + str(this_round) + '_' + '_'.join(basename(image_path).split('_')[-2:])
		os.system(" ".join(['cp', image_path, dupl_path]))

#balancing class distribution so that training isn't skewed
def balance_classes(training_folder):

	subfolders = get_subfolder_paths(training_folder)
	subfolder_to_images = {subfolder:get_image_paths(subfolder) for subfolder in subfolders}
	subfolder_to_num_images = {subfolder:len(subfolder_to_images[subfolder]) for subfolder in subfolders}

	#get class with the most images
	biggest_size = max(subfolder_to_num_images.values())

	for subfolder in subfolder_to_images:
		image_paths = subfolder_to_images[subfolder]
		duplicate_until_n(image_paths, biggest_size)

	print('balanced all training classes to have', biggest_size, 'images\n')


## main

if __name__ == "__main__":

	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("--input_folder", type=str, help="input folder")
	args = parser.parse_args()
	balance_classes(args.input_folder)






