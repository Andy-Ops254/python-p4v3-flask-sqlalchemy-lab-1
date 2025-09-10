# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def earthquakes(id):
    query = Earthquake.query.filter_by(id=id).first()
    if query:
        body = {
            "id":query.id,
            "location": query.location,
            "magnitude": query.magnitude,
            "year": query.year
        }
        return make_response(body, 200)
    else:
        body = {
            "message": f"Earthquake 9999 not found."
        }
        return make_response(body, 404)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def quakes (magnitude):
    query = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()   
    quakes = [
            {
                "id":quake.id,
                "location": quake.location,
                "magnitude":quake.magnitude,
                "year":quake.year
            } 
            for quake in query
            ]
    count = len(quakes)

    if query:
        body = {
            "count": count,
            "quakes": quakes
        }
        return make_response(body, 200)
    else:
        body = {
            "count":0,
            "quakes":[]
        }
        return make_response(body,200)

if __name__ == '__main__':
    app.run(port=5556, debug=True)
