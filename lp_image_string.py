import sys
import os
import ntpath
import itertools
import time

import cv2
import numpy as np
from matplotlib import pyplot as plt

import glob
import string
import cPickle as pickle
from collections import Counter
from collections import OrderedDict

import util

"""
Function for feature array construction
Feature array represents characters as an array of +1 and -1's
"""
def filterfn(val1, val2):
    if val1 < val2:
        return +1
    return -1

"""
Function which takes in an image and returns the characters
Vertical projection histogram for image segmentation
"""
def segment_characters(img):
    height, width = util.get_2dimensions(img)
    # Find the sum of pixels in each column of image
    colsum = []
    for j in range(width):
        cols = sum([img[i, j] for i in xrange(height)])
        colsum.append(cols)

    vertical_pixel_count = [i for i in xrange(width) if colsum[i] != util.ABOVE_THRESHOLD * height]

    # Find the start and end value where the vertical_pixel_count is continuous
    # This is analogous to finding the vertical projection histogram values
    vertical_projection_range = OrderedDict()
    n = 0
    for each_pix_count in vertical_pixel_count:
        if each_pix_count-n in vertical_projection_range:
            vertical_projection_range[each_pix_count-n] = each_pix_count
            n += 1
        else:
            vertical_projection_range[each_pix_count] = each_pix_count
            n = 1

    string = []
   # Segment characters based on the vertical_projection_range
    feature_vector = []
    for start in vertical_projection_range:
        end = vertical_projection_range[start]
        img_character = img[0 : height, start-1 : end+2]
        h, w = util.get_2dimensions(img_character)
        value = 1.5
        temp_sum_rows = sum([1 for j in xrange(w) if img_character[h/value, j] == 0])
        if temp_sum_rows :
            # Removes the rows and columns in the image that are completely white pixels
            img_hor_trim = util.horiz_trimmer(img_character)
            img_vert_trim = util.vert_trimmer(img_hor_trim)
            cv2.imwrite("/home/archana/LPR/codes/extracted/ltr-" + str(start) + ".jpg", img_vert_trim)
            # Calls function to find feature array
            lp_character_feature(img_vert_trim)
            # Calls function to idenfity the character from hte feature array
            char = identify_character()
            string.append(char)
    return string

"""
Function to find the feature array of character in x and y direction
Converts the image to one dimensional array in both directions
"""
def lp_character_feature(img):
    img_resize = cv2.resize(img, (30,60))
    img_1d = util.conv1d_xdr(img_resize)
    feature(img_1d, 0)
    img_y_1d = util.conv1d_ydr(img_resize)
    feature(img_y_1d, 1)

"""
Function which partitions the 1D array into blocks of pixels
Blocks array has the elements as the sum of pixels in each block
Feature array is formed from the blocks array
"""
def feature(img_1d, dr):
    for each in util.BLOCK_SIZE:
        partition = [sum(img_1d[i:i+each]) for i in xrange(0,len(img_1d), each)]
        feature = [filterfn(partition[i+1],partition[i]) for i in xrange(len(partition)-1)]
        pickle.dump(feature, open( "/home/archana/LPR/codes/extracted/feat"+str(each)+"_"+str(dr)+".txt", "wb" ) )

"""
Function to find the count of the predicted values
Most common prediction is assumed to be correct character prediction
"""
def identify_character():
    min_file = []
    min_file.extend(min_character(0))
    min_file.extend(min_character(1))
    count_of_files = Counter(min_file)
    if sys.argv[-1] == "-d":
        print count_of_files
    return count_of_files.most_common()[0][0]

def min_character(dr):
    path = "/home/archana/LPR/codes/std/"
    min_file = []
    filenames = glob.glob(os.path.join(path,"*.jpg")) + glob.glob(os.path.join(path,"*.png"))

    for each in util.BLOCK_SIZE :
        std = pickle.load( open( "/home/archana/LPR/codes/extracted/feat"+str(each)+"_"+str(dr)+".txt", "rb" ) )
        features = []
        for filename in filenames:
            img = cv2.imread(filename)
            img = util.conv2gray(img)
            height, width = util.get_2dimensions(img)
            img_thresh = util.threshold(img)
            img_hor_trim = util.horiz_trimmer(img_thresh)
            img_vert_trim = util.vert_trimmer(img_hor_trim)
            img_resize = cv2.resize(img_vert_trim, (30,60))
            if dr == 0:
                img_1d = util.conv1d_xdr(img_resize)
            elif dr == 1:
                img_1d = util.conv1d_ydr(img_resize)
            partition = [sum(img_1d[i : i+each]) for i in xrange(0,len(img_1d), each)]
            feature = [filterfn(partition[i+1],partition[i]) for i in xrange(len(partition)-1)]
            features.append(feature)
        diff = [(sum((x-y)**2 for x,y in zip(std, temp))) for temp in features]
        files =  [ntpath.basename(each) for each in filenames]
        _list = zip(files, diff)
        min_file.append(util.get_min_filename(min(diff), _list))
    return min_file

def character_integer(char_string):
    value = dict(zip(util.NUMER_WORDS, xrange(0,10)))
    char_int_map = {key:value for (key,value) in zip(string.ascii_uppercase, xrange(10,36))}
    char_int = map(lambda x : char_int_map[x] if x in string.ascii_uppercase else value[x], char_string)
    if sys.argv[-1] == "-d":
        print "Integers representing characters\n", char_int
    lp_value = sum([2**(i*6) * each for each,i in zip(char_int, xrange(len(char_int)-1,-1,-1))])
    return lp_value

def main():
    img = cv2.imread(sys.argv[1])
    if sys.argv[-1] == "-d":
        print "The license plate is : ", sys.argv[1].split("_")[0], "\n Predicting the characters of plate :"
    img = util.conv2gray(img)
    img_thresh = util.threshold(img)
    if sys.argv[-1] == "-d":
        util.show_image(img_thresh)
    height, width = util.get_2dimensions(img_thresh)

   # if sys.argv[2] == "0":
     #   img_resize = img_resize[util.BORDER : height-util.BORDER,
     #                     util.NL_LOGO : width - util.BORDER]

    string = segment_characters(img_thresh)
    string = [each.split(".")[0] for each in string]
    if sys.argv[-1] == "-d":
        print "\nIdentified characters of license plate \n", string
    lpr_value = character_integer(string)
    if sys.argv[-1] == "-d":
        print "Concatenated integer"
    print lpr_value

if __name__ == '__main__':
    main()
