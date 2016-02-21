
import cv2
import numpy as np
from matplotlib import pyplot as plt

THRESHOLD_TO_BW = 127
BLOCK_SIZE = [5, 10, 15, 20, 25, 30, 40, 45, 50, 60, 75, 90, 100]
#[10, 15, 20, 25, 30, 40, 45, 50, 60, 65, 70, 75, 90]
NUMER_WORDS = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
BORDER = 15
NL_LOGO = 55
ABOVE_THRESHOLD = 255

"""
Trimming related functions
"""
def _trimmer_common(img_character, horiz=True):
    start, end = 0, 0
    dimension1, dimension2 = get_2dimensions(img_character)
    if not horiz:
        # Interchange dimension values
        dimension1, dimension2 = dimension2, dimension1

    for i in xrange(dimension1):
        if horiz:
            _sum = sum([img_character[i,j] for j in xrange(dimension2)])
        else:
            _sum = sum([img_character[j,i] for j in xrange(dimension2)])
        if _sum != (ABOVE_THRESHOLD * dimension2) and start == 0:
                start = i
        elif _sum == (ABOVE_THRESHOLD * dimension2) and start != 0:
                end = i
                break
    if start<end:
    	new_img = img_character[start:end, ]
    	if not horiz:
        	new_img = img_character[0:dimension2, start:end]
    	return new_img
    else :
	return img_character

def horiz_trimmer(img_character):
    return _trimmer_common(img_character)

def vert_trimmer(img_character):
    return _trimmer_common(img_character, horiz=False)

"""
Thresholding function
"""
def threshold(img):
    # value to set when encountering a byte > THRESHOLD_TO_BW
    ret, img_thresh = cv2.threshold(img,
                                THRESHOLD_TO_BW,
                                ABOVE_THRESHOLD,
                                cv2.THRESH_BINARY)
    return img_thresh

"""
File color change related functions
"""
def conv2gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def conv1d_xdr(img):
    return img.reshape(-1)

def conv1d_ydr(img):
    h,w = get_2dimensions(img)
    array = []
    for j in xrange(w):
        array.extend([img[i,j] for i in xrange(h)])
    return array

"""
Dimension related functions
"""
def get_2dimensions(img):
    return img.shape[:2]

"""
Printing related functions
"""
def show_image(img):
    plt.imshow(img, 'gray')
    plt.show()


"""
Fetch a value from a list of tuples
"""
def get_min_filename(val, _list):
    for i in xrange(len(_list)):
        if val == _list[i][1]:
            return _list[i][0]

