from flask import Flask
from flask import render_template, abort, redirect, url_for
from flask import request
from flask import g
import sqlite3

app = Flask(__name__)

def get_message_db():
    try:
        return g.message_db
    except:
        g.message_db = sqlite3.connect("messages_db.sqlite")
        cmd = "CREATE TABLE IF NOT EXISTS messages \
        (id INT, handle TEXT, message TEXT)"
        cursor = g.message_db.cursor()
        cursor.execute(cmd)
        return g.message_db

def insert_message(request):
    message = request.form["message"]
    handle = request.form["handle"]
    
    with get_message_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM messages")
    
        message_id = cursor.fetchone()[0] + 1
    
        cmd = f"INSERT INTO messages (id,handle,message) \
        VALUES ({message_id},'{handle}','{message}')"
        cursor.execute(cmd)
    
        db.commit()
    
    return [message,handle]
    
def random_messages(n):
    with get_message_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT handle,message FROM messages \
        ORDER BY RANDOM() LIMIT " + str(n))
        messages = cursor.fetchall()
    
    return messages

@app.route("/",methods=["POST","GET"])
def main():
    if request.method == "GET":
        return render_template("submit.html",submit=False)
    else:
        insert_message(request)
        return render_template("submit.html",submit=True)
        
@app.route("/view/")
def view():
    to_display = random_messages(5)
    return render_template("view.html",messages=to_display)


        