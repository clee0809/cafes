from flask_wtf import FlaskForm
from wtforms import * #StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL, Email

class CreateCafeForm(FlaskForm):
    name = StringField("Cafe Name", validators=[DataRequired()])
    map_url = StringField("Map URL", validators=[DataRequired(), URL()])
    img_url = StringField("Image URL", validators=[DataRequired(), URL()])
    location = StringField("Location (City)", validators=[DataRequired()])
    has_sockets = BooleanField("Does this cafe have sockets?")
    has_toilet = BooleanField("Does this cafe have toilet?")
    has_wifi = BooleanField("Does this cafe have WIFI?")
    can_take_calls = BooleanField("Can I take calls?")
    seat_choices =['1-10', '10-20','20-30','30-40','40-50','50+']
    # seat_choices =[('10','1-10'), ('20','10-20'), ('30','20-30'), ('40','30-40'), ('50','40-50'), ('60','50+')]
    seats = SelectField("Number of seats", choices=seat_choices)
    coffee_price = StringField("Price of plain coffee e.g. $5.99", validators=[DataRequired()])
    submit = SubmitField("Submit")
   