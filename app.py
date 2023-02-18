from flask import Flask
from flask import render_template, abort, redirect, url_for
from flask import request
from flask import g
import sqlite3

app = Flask(__name__)

def get_message_db():
    try: #returns database if it exists
        return g.message_db
    except: #otherwise creates and returns
        g.message_db = sqlite3.connect("messages_db.sqlite")
        cmd = "CREATE TABLE IF NOT EXISTS messages \
        (id INT, handle TEXT, message TEXT)"
        cursor = g.message_db.cursor()
        cursor.execute(cmd)
        return g.message_db

def insert_message(request):
    #extract form data
    message = request.form["message"]
    handle = request.form["handle"]
    
    with get_message_db() as db:
        #assigns message ID in order of submission
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM messages")
    
        message_id = cursor.fetchone()[0] + 1
        
        #inserts message into database
        cmd = f"INSERT INTO messages (id,handle,message) \
        VALUES ({message_id},'{handle}','{message}')"
        cursor.execute(cmd)
    
        db.commit()
    
def random_messages(n):
    with get_message_db() as db:
        #randomly orders database and fetches first n rows
        #effectively fetches n random rows
        cursor = db.cursor()
        cursor.execute("SELECT handle,message FROM messages \
        ORDER BY RANDOM() LIMIT " + str(n))
        messages = cursor.fetchall()
    
    return messages

@app.route("/",methods=["POST","GET"])
def main():
    #submission page
    if request.method == "GET":
        return render_template("submit.html",submit=False)
    else: 
        #if page refresh after submission, inserts message into db and displays thank you message
        insert_message(request)
        return render_template("submit.html",submit=True)
        
@app.route("/view/")
def view():
    #view page
    to_display = random_messages(5)
    return render_template("view.html",messages=to_display)


        