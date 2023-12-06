"""Flask app for Cupcakes"""
import requests
from models import db_connect, Cupcake, db
from flask import Flask, redirect, render_template, request


app = Flask(__name__, static_folder="static")

# Configure app information
app.config['SECRET_KEY'] = 'devwoof0701'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# connect to db
db_connect(app)
