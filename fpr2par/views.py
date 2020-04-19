from flask import Flask, render_template, flash, redirect, request
from fpr2par import app, db
from .add_fpr_data import adddata
from datetime import datetime


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/add_fpr_data", methods=["GET"])
def addFPRdata():
    duration = adddata()
    flash("FPR data loaded")
    flash("Import duration: " + duration)

    return render_template("index.html")
