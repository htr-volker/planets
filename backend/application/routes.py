from application import app, db
from application.models import Planet, Moon
from flask import request, jsonify

@app.route('/create/planet', methods=["POST"])
def create_planet():
    json = request.json
    new_planet = Planet(
        name = json["name"],
        mass = json["mass"],
        type = json["type"],
        star_system = json["star_system"]
    )
    db.session.add(new_planet)
    db.session.commit()
    return f"Planet '{new_planet.name}' added to database"

@app.route('/create/moon/<int:planet_id>', methods=["POST"])
def create_moon(planet_id):
    json = request.json
    new_moon = Moon(
        name = json["name"],
        planet_id = planet_id,
        mass = json["mass"]
    )
    db.session.add(new_moon)
    db.session.commit()
    return f"Moon '{new_moon.name}' added to database"

@app.route('/get/allPlanets', methods=["GET"])
def get_all_planets():
    all_planets = Planet.query.all()
    json = {"planets": []}
    for planet in all_planets:
        moons = []
        for moon in planet.moons:
            moons.append(
                {
                    "id": moon.id,
                    "name": moon.name,
                    "planet_id": moon.planet_id,
                    "mass": moon.mass
                }
            )
        json["planets"].append(
            {
                "id": planet.id,
                "name": planet.name,
                "mass": planet.mass,
                "type": planet.type,
                "star_system": planet.star_system,
                "moons": moons
            }
        )
    return jsonify(json)

@app.route('/get/allMoons', methods=["GET"])
def get_all_moons():
    all_moons = Planet.query.all()
    json = {"moons": []}
    for moon in all_moons:
        json["moons"].append(
            {
                "id": moon.id,
                "name": moon.name,
                "planet_id": moon.planet_id,
                "mass": moon.mass
            }
        )
    return jsonify(json)

@app.route('/get/planet/<int:id>', methods=["GET"])
def get_planet(id):
    planet = Planet.query.get(id)
    return jsonify(
        {
            "id": planet.id,
            "name": planet.name,
            "mass": planet.mass,
            "type": planet.type,
            "star_system": planet.star_system
        }
    )

@app.route('/get/planet/<int:id>/moons', methods=["GET"])
def get_moons(id):
    moons = Planet.query.get(id).moons
    json = {"moons": []}
    for moon in moons:
        json["moons"].append(
            {
                "id": moon.id,
                "name": moon.name,
                "planet_id": moon.planet_id,
                "mass": moon.mass
            }
        )
    return jsonify(json)

@app.route('/update/planet/<int:id>', methods=["PUT"])
def update_planet(id):
    data = request.json
    planet = Planet.query.get(id)
    planet.name = data["name"]
    planet.mass = data["mass"]
    planet.type = data["type"]
    planet.star_system = data["star_system"]
    db.session.commit()
    return f"Planet '{planet.name}' updated successfully"

@app.route('/delete/planet/<int:id>', methods=["DELETE"])
def delete_planet(id):
    planet = Planet.query.get(id)
    db.session.delete(planet)
    return f"Planet '{planet.name}' deleted successfully"