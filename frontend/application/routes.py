from application import app
from application.forms import CreatePlanetForm
from flask import render_template, request, redirect, url_for
import requests
from os import getenv

backend = getenv("BACKEND_HOSTNAME")

@app.route('/', methods=["GET"])
def home():
    planets = requests.get(f"http://{backend}/get/allPlanets").json()["planets"]
    return render_template("index.html", title="Home", planets=planets)

@app.route('/create/planet', methods=["GET", "POST"])
def create_planet():
    form = CreatePlanetForm()

    if request.method == "POST":
        response = requests.post(
            f"http://{backend}/create/planet",
            json={
                "name": form.name.data,
                "mass": form.mass.data,
                "type": form.type.data,
                "star_system": form.star_system.data
            }
        )
        app.logger.info(f"Response: {response.text}")
        return redirect(url_for("home"))

    return render_template("create_planet.html", title="Add Planet", form=form)

@app.route('/create/moon')
def create_moon():
    return redirect(url_for('home'))
