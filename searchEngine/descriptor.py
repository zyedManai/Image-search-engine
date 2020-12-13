import cv2 as cv2
from skimage.io import imread, imshow
from skimage.feature import hog
from skimage.transform import resize
import numpy as np
import csv
import ast
import urllib.request as ur
import requests


# METHOD #1: OpenCV, NumPy, and urllib
def url_to_image(url):
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
	resp = ur.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	# return the image
	return image


def hogDescriptor (imagePath):
	image = cv2.imread(imagePath)
	resized_img = resize(image, (128,64)) 
	fd, hog_image = hog(resized_img, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), visualize=True, multichannel=True)
	features = cv2.normalize(fd, fd)
	features= features.flatten()
	features = [float(x) for x in features]
	return features
