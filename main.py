from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from forms import CreateCafeForm
# from dotenv import load_dotenv ## production
import os  # production

app = Flask(__name__)

# load_dotenv() # production
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # production
# debug mode
##app.config['SECRET_KEY'] = ''

Bootstrap(app)

# ------- create new database ------------#
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db' # development
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL_1','sqlite:///cafes.db') # production
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Cafe(db.Model):
    __tablename__ = "cafe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    map_url = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def __repr__(self) -> str:
        return super().__repr__()


@app.route("/")
def home():
    cafes = Cafe.query.all()
    return render_template('index.html', cafes=cafes)


@app.route('/cafes')
def get_all_cafes():
    cafes = Cafe.query.all()
    return render_template('cafes.html', cafes=cafes)


@app.route('/edit-cafe/<int:cafe_id>', methods=["GET", "POST"])
def edit_cafe(cafe_id):
    cafe = Cafe.query.get(cafe_id)

    edit_form = CreateCafeForm(
        name=cafe.name,
        map_url=cafe.map_url,
        img_url=cafe.img_url,
        location=cafe.location,
        has_sockets=cafe.has_sockets,
        has_toilet=cafe.has_toilet,
        has_wifi=cafe.has_wifi,
        can_take_calls=cafe.can_take_calls,
        seats=cafe.seats,
        coffee_price=cafe.coffee_price
    )

    if edit_form.validate_on_submit():
        cafe.name = edit_form.name.data
        cafe.map_url = edit_form.map_url.data
        cafe.img_url = edit_form.img_url.data
        cafe.location = edit_form.location.data
        cafe.has_sockets = edit_form.has_sockets.data
        cafe.has_toilet = edit_form.has_toilet.data
        cafe.has_wifi = edit_form.has_wifi.data
        cafe.can_take_calls = edit_form.can_take_calls.data
        cafe.seats = edit_form.seats.data
        cafe.coffee_price = edit_form.coffee_price.data

        db.session.commit()
        return redirect(url_for("home"))
    return render_template('edit-cafe.html', form=edit_form)


@app.route('/new-cafe', methods=["GET", "POST"])
def add_new_cafe():
    form = CreateCafeForm()
    if form.validate_on_submit():
        name = form.name.data
        map_url = form.map_url.data
        img_url = form.img_url.data
        location = form.location.data
        socket = form.has_sockets.data
        toilet = form.has_toilet.data
        wifi = form.has_wifi.data
        take_calls = form.can_take_calls.data
        seats = form.seats.data
        price = f"${form.coffee_price.data}"
        print(name, map_url, img_url, location, socket,
              toilet, wifi, take_calls, seats, price)

        new_cafe = Cafe(name=name, map_url=map_url, img_url=img_url,
                        location=location, has_sockets=socket, has_toilet=toilet,
                        has_wifi=wifi, can_take_calls=take_calls,
                        seats=seats, coffee_price=price)
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("add_new_cafe.html", form=form)


@app.route('/delete/<int:cafe_id>')
def delete_cafe(cafe_id):
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
