from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, validators
from wtforms.validators import DataRequired
import csv
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY")
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired(), validators.Length(min=8, max=120)])
    maps_link = StringField('Cafe Location on Google Maps (URL)', validators=[DataRequired(), validators.URL()])
    opening_time = StringField('Opening Time e.g. 8AM', validators=[DataRequired()])
    closing_time = StringField('Closing Time e.g. 5:30PM', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', validators=[DataRequired()], choices=[('☕'), ('☕☕'), ('☕☕☕'), ('☕☕☕☕'), ('☕☕☕☕☕')])
    wifi_strength = SelectField('Wifi Strength Rating', validators=[DataRequired()], choices=[('✘'),('💪'), ('💪💪'), ('💪💪💪'), ('💪💪💪💪'), ('💪💪💪💪💪')])
    power_socket_availability = SelectField('Wifi Strength Rating', validators=[DataRequired()], choices=[('🔌'), ('🔌🔌'), ('🔌🔌🔌'), ('🔌🔌🔌🔌'), ('🔌🔌🔌🔌🔌')])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    cafe_info = [form.cafe.data, form.maps_link.data, form.opening_time.data, form.closing_time.data, form.coffee_rating.data, form.wifi_strength.data, form.power_socket_availability.data]
    if form.validate_on_submit():
        with open('cafe-data.csv', "a", encoding="utf8") as csv_file:
            csv_file.write("\n")
            csv_data = csv.writer(csv_file)
            csv_data.writerow(cafe_info)
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        print(list_of_rows[1][1])
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
