from flask import Flask, render_template, redirect, jsonify
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from config import ppwd

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d

username='postgres'
password=ppwd
port=5432
database='parks_db'
connection_str = f"postgresql://{username}:{password}@localhost:{port}/{database}"
engine = create_engine(connection_str)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
# Assign the measurement class to a variable called `Measurement`
Parks = Base.classes.parks

# Create an instance of Flask
app = Flask(__name__)
# app = Flask(__name__, template_folder=".")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all passengers
    results = session.query(Parks).all()

    session.close()

    # Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
    all_parks = []
    for row in results:
        park_dict = row2dict(row)
        all_parks.append(park_dict)

    # Return template and data
    return render_template("index.html", parks=all_parks)

if __name__ == "__main__":
    app.run(debug=True)