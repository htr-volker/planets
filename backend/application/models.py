from application import db

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    mass = db.Column(db.Integer(), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    star_system = db.Column(db.String(50), nullable=False)

    moons = db.relationship('Moon', backref='planet')

class Moon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)
    mass = db.Column(db.Integer(), nullable=False)
