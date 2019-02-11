# medical_image_processing
Functions for pre-processing large images

By [Jason Wei](https://jasonwei20.github.io/)

## Dependencies

### Compressing a single folder of images:

Compressing a single folder of images called `x` by `2` into an output folder called `y`:
```
python code/compress_single_folder.py --input_folder=x --output_folder=y --compression_factor=2
```

### Compressing a folder with subfolders containing images:

Compressing a folder with subfolders of images called `x` by `8` into an output folder called `y`:
```
python code/compress_big_folder.py --input_big_folder=x --output_big_folder=y --compression_factor=8
```

### Anonmyzing all files in a folder:


Note that the capacity for this is 26^3 = 17576 images.

The mappings will be stored in a file called `sensitive_mappings.csv` in case you need to convert back at some point.

### Randomly moving *n* files from one folder into another folder (e.g., spliting 10 pics from training to validation set)


### Seeing how many images are in each subdirectory in a directory:

```
du -a | cut -d/ -f2 | sort | uniq -c | sort -nr
```

