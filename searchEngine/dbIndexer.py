# import the necessary packages
import glob
import os
from cv2 import cv2
from skimage.io import imread, imshow
from skimage.feature import hog
from skimage.transform import resize
import descriptor
import searcher
import psycopg2
import numpy as np
from pymongo import MongoClient
from bson.objectid import ObjectId
from sklearn.cluster import KMeans
import pandas as pd
from sklearn.cluster import KMeans
import ast

# Chi-2 distance metric
def distance(histA, histB, eps = 1e-10):
	# compute the chi-squared distance
	d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
		for (a, b) in zip(histA, histB)])
	# return the chi-squared distance
	return d 

dataset = " "
index_path = " "

#MongoDB
client=MongoClient('mongodb://localhost:27017/images')
db=client.images
collection=db.hogClusters
collection2=db.hogDescriptors

#Read hogDescriptors from indexed CSV
data = pd.read_csv(index_path, sep=",", header=None)
hog_features = data[1]
array_edge=hog_features.apply(lambda row: np.array(ast.literal_eval(row)))
a = np.array(array_edge.values.tolist())

#Calculate Centroids
Kmeans=KMeans(n_clusters=15, n_init=20).fit(a)
Clusters=Kmeans.predict(a)
centroids = Kmeans.cluster_centers_

#Create collections for centroids
for i in range (0, len(centroids)):
    line_DB={"centroid":centroids[i].tolist(), "images" : []}
    collection.insert_one(line_DB)

#Create hogdescriptor collection
folders = os.listdir(dataset)
for folder in folders:
    for imagePath in glob.glob(dataset + "/"+folder+"/*.jpg"):
        imageID = imagePath[imagePath.rfind("/") + 1:]
        features = descriptor.hogDescriptor(imagePath)
       
        #strore hog descriptors in sepearate collection and reference if inside hogClusters
        collection2.insert_one({"id": imageID, "hogDescriptor": features, "localPath": imagePath})

#Reference each image in correspoding cluster
for document in collection2.find():
    
    id = document["_id"]
    features = collection2.find_one({"_id" : ObjectId(id)})['hogDescriptor']

    #find out the closest centroid to the picture
    d_min = abs(distance(features, centroids[0]))
    i_cluster = 0
    for i in range (1, len(centroids)):
        d_tmp = abs(distance(features, centroids[i]))
        if (d_tmp<d_min):
            d_min = d_tmp
            i_cluster = i
    try:
        #collection.update_one({"centroid" : centroids[i_cluster].tolist()}, {"$push": {"images":{"id": imageID, "hogDescriptor": str(features), "localPath": imagePath}}})
        collection.update_one({"centroid" : centroids[i_cluster].tolist()}, {"$push": {"images":{"hogref_id": id}}})
    except:
        print ("error image ",id)
        continue

