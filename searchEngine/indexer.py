# import the necessary packages
import glob
import os
import descriptor
import csv


dataset = input("Relative Path to the directory that contains the images to be indexed: ")
output = input("Path to where the computed index will be stored: ")

folders = os.listdir(dataset)
for folder in folders:
	index = open (output , "w", newline="")
	indexWriter = csv.writer(index) 
	for imagePath in glob.glob(dataset +"/"+folder+"/*.jpg"):
		imageID = imagePath[imagePath.rfind("/") + 1:]
		features = descriptor.hogDescriptor(imagePath)

		# write the features to file
		indexWriter.writerow([imageID,features,folder,imagePath])
	index.close()
