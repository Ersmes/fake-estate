from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required,\
    logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from time import localtime

from helpers import detail, list_for_sale, type_filter, usd, status_filter

import traceback

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///fakeestate.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = b'\xb82\xe2\xballdGW\xa4\xab\x99\xd8\x06\x98,'
db = SQLAlchemy(app)

login_manager = LoginManager(app)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.add_template_filter(type_filter)
app.add_template_filter(usd)
app.add_template_filter(status_filter)


class User (UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    pass_hash = db.Column(db.String, nullable=False)

    saves = db.relationship("Saved", back_populates="user")

    def __repr__(self):
        return "<User(username='%s', pass_hash='%s')>" % \
                (self.username, self.pass_hash)


class Saved (db.Model):
    __tablename__ = "saves"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"),
                        primary_key=True)
    property_id = db.Column(db.String,
                            db.ForeignKey("properties.property_id"),
                            primary_key=True, nullable=False)

    user = db.relationship("User", back_populates="saves")
    property = db.relationship("Property", back_populates="saves")

    def __repr__(self):
        return "<Saved(user_id='%s', property_id='%s')>" % \
                (self.user_id, self.property_id)


class Property (db.Model):
    __tablename__ = "properties"

    property_id = db.Column(db.String, primary_key=True)
    description = db.Column(db.String)
    price = db.Column(db.Integer)
    status = db.Column(db.String)
    type = db.Column(db.String)
    beds = db.Column(db.Integer)
    baths = db.Column(db.Integer)
    city = db.Column(db.String)
    state = db.Column(db.String)
    postal_code = db.Column(db.String)
    lot_size = db.Column(db.Integer)
    units = db.Column(db.String)
    year_built = db.Column(db.Integer)

    saves = db.relationship("Saved", back_populates="property")
    photos = db.relationship("Photo", back_populates="property")


class Photo (db.Model):
    __tablename__ = "photos"

    href = db.Column(db.String, primary_key=True, nullable=False)
    property_id = db.Column(db.String, db.ForeignKey("properties.property_id"),
                            nullable=False)

    property = db.relationship("Property", back_populates="photos")


db.create_all()


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).filter(User.id == user_id).one_or_none()


@app.route("/")
def index():
    timeNum = localtime()
    time = ""

    if timeNum.tm_hour in range(0, 12):
        time = "morning"
    elif timeNum.tm_hour in range(12, 18):
        time = "afternoon"

    if current_user.is_authenticated:
        cities = db.session.query(Property.city, Property.state)\
            .distinct(Property.city, Property.state)\
            .join(Saved)\
            .filter(Saved.user_id == current_user.id).all()
    else:
        cities = []

    return render_template("index.html", time=time, cities=cities)


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":

        city = request.form.get("city")
        state_code = request.form.get("state_code")

        if not len(state_code) == 2 or not state_code.isupper():
            flash("You did not input a valid state code")

            return redirect("/search")

        try:
            properties = list_for_sale(city, state_code)

            return render_template("search_results.html",
                                   properties=properties)
        except Exception:
            flash("Error loading search results, please try again")

            traceback.print_exc()

            return redirect("/search")

    return render_template("search.html")


@app.route("/details/<property_id>")
def details(property_id):
    if (db_property := db.session.query(Property).
       filter(Property.property_id == property_id).one_or_none()) is None:
        property = detail(property_id)

        photos = []

        if "photos" in property:
            for photo in property["photos"]:
                photos.append(Photo(href=photo["href"],
                              property_id=property_id))

        if "lot_size" not in property:
            lot_size = None
            units = None
        else:
            lot_size = property["lot_size"]["size"]
            units = property["lot_size"]["units"]

        saveProperty = Property(property_id=property_id,
                                description=property["description"],
                                photos=photos,
                                price=property["price"],
                                status=property["prop_status"],
                                type=property["prop_type"],
                                beds=property["beds"],
                                baths=property["baths"],
                                city=property["address"]["city"],
                                state=property["address"]["state"],
                                postal_code=property["address"]["postal_code"],
                                lot_size=lot_size,
                                units=units,
                                year_built=property["year_built"])

        db.session.merge(saveProperty)
        db.session.commit()
    else:
        property = {"property_id": db_property.property_id,
                    "description": db_property.description,
                    "photos": db_property.photos,
                    "price": db_property.price,
                    "prop_status": db_property.status,
                    "prop_type": db_property.type,
                    "beds": db_property.beds,
                    "baths": db_property.baths,
                    "address":
                        {"city": db_property.city,
                         "state": db_property.state,
                         "postal_code": db_property.postal_code},
                    "lot_size":
                        {"size": db_property.lot_size,
                         "units": db_property.units},
                    "year_built": db_property.year_built}

    if current_user.is_authenticated:
        saved = not (db.session.query(Saved)
                       .filter(Saved.user_id == current_user.id)
                       .filter(Saved.property_id == property_id)
                       .one_or_none() is None)
    else:
        saved = False

    return render_template("details.html", property=property, saved=saved)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")

        if username == "" or password == "":
            # flash that the form was not filled out completely
            flash("You must provide both a username and a password")

            return redirect("/register")

        if not password == password_confirm:
            flash("The password you input does not match your confirmation")

            return redirect("/register")

        # test validity of password and username, if invalid, frick it up
        # account for blank fields (also do this for /login)
        if not len(db.session.query(User).filter(User.username == username).
                   all()) == 0:
            # flash that the username already exists
            flash("That username is already taken, try another one")

            return redirect("/register")
        else:
            flash("Registration successful")

            newUser = User(username=username,
                           pass_hash=generate_password_hash(password))
            db.session.add(newUser)
            db.session.commit()

            login_user(newUser)

            return redirect("/")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "" or password == "":
            # flash that the form was not filled out
            flash("You must provide both a username and a password")
            return redirect("/login")

        user = db.session.query(User).filter(User.username == username).\
            one_or_none()

        if user is None:
            # flash invalid username
            flash("That username does not exist")

            return redirect("/login")
        elif not check_password_hash(user.pass_hash, password):
            # flash incorrect password
            flash("That password is incorrect")

            return redirect("/login")
        else:
            # implement session logic
            flash("Login successful")

            login_user(user)
            return redirect("/")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    # use notifications instead of flashing messages (same for other
    # successful operations) ???
    flash("Logout successful")

    logout_user()
    return redirect("/")


@app.route("/saved")
@login_required
def saved():
    properties = db.session.query(Property)\
        .join(Saved)\
        .filter(Saved.user_id == current_user.id).all()

    return render_template("view_saved.html", properties=properties)


@app.route("/save", methods=["POST"])
@login_required
def save():
    property_id = request.form.get("property_id")

    query = db.session.query(Saved)\
        .filter(Saved.user_id == current_user.id)\
        .filter(Saved.property_id == property_id)

    if query.one_or_none() is None:
        saved = Saved(user_id=current_user.id, property_id=property_id)

        db.session.merge(saved)
        db.session.commit()

        return "saved"
    else:
        query.delete()
        db.session.commit()

        return "deleted"
