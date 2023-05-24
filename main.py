from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)
    
    def __repr__(self):
        return f"<Cafe {self.name}>"

with app.app_context():
    #create a record
    db.create_all()
    
    # newCafe = Cafe(name="akkkk",
    #                map_url="abssshi@google.com", img_url="googffle.com", location="indaaia",
    #                seats="5", has_toilet = True, has_wifi=True, has_sockets=True,
    #                can_take_calls=True, coffee_price=2.5)
    # db.session.add(newCafe)
    # db.session.commit()

# with app.app_context():
#     # read all records
#     Cafe.query.all()

## HTTP GET - Read Record

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/random", methods=['GET'])
def get_random_cafe():
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)
    print(random_cafe)
    return jsonify(cafe={
        "id": random_cafe.id,
        "name": random_cafe.name,
        "map_url": random_cafe.map_url,
        "img_url": random_cafe.img_url,
        "location": random_cafe.location,
        "seats": random_cafe.seats,
        "has_toilet": random_cafe.has_toilet,
        "has_wifi": random_cafe.has_wifi,
        "has_sockets": random_cafe.has_sockets,
        "can_take_calls": random_cafe.can_take_calls,
        "coffee_price": random_cafe.coffee_price,
    })

@app.route("/all")
def get_all_cafes():
    cafes = db.session.query(Cafe).all()
    all_cafes = []
    for cafe in cafes:
        cafe={
        "id":cafe.id,
        "name":cafe.name,
        "map_url":cafe.map_url,
        "img_url":cafe.img_url,
        "location":cafe.location,
        "seats":cafe.seats,
        "has_toilet":cafe.has_toilet,
        "has_wifi":cafe.has_wifi,
        "has_sockets":cafe.has_sockets,
        "can_take_calls":cafe.can_take_calls,
        "coffee_price":cafe.coffee_price,
    }
        all_cafes.append(cafe)
    return jsonify(all_cafes)

@app.route('/search')
def search_cafe():
    query_location = request.args.get("loc")
    cafes_loc = db.session.query(Cafe).filter_by(location = query_location).first()
    if cafes_loc:
        return jsonify(cafe={
        "id":cafes_loc.id,
        "name":cafes_loc.name,
        "map_url":cafes_loc.map_url,
        "img_url":cafes_loc.img_url,
        "location":cafes_loc.location,
        "seats":cafes_loc.seats,
        "has_toilet":cafes_loc.has_toilet,
        "has_wifi":cafes_loc.has_wifi,
        "has_sockets":cafes_loc.has_sockets,
        "can_take_calls":cafes_loc.can_take_calls,
        "coffee_price":cafes_loc.coffee_price,
    })
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})
    
## HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def post_new_cafe():
    new_cafe = Cafe(
    name = request.form.get("name"),
    map_url = request.form.get("map_url"),
    img_url = request.form.get("img_url"),
    location = request.form.get("loc"),
    seats = request.form.get("seats"),
    has_toilet = bool(request.form.get("has_toilet")),
    has_wifi = bool(request.form.get("has_wifi")),
    has_sockets = bool(request.form.get("has_sockets")),
    can_take_calls = bool(request.form.get("can_take_calls")),
    coffee_price = request.form.get("coffee_price")
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response = {"Success": "successfully added a new cafe"})

## HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def patch_update_price(cafe_id):
    new_price = request.args.get("new_price")
    cafe = db.session.query(Cafe).get(cafe_id)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response = {"Success": "Successfully updated the price"})
    else:
        return jsonify(error = {"Not Found": "Sorry cafe with that id not found in the database"})

## HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api_key")
    if api_key == "TopSecretAPIKey":
        cafe = db.session.query(Cafe).get(cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
        else:
            return jsonify(error={"Not found": "Sorry cafe with that id was not found."}), 404
    else:
        return jsonify(error = {"Forbidden": "Sorry, Thats's not allowed. make sure you have correct api_key"}),403

if __name__ == '__main__':
    app.run(debug=True)
