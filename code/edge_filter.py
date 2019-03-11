import cv2
import numpy as np
from scipy.misc import imsave
from matplotlib import pyplot as plt

image_path = 'data/aje.png'
output_path = 'data/edges.png'

img = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
plt.hist(img.ravel(),256,[0,256]); plt.show()
#edges = cv2.Canny(img,500,600)

# plt.subplot(121),plt.imshow(img,cmap = 'gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(edges,cmap = 'gray')
# plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
imsave(output_path, img)