import os
from flask import Flask, render_template, request, jsonify, send_file
from descriptor import hogDescriptor
from pymongo import MongoClient
from bson.objectid import ObjectId
import numpy as np
import descriptor as descriptor

#MongoDB
client=MongoClient('mongodb://localhost:27017/images')
db=client.images
collection=db.hogClusters
collection2=db.hogDescriptors

# Chi-2 distance metric
def distance(histA, histB, eps = 1e-10):
	# compute the chi-squared distance
	d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
		for (a, b) in zip(histA, histB)])
	# return the chi-squared distance
	return d 

app = Flask(__name__)

#Receive a File 
@app.route("/search",methods=['GET','POST'])
def search():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            image.save("../downloads/image.jpg")
            #return jsonify("uploaded")
        
        # load the query image and describe it
        features = descriptor.hogDescriptor ("../downloads/image.jpg")

        #find the nearest centroid
        d_min = abs(distance(features, collection.find_one()["centroid"]))
        for document in collection.find():
            d_tmp = abs(distance(features, document["centroid"]))
            if (d_tmp<d_min):
                d_min = d_tmp
                i_cluster = document["_id"] 
        
        #find the closest image:  
        images = collection.find_one({"_id": ObjectId(i_cluster)})["images"]
        
        #Return the 10 most closest images
        results = {}
        for image in images:
            im_id = image["hogref_id"]
            im_hog = collection2.find_one({"_id": ObjectId(im_id)})["hogDescriptor"]
            im_path = collection2.find_one({"_id": ObjectId(im_id)})["localPath"]
            d = abs(distance(features,im_hog))
            results[im_path] = d

        results = sorted([(v, k) for (k, v) in results.items()])
        return jsonify(results[:10])
        #for (distance, path) in results[:10]:
        #    print(path)        


if __name__ == '__main__':
    app.run(debug=True)