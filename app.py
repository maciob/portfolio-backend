#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify, Response
from flask_pymongo import PyMongo
import requests
import socket
import json
import os
from flask_cors import CORS, cross_origin
from bson.objectid import ObjectId
import requests

app = Flask(__name__)

app.config["MONGO_URI"] = f"mongodb://{os.environ.get('MONGO_USER')}:{os.environ.get('MONGO_PASS')}@{os.environ.get('MONGO_SERVICE_NAME')}:{os.environ.get('MONGO_PORT')}/{os.environ.get('MONGO_COLLECTION')}?authSource={os.environ.get('MONGO_AUTHSOURCE')}"

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


mongo = PyMongo(app)

def run():
    app.run(host="0.0.0.0")

@app.route("/health", methods=["GET"])
@cross_origin()
def check():
    if request.method == "GET":
        return jsonify(status=200)


@app.route("/api", methods=["GET","POST"])
@cross_origin()
def index():
    if request.method == "GET":
        try:
            output = list(mongo.db.books.find())
            for book in output:
                book["_id"] = str(book["_id"])
            return Response(
                response = json.dumps(output),
                status=200,
                mimetype="application/json"
            )
        except:
            return jsonify(status=500)
    elif request.method == "POST":
        try:
            data = request.get_json()
            Author = data['Author']
            Title = data['Title']
            Year = data['Year']
            conn = mongo.db.books
            output = conn.insert_one({'Author': Author,'Title': Title,'Year': Year})
            return jsonify(status=200)
        except:
            return jsonify(status=500)

@app.route("/api/<ObjectId:id>", methods=["GET","DELETE","PUT"])
@cross_origin()
def book(id):
    if request.method == "GET":
        try:
            output = list(mongo.db.books.find({"_id": id}))
            for book in output:
                book["_id"] = str(book["_id"])
            return Response(
                response = json.dumps(output),
                mimetype="application/json"
            )
        except:
            return jsonify(status=500)
    elif request.method == "DELETE":
        try:
            output = mongo.db.books.delete_one({"_id": id})
            return Response(
                response = json.dumps(output),
                mimetype="application/json"
            )

        except:
            return jsonify(status=500)
    elif request.method == "PUT":
        try:
            data = request.get_json()
            Author = data['Author']
            Title = data['Title']
            Year = data['Year']
            conn = mongo.db.books
            output = conn.update_one({"_id": id},{'$set': {'Author': Author,'Title': Title,'Year': Year} })
            return jsonify(status=200)
        except:
            return jsonify(status=500)

if __name__ == "__main__":
    run()