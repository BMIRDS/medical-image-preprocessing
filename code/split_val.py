#Jason Wei
#Split the validation set from the training set
#jason.20@dartmouth.edu

#Fetch all the arguments from the command line
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input_big_folder", type=str, help="input folder")
parser.add_argument("--num_per_class", type=int, help="number to move per class/subfolder")
parser.add_argument("--output_big_folder", type=str, help="output_folder")
args = parser.parse_args()


#Get the paths to the images
import os
from os import listdir
from os.path import isfile, join, isdir
from random import shuffle

#just get the name of images in a folder
def get_image_names(folder):
	image_names = [f for f in listdir(folder) if isfile(join(folder, f))]
	if '.DS_Store' in image_names:
		image_names.remove('.DS_Store')
	image_names = sorted(image_names)
	return image_names

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

#create an output folder if it does not already exist
def confirm_output_folder(output_folder):
	if not os.path.exists(output_folder):
	    os.makedirs(output_folder)

############# Newly written functions #############

#pick a random number of images to move to the validation set
def pick_random_n(my_list, n):
	shuffle(my_list)
	return my_list[:n]

#for a given subfolder in the training set, move the images to the val subfolder
def move_to_val(input_folder, output_folder, n):

	image_names = get_image_names(input_folder)
	val_image_names = pick_random_n(image_names, n)
	for image_name in val_image_names:
		input_path = join(input_folder, image_name)
		output_path = join(output_folder, image_name)
		command = " ".join(['mv', input_path, output_path])
		print(command)
		os.system(command)

#main function
def partition_big_folder(input_big_folder, output_big_folder, n):

	confirm_output_folder(output_big_folder)

	input_subfolders = get_subfolder_paths(input_big_folder)

	for input_subfolder in input_subfolders:
		output_folder = join(output_big_folder, basename(input_subfolder))
		confirm_output_folder(output_folder)

		move_to_val(input_subfolder, output_folder, n)

#execute the code
if __name__ == "__main__":

	partition_big_folder(args.input_big_folder, args.output_big_folder, args.num_per_class)







