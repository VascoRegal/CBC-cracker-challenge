from flask import Flask, request
import os
import random 
import logging

from crypto import AESCipher

app = Flask(__name__)

cipher = AESCipher()
cookie = cipher.encrypt(os.getenv("FLAG"))

@app.route("/cookie")
def fav_cookie():
	return f"[Cookie Monster] -> My favourite cookies look like : {cookie.decode('utf-8')}", 200 

@app.route("/feed")
def feed():
	request_cookie = request.headers.get("Cookie")
	try:
		cipher.decrypt(request_cookie)
	except:
		return "[Cookie Monster] -> Ugh! This cookie is horrible!", 500

	return "[Cookie Monster] -> Hehehehe. Thank you!", 200

