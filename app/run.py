
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify
import json
import MySQLdb
import MySQLdb.cursors
from settings import *
import requests

app = Flask(__name__)

def get_db():
    """Initializes the database."""
    db = MySQLdb.connect(DB_CONN['HOST'], DB_CONN['USERNAME'], DB_CONN['PASSWORD'], DB_CONN['DATABASE'])
    return db, db.cursor()


@app.route('/', methods=['GET','POST'])
def login ():
	db,cursor=get_db()
	request.form = json.loads(request.data)
	email = request.form['email']
	password = request.form['password']
	cursor.execute('SELECT count(*) FROM user WHERE email="{0}" AND password="{1}"'.format(email,password))
	entries = cursor.fetchall()
	count = entries[0][0]
	if count == 0:
		return jsonify(status='error', msg='Invalid Username or Password')
	else:
		cursor.execute('SELECT username FROM user WHERE email="{0}" AND password="{1}"'.format(email,password))
		entries = cursor.fetchall()
		username = entries[0][0]
		return jsonify(status='success', msg='Login Successfull', username=username)

if __name__=='__main__':
    app.run(debug=True)

