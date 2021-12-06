from application import app
from application.routes import backend
from flask import url_for
from flask_testing import TestCase
import requests_mock

test_data = {
    "id": 1,
    "name": "Test Planet 1",
    "mass": 12345,
    "type": "Gas Giant",
    "star_system": "Test Star System",
    "moons": [
        {
            "id": 1,
            "mass": 500,
            "name": "Test Moon",
            "planet_id": 1
        }
    ]
}

class TestBase(TestCase):

    def create_app(self):
        app.config.update(
            DEBUG=True,
            WTF_CSRF_ENABLED=False
        )
        return app

class TestViews(TestBase):

    def test_home_get(self):
        with requests_mock.Mocker() as m:
            m.get(f"http://{backend}/get/allPlanets", json={'planets': []})
            response = self.client.get(url_for('home'))
            self.assert200(response)

    def test_home_create_planet(self):
        response = self.client.get(url_for('create_planet'))
        self.assert200(response)

class TestHome(TestBase):

    def test_home_read_planets(self):
        with requests_mock.Mocker() as m:
            m.get(f"http://{backend}/get/allPlanets", json={'planets': [test_data]})
            response = self.client.get(url_for('home'))
            self.assertIn("Test Planet 1", response.data.decode("utf-8"))
    
class TestCreatePlanet(TestBase):

    def test_create_planet_form_post(self):
        with requests_mock.Mocker() as m:
            m.post(f"http://{backend}/create/planet", text="Test response")
            m.get(f"http://{backend}/get/allPlanets", json={'planets': [test_data]})
            response = self.client.post(url_for('create_planet'), follow_redirects=True)
            self.assertIn("Test Planet 1", response.data.decode("utf-8"))

class TestCreateMoon(TestBase):

    def test_create_moon_form_post(self):
        with requests_mock.Mocker() as m:
            m.post(f"http://{backend}/create/moon/1", text="Test response")
            m.get(f"http://{backend}/get/allPlanets", json={'planets': [test_data]})
            response = self.client.post(url_for('create_planet'), follow_redirects=True)
            self.assertIn("Test Planet 1", response.data.decode("utf-8"))
