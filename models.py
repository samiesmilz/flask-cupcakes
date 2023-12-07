"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy

# create database
db = SQLAlchemy()


def db_connect(app):
    db.app = app
    db.init_app(app)

# create the cupcake model


class Cupcake(db.Model):
    __tablename__ = 'cupcakes'

    # set up model attributes to turn into table columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, nullable=False,
                      default="https://tinyurl.com/demo-cupcake")


def serialize(cupcake):
    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }
