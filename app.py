"""Flask app for Cupcakes"""
from flask import abort
import requests
from models import db_connect, Cupcake, db, serialize
from flask import Flask, redirect, render_template, request, jsonify


app = Flask(__name__, static_folder="static")

# Configure app information
app.config['SECRET_KEY'] = 'devwoof0701'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# connect to db
db_connect(app)

app.app_context().push()


# make api routes
@app.route("/api/cupcakes")
def get_all_cupcakes():
    """Retrieve all cupcakes"""
    cupcakes = Cupcake.query.all()
    serialized = [serialize(cupcake) for cupcake in cupcakes]
    return jsonify(cupcakes=serialized)


@app.route("/api/cupcakes/<int:cupcake_id>")
def get_a_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = serialize(cupcake)

    return jsonify(cupcake=serialized)


@app.route("/api/cupcakes", methods=['POST'])
def create_cupcake():
    """Create a new cupcake from received JSON data and return the recreated cupcake"""
    data = request.get_json()

    # Simple validation
    required_fields = ["flavor", "size", "rating", "image"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        abort(400, description=f"Missing required fields: {missing_fields}")

    try:
        rating = float(data["rating"])
    except ValueError:
        abort(400, description="Invalid rating format")

    # Using **data for dynamic field assignment
    new_cake = Cupcake(**data)

    db.session.add(new_cake)
    db.session.commit()

    return jsonify(cupcake=serialize(new_cake)), 201
