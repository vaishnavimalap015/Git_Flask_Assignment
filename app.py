import json
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, url_for
from pymongo import MongoClient

# Load variables from .env
load_dotenv()

app = Flask(__name__)

# MongoDB Atlas Connection
mongo_uri = os.getenv("MONGO_URI")

try:
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    db = client["flask_assignment"]
    collection = db["students"]
except Exception as e:
    client = None
    db = None
    collection = None
    print("MongoDB connection error:", e)


# ----------------------------------------------------
# TASK 1: JSON API Route
# ----------------------------------------------------
@app.route("/api")
def api():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)

        return jsonify(data)

    except Exception as e:
        return jsonify({
            "error": "Unable to read data from backend file."
        }), 500


# ----------------------------------------------------
# TASK 2: Frontend Form with MongoDB Atlas
# ----------------------------------------------------

# Form page (GET)
@app.route("/")
def home():
    return render_template("index.html")


# Form submission handler (POST)
@app.route("/submit", methods=["POST"])
def submit():

    # Get data from the form
    name = request.form.get("name")
    email = request.form.get("email")
    course = request.form.get("course")

    try:
        # Check that all fields are filled
        if not name or not email or not course:
            raise ValueError("Please fill in all fields.")

        # Check MongoDB connection
        client.admin.command("ping")

        # Insert data into MongoDB Atlas
        collection.insert_one({
            "name": name,
            "email": email,
            "course": course
        })

        # If successful, redirect to success page
        return redirect(url_for("success"))

    except ValueError as e:

        # Display validation error on the same page
        return render_template(
            "index.html",
            error=f"Error: {str(e)}",
            name=name,
            email=email,
            course=course
        )

    except Exception as e:

        # Display database error on the same page
        return render_template(
            "index.html",
            error="Error: Unable to submit data. Please try again.",
            name=name,
            email=email,
            course=course
        )


# ----------------------------------------------------
# SUCCESS PAGE
# ----------------------------------------------------
@app.route("/success")
def success():
    return render_template("success.html")


# ----------------------------------------------------
# RUN FLASK APPLICATION
# ----------------------------------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )