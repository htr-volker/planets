from application import app
from application.forms import CreatePlanetForm, CreateMoonForm
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

@app.route('/create/moon', methods=["GET", "POST"])
def create_moon():
    form = CreateMoonForm()
    
    json = requests.get(f"http://{backend}/get/allPlanets").json()
    planets = json["planets"]
    for planet in planets:
        form.planet.choices.append((planet["id"], planet["name"]))

    if request.method == "POST":
        response = requests.post(
            f"http://{backend}/create/moon/{form.planet.data}",
            json={
                "name": form.name.data,
                "mass": form.mass.data,
                "planet_id": form.planet.data
            }
        )
        app.logger.info(f"Response: {response.text}")
        return redirect(url_for("home"))

    return render_template("create_moon.html", title="Add Planet", form=form)

