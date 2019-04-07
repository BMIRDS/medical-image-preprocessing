import cv2
import numpy as np
from scipy.misc import imsave
from matplotlib import pyplot as plt
from scipy import ndimage as ndi

from skimage import feature

image_path = 'data/apx.png'
sobel_path = 'data/sobel.png'
edge_path = 'data/edges.png'

img = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
print(img.shape)
print(img[:5, :5])
#plt.hist(img.ravel(),256,[0,256]); plt.show()

sobelx = cv2.Sobel(img,cv2.CV_64F,1,1,ksize=17)
print(sobelx.shape)
imsave(sobel_path, sobelx)

# edge_horizont = ndi.sobel(img, 0)
# edge_vertical = ndi.sobel(img, 1)
# magnitude = np.hypot(edge_horizont, edge_vertical)

# slicecanny = cv2.Canny(sobelx,1,100)
sobel_img = cv2.imread(sobel_path,cv2.IMREAD_GRAYSCALE)
print(sobel_img[0:5, 0:5])
ret,thresh1 = cv2.threshold(sobel_img,115,255,cv2.THRESH_BINARY_INV)
edges = cv2.Canny(sobel_img,120,200)
imsave(edge_path, thresh1)

# plt.subplot(121),plt.imshow(img,cmap = 'gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(edges,cmap = 'gray')
# plt.title('Edge Image'), plt.xticks([]), plt.yticks([])