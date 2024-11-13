from dotenv import load_dotenv
import os
from flask import Flask, render_template, request, abort, redirect, url_for
from flask_pymongo import PyMongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
load_dotenv()

uri = os.getenv("MONGODB_URI")
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.note_app
notes_collection = db.notes
app = Flask(__name__)
app.config["MONGO_URI"]= uri
mongo = PyMongo(app)

# Home Page with all data
@app.route("/")
def home():
    notes = notes_collection.find()
    return (render_template("home.html", notes=notes))

# Adds post with name, cwid, and body
@app.route("/add", methods=["POST"])
def addNote():
    if "name" in request.form and "CWID" in request.form and "body" in request.form:
        name = request.form["name"]
        CWID = request.form["CWID"]
        body = request.form["body"]
        print("Hello world")
        try:            
            db.notes.insert_one({
                "name": name,
                "CWID": CWID,
                "body": body
            })
    
            return redirect(url_for("home"))
            
        except Exception as e:
            print(e)
            return abort(500)
    return abort(400)

# Deletes note based on id
@app.route("/delete/<note_id>")
def deleteNote(note_id):
    if note_id:
        try:
            notes_collection.delete_one({"_id": ObjectId(note_id)})
            return redirect(url_for("home"))
        except Exception as e: 
            print(e)
    return abort(400)

app.run(debug=True)