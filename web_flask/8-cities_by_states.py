#!/usr/bin/python3
"""
    This script starts a Flask web app
"""
from models import storage
from models.state import State
from flask import Flask, render_template


app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def states_list():
    """ a route to get all states from db storage """
    states = storage.all(State).values()
    return render_template("8-cities_by_states.html", states=states)


@app.teardown_appcontext
def close(exc):
    """ remove current sqlalchemy session after each request """
    storage.close()


if __name__ == "__main__":
    storage.reload()
    app.run(host="0.0.0.0", port=5000)
