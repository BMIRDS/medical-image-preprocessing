# Medical Image Processing

By [Jason Wei](https://jasonwei20.github.io/)

These are a bunch of functions that I've written over the years for preprocessing medical images. If one of the functions here can save you the hour of searching up documentation/writing code for simple processing tasks, I consider that a win. Contributions are more than welcome. 

## Table of contents
1. compressing a single folder of images
2. compressing a folder of subfolders containing images
3. seeing how many images are in subdirectories in a directory
4. generating a csv file from images sorted by folder
5. randomly moving some files in a folder to another folder
6. anonmyzing all files in a folder

## Dependencies

- PIL `pip install Pillow`
- scipy `pip install scipy`
- cv2 `pip install opencv-python`

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

### 6. Randomly moving *n* files from one folder into another folder (e.g., spliting 10 pics from training to validation set)




### 7. Anonmyzing all files in a folder:


Note that the capacity for this is 26^3 = 17576 images.

The mappings will be stored in a file called `sensitive_mappings.csv` in case you need to convert back at some point.





