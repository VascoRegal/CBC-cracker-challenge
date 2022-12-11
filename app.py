from flask import Flask, request
import os
import random 
import logging

from crypto import AESCipher

app = Flask(__name__)

key = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
cipher = AESCipher(key)
cookie = cipher.encrypt(os.getenv("FLAG"))

@app.route("/hello")
def hello_world():
	request_cookie = request.headers.get("Cookie")

	if not request_cookie:
		return f"You dropped your cookie. Here it is: {cookie.hex()}", 200 

	#try:
	cipher.decrypt(bytes.fromhex(request_cookie))
	#except:
	#	return "Invalid cookie format", 500
	
	return "Hello, World", 200


