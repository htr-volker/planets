from application import app
# from application.forms import PlanetForm, MoonForm
from flask import render_template
import requests

@app.route('/', methods=["GET"])
def home():
    planets = requests.get("http://backend/get/allPlanets").json()
    # moons = requests.get("http://backend/get/allMoons")
    return render_template("index.html", planets=planets["planets"])