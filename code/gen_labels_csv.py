#Jason Wei
#Generate a csv file with the labels
#jason.20@dartmouth.edu

#Fetch all the arguments from the command line
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input_big_folder", type=str)
parser.add_argument("--output_csv_name", type=str)
args = parser.parse_args()

#Get the paths to the images
import os
from os import listdir
from os.path import isfile, join, isdir

#get '17asdfasdf2d_0_0.jpg' from 'train_folder/train/o/17asdfasdf2d_0_0.jpg'
def basename(path):
	return path.split('/')[-1]

#get 'train_folder/train/o' from 'train_folder/train/o/17asdfasdf2d_0_0.jpg'
def basefolder(path):
	return '/'.join(path.split('/')[:-1])

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

############# Newly written functions #############

#main function
def output_labels_to_csv(input_big_folder, output_csv_name):
	writer = open(output_csv_name, 'w')
	writer.write('img,class\n')

	subfolder_paths = get_subfolder_paths(input_big_folder)
	for subfolder_path in subfolder_paths:

		image_paths = get_image_paths(subfolder_path)
		for image_path in image_paths:
			image_name = basename(image_path)
			image_class = basename(basefolder(image_path))
			out_line = image_name + ',' + image_class
			writer.write(out_line + "\n")


#smoke 'em
if __name__ == "__main__":
	output_labels_to_csv(args.input_big_folder, args.output_csv_name)






