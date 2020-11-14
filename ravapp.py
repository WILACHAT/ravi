#import os

#from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
#from flask_session import Session
#from tempfile import mkdtemp
#from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
#from werkzeug.security import check_password_hash, generate_password_hash


# Configure application
app = Flask(__name__)

@app.route("ravilayout.html")
def ravilayout():
    return render_template("ravilayout.html")


