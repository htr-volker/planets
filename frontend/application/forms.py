from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

class CreatePlanetForm(FlaskForm):
    name = StringField('Planet Name', validators=[DataRequired()])
    mass = IntegerField('Planet Mass', validators=[DataRequired()])
    type = SelectField('Planet Type', validators=[DataRequired()],
        choices=[
            ('Dwarf', 'Dwarf'),
            ('Terrestrial', 'Terrestrial'),
            ('Ice Giant', 'Ice Giant'),
            ('Gas Giant', 'Gas Giant')
        ]
    )
    star_system = StringField('Star System Name', validators=[DataRequired()])
    submit = SubmitField('Add Planet')

class CreateMoonForm(FlaskForm):
    name = StringField('Moon Name', validators=[DataRequired()])
    mass = IntegerField('Moon Mass', validators=[DataRequired()])
    planet = SelectField('Orbiting Planet', validators=[DataRequired()], choices=[])
    submit = SubmitField('Add Moon')
