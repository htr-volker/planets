from application import app, db
from application.models import Planet, Moon
from flask import request, jsonify
from os import getenv

print(f"CREATE_SCHEMA = {getenv('CREATE_SCHEMA')}")
if getenv("CREATE_SCHEMA").lower() == "true":
    print("Creating table schema")
    db.drop_all()
    db.create_all()

@app.route('/create/planet', methods=["POST"])
def create_planet():
    data = request.json
    new_planet = Planet(
        name = data["name"],
        mass = data["mass"],
        type = data["type"],
        star_system = data["star_system"]
    )
    db.session.add(new_planet)
    db.session.commit()
    return f"Planet '{new_planet.name}' added to database"

@app.route('/create/moon/<int:planet_id>', methods=["POST"])
def create_moon(planet_id):
    data = request.json
    new_moon = Moon(
        name = data["name"],
        planet_id = planet_id,
        mass = data["mass"]
    )
    db.session.add(new_moon)
    db.session.commit()
    return f"Moon '{new_moon.name}' added to database"

@app.route('/get/allPlanets', methods=["GET"])
def get_all_planets():
    all_planets = Planet.query.all()
    json = {"planets": []}
    for planet in all_planets:
        json["planets"].append(
            {
                "id": planet.id,
                "name": planet.name,
                "mass": planet.mass,
                "type": planet.type,
                "star_system": planet.star_system
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

@app.route('/update/planet/<int:id>', methods=["POST"])
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