from flask import Flask
from flask_bootstrap import Bootstrap5


def create_app(name=__name__):
    flask = Flask(name)
    Bootstrap5(flask)

    return flask


app = create_app()

from patpat_viewer import viewer


