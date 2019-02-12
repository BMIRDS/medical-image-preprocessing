#Jason Wei
#Anonymize all images in the subfolder
#jason.20@dartmouth.edu

#Fetch all the arguments from the command line
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input_big_folder", type=str, help="input folder")
parser.add_argument("--suffix", type=str, default="png")
args = parser.parse_args()

#Get the paths to the images
import os
from os import listdir
from os.path import isfile, join, isdir

#get subfolders
def get_subfolder_paths(folder):
	subfolder_paths = [join(folder, f) for f in listdir(folder) if (isdir(join(folder, f)) and '.DS_Store' not in f)]
	if join(folder, '.DS_Store') in subfolder_paths:
		subfolder_paths.remove(join(folder, '.DS_Store'))
	subfolder_paths = sorted(subfolder_paths)
	return subfolder_paths

#get 'x' from 'x.jpg'
def file_no_extension(file):
	head = file.split('.')[:-1]
	return "".join(head)

#get full image paths
def get_image_paths(folder):
	image_paths = [join(folder, f) for f in listdir(folder) if isfile(join(folder, f))]
	if join(folder, '.DS_Store') in image_paths:
		image_paths.remove(join(folder, '.DS_Store'))
	image_paths = sorted(image_paths)
	return image_paths

#get 'train_folder/train/o' from 'train_folder/train/o/17asdfasdf2d_0_0.jpg'
def basefolder(path):
	return '/'.join(path.split('/')[:-1])

############# Newly written functions #############

#getting an anonymized name based on the number
def get_alpha_name(number):
	alphas = "abcdefghijklmnopqrstuvwxyz"
	first = int(number / 26 / 26)
	second = int(number / 26) % 26
	third = number % 26
	return alphas[first] + alphas[second] + alphas[third]

#getting all the images names in a big folder with depth 3
def get_all_image_names(input_big_folder):

	all_image_paths = []

	subfolder_paths = get_subfolder_paths(input_big_folder)

	for subfolder_path in subfolder_paths:

		subsubfolder_paths = get_subfolder_paths(subfolder_path)

		for subsubfolder_path in subsubfolder_paths:
			image_paths = get_image_paths(subsubfolder_path)
			all_image_paths += image_paths

	return all_image_paths

#anonymizing all the names
def anonymize(input_big_folder, csv_path, suffix):

	all_image_paths = get_all_image_names(input_big_folder)
	print(len(all_image_paths), "images found")
	writer = open(csv_path, 'w')
	writer.write("sensitive,anon\n")

	for i, old_path in enumerate(all_image_paths):
		folder = basefolder(old_path)
		new_name = get_alpha_name(i)
		new_path = join(folder, new_name+'.'+suffix)

		#rename to anonymize
		command = ' '.join(['mv', old_path, new_path])
		print(command)
		os.system(command)

		#write the mappings to output file
		out_line = old_path + ',' + new_path + '\n'
		writer.write(out_line)

#lets go for it
if __name__ == "__main__":

	csv_path = 'sensitive_mappings.csv'
	anonymize(args.input_big_folder, csv_path, args.suffix)














