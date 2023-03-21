################################################################################
################################################################################
########                                                                ########
########   Python - Firebase - Flask Login/Register App                 ########
########   Author: Hemkesh Agrawal                                      ########
########   Website: http://hemkesh.com                                  ########
########   Last updated on: 11/27/2019                                  ########
########                                                                ########
########   P.S. This is my first ever github project, so I              ########
########   would love to hear your feedback : agrawalh@msu.edu          ########
########                                                                ########
################################################################################
################################################################################

import pyrebase
import logging
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for

app = Flask(__name__)       #Initialze flask constructor

#Add your own details
config = {
  "apiKey": "AIzaSyBbKcLEb23CeEe-J8xcxAkuicFGSomUFiM",
  "authDomain": "flask-firebase-1dbe8.firebaseapp.com",
  "databaseURL": "https://flask-firebase-1dbe8-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "flask-firebase-1dbe8",
  "storageBucket": "flask-firebase-1dbe8.appspot.com",
  "messagingSenderId": "451425941911",
  "appId": "1:451425941911:web:811c867df53ad4e1b5ecd2"
}

#initialize firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

#Initialze person as dictionary
person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}

#Login
@app.route("/")
@app.route("/login")
def login():
    return render_template("login.html")

#Sign up/ Register
@app.route("/signup")
def signup():
    return render_template("signup.html")

#Welcome page
@app.route("/welcome")
def welcome():
    if person["is_logged_in"] == True:
        return render_template("welcome.html", email = person["email"], name = person["name"])
    else:
        return redirect(url_for('login'))
    


#If someone clicks on login, they are redirected to /result
@app.route("/result", methods = ["POST", "GET"])
def result():
    if request.method == "POST":        #Only if data has been posted
        result = request.form           #Get the data
        email = result["email"]
        password = result["pass"]
        try:
            #Try signing in the user with the given information
            user = auth.sign_in_with_email_and_password(email, password)
            #Insert the user data in the global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            #Get the name of the user
            data = db.child("users").get()
            person["name"] = data.val()[person["uid"]]["name"]
            #Redirect to welcome page
            return redirect(url_for('welcome'))
        except:
            #If there is any error, redirect back to login
            return redirect(url_for('login'))
    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('login'))

#If someone clicks on register, they are redirected to /register
@app.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == "POST":        #Only listen to POST
        result = request.form           #Get the data submitted
        email = result["email"]
        password = result["pass"]
        name = result["name"]
        try:
            #Try creating the user account using the provided data
            auth.create_user_with_email_and_password(email, password)
            #Login the user
            user = auth.sign_in_with_email_and_password(email, password)
            #Add data to global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            person["name"] = name
            #Append data to the firebase realtime database
            data = {"name": name, "email": email}
            db.child("users").child(person["uid"]).set(data)
            #Go to welcome page
            return redirect(url_for('welcome'))
        except:
            #If there is any error, redirect to register
            return redirect(url_for('register'))

    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('register'))




@app.route("/editProfile", methods = ["POST", "GET"])
def editProfile():
    if request.method == "POST":        #Only listen to POST
        result = request.form           #Get the data submitted
        email = result["email"]
        password = result["pass"]
        name = result["name"]
        height = result["height"]
        weight = result["weight"]
        try:
            #Try creating the user account using the provided data
            #auth.create_user_with_email_and_password(email, password)
            #Login the user
            user = auth.sign_in_with_email_and_password(email, password)
            #Add data to global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            person["name"] = name
            person["weight"] = weight
            person["height"] = height
            #Append data to the firebase realtime database
            data = {"name": name, "email": email, "weight": weight, "height": height}
            db.child("users").child(person["uid"]).set(data)
            #Go to welcome page
            return redirect(url_for('profile'))
        except:
            #If there is any error, redirect to register
            return redirect(url_for('welcome'))

    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('register'))

##If someone clicks on login, they are redirected to /result
#@app.route("/getProfile", methods = ["POST", "GET"])
#def getProfile():
#    if request.method == "POST":        #Only if data has been posted
#        result = request.form           #Get the data
#        email = result["email"]
#        password = result["pass"]
#        try:
#            #Try signing in the user with the given information
#            user = auth.sign_in_with_email_and_password(email, password)
#            #Insert the user data in the global person
#            global person
#            person["is_logged_in"] = True
#            person["email"] = user["email"]
#            person["uid"] = user["localId"]
#            #Get the name of the user
#            #data = db.child("users").get()
#            #person["name"] = data.val()[person["uid"]]["name"]
#            #person["weight"] = data.val()[person["uid"]]["weight"]
#            #person["height"] = data.val()[person["uid"]]["height"]
#            data = db.child("users").child(person["uid"]).get().val()
#            person["name"] = data["name"]
#            person["weight"] = data["weight"]
#            person["height"] = data["height"]
#            #Debugging: print out retrieved data
#            print(data)

#            #Redirect to welcome page
#            return redirect(url_for('profile'))
#        except:
#            #If there is any error, redirect back to login
#            return redirect(url_for('welcome'))
#    else:
#        if person["is_logged_in"] == True:
#            return redirect(url_for('welcome'))
#        else:
#            return redirect(url_for('login'))

#@app.route("/profile")
#def profile():
#    if person["is_logged_in"] == True:
#        return render_template("profile.html", email = person["email"], name = person["name"], weight = person["weight"])
#    else:
#        return redirect(url_for('welcome'))


@app.route("/getProfile", methods = ["POST", "GET"])
def getProfile():
    if request.method == "POST":
        result = request.form
        email = result["email"]
        password = result["pass"]
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            data = db.child("users").child(person["uid"]).get().val()
            person["name"] = data["name"]
            #if "weight" in data:
            #    person["weight"] = data["weight"]
            #if "height" in data:
            #    person["height"] = data["height"]
            person["weight"] = data.get("weight")
            person["height"] = data.get("height")
            logging.info(f"Retrieved profile data from Firebase: {person}")
            return redirect(url_for('profile'))
        except Exception as e:
            logging.error(f"Failed to retrieve profile data from Firebase: {e}")
            return redirect(url_for('welcome'))
    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('login'))

@app.route("/profile")
def profile():
    if person["is_logged_in"] == True:
        return render_template("profile.html", email = person["email"], name = person["name"], weight = person.get("weight"), height = person.get("height"))
    else:
        return redirect(url_for('welcome'))



@app.route("/updateProfile")
def updateProfile():
    return render_template("updateProfile.html")

if __name__ == "__main__":
    app.run()