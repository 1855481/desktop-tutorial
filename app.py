import os
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_migrate import Migrate
from forms import AddForm
######################################
#### SET UP OUR SQLite DATABASE #####
####################################
app = Flask(__name__)
# This grabs our directory

app.config['SECRET_KEY'] = 'MySecret'
basedir = os.path.abspath(os.path.dirname(__file__))
# Connects our Flask App to our Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#OMG SO IMPORTANT TO INCLUDE THIS ABOVE! Warnings up the wazoo if not here on a develoment server.

db = SQLAlchemy(app)
Migrate(app, db)


class Characters(db.Model):

    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    p_name = db.Column(db.Text)
    p_date = db.Column(db.Text)

    def __init__(self, p_name, p_date):
        self.p_name = p_name
        self.p_date = p_date

    def __repr__(self):
        return f"{self.p_name}, {self.p_date}"


@app.route('/characters')
def characters():
    #go to the score table and query it, order it by the score value descending, limit 5 and serve up all of those items I asked for as a list.
    #results = Characters.query.order_by(desc('p_date')).all()
    #dates = []

    #for result in results:
      #  date_dict = {'name': result.p_name, 'date': result.p_date}
      #  dates.append(date_dict)

   # return render_template('list.html', dates=dates)

    mar_char = Characters.query.all()
    return render_template('list.html', mar_char=mar_char)


@app.route('/add-character', methods=['GET', 'POST'])
def add_character():

    form = AddForm()
    if form.validate_on_submit():
        name = form.p_name.data
        date = form.p_date.data
        new_date = Characters(date)
        new_char = Characters(name)
        db.session.add(new_char, new_date)
        db.commit()
        return redirect(url_for('characters'))
    return render_template('add-character.html', form=form)
    #if request.method == 'POST':
      #  name = request.form['name']
      #  date_created = request.form['date_created']

      #  new_character = Characters(name, date_created)
      #  db.session.add(new_character)
      #  db.session.commit()

       # return redirect(url_for('characters', username=name))

   # return render_template('add_character.html')


#debug = True so we can send and see messages to the terminal window so we can see what our code is doing!
if __name__ == '__main__':
    app.run(debug=True)#host and port can be added into parameters
