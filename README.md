# Medical Image Processing

By [Jason Wei](https://jasonwei20.github.io/)

These are a bunch of functions that I've written over the years for preprocessing medical images. If one of the functions here can save you the hour of searching up documentation/writing code for simple processing tasks, I consider that a win. Contributions are more than welcome. For high-res medical image classification, see my repository [DeepSlide](https://github.com/BMIRDS/deepslide).

## Table of contents
1. compressing a single folder of images
2. compressing a folder of subfolders containing images
3. seeing how many images are in subdirectories in a directory
4. generating a csv file from images sorted by folder
5. randomly moving some files in a folder to another folder
6. anonmyzing all files in a folder
7. **svs to png**
8. duplicate files to balance the class distribution of a folder:
9. delete files in a validation folder until all folders have at most *n* images:
10. clean whitespace in a folder of images

## Dependencies

- PIL: `pip install Pillow`
- scipy: `pip install scipy`
- cv2: `pip install opencv-python`

### 1. Compressing a single folder of images:
Compressing a single folder of images called `x` by `2` into an output folder called `y`:
```
python code/compress_single_folder.py --input_folder=x --output_folder=y --compression_factor=2
```

### 2. Compressing a folder with subfolders containing images:
Compressing a folder with subfolders of images called `x` by `8` into an output folder called `y`:
```
python code/compress_big_folder.py --input_big_folder=x --output_big_folder=y --compression_factor=8
```

### 3. Seeing how many images are in each subdirectory in a directory:
```
du -a | cut -d/ -f2 | sort | uniq -c | sort -nr
```

### 4. Generating a csv file from images sorted by folder:
Generate a csv file for `wsi_train` to `labels_train.csv`
```
python code/gen_labels_csv.py --input_big_folder=wsi_train --output_csv_name=labels_train.csv
```


### 5. Randomly moving *n* files from one folder into another folder (e.g., spliting 10 pics from training to validation set)
Grabbing a validation set from a folder with subfolders of images called `x`, with `7` from each subfolder into an output folder called `y`:
```
python code/split_val.py --input_big_folder=x --output_big_folder=y --num_per_class=5
```


### 6. Anonmyzing all files in a folder:
Note that this does not retain the data, so you should make a back-up of this. For example, if your folder `x` has `wsi_train`, `wsi_val`, and `wsi_test`, each with subfolders by class containing images, do:
```
python code/anonymize.py --input_big_folder=x
```
Note that the capacity for this is 26^3 = 17576 images. The mappings will be stored in a file called `sensitive_mappings.csv` in case you need to convert back at some point.


### 7. svs to png:
Compress your `svs` images and convert them to `png` at the same time. Note that since you can't load an entire SVS image into memory, you will have to tile it and then piece it together. For an input folder with svs images `x`, convert to `png` and compress by `2`
```
python code/svs_to_png.py --input_folder=x --output_folder=y_pieces --compression_factor=2
python code/repiece_png_tiles.py --input_folder=y_pieces --output_folder=y --compression_factor=2
```

### 8. Duplicate files to balance the class distribution of a folder:
Your training images are in `train`, such that `train/a` has your images for acinar, `train/l` has your images for lepidic, etc. To balance the training distribution to the class with the max number of images, run:
```
python code/balance_train.py --input_folder=train
```

### 9. Delete files in a validation folder until all folders have at most *n* images:
If you have too many images in a validation folder `val`, you can delete some of them randomly until each class has at most `500` images. To balance a validation distribution, run:
```
python code/cut_val.py --input_folder=val --num_val=500
```

### 10. Clean whitespace in a folder of images:
If there is extraneous whitespace outside of images, it will be deleted. This also pads the image by adding "whitespace" to the edges of size `w=224`, so that when you use sliding window you can also cover the edges of an image during visualization. 
```
python code/clean_whitespace.py --input_folder=test_folder --output_folder=test_folder_clean
```









