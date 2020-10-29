from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date




app = Flask(__name__)
app.secret_key = "Secret Key"

#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["WHOOSH_BASE"]='whoosh'
db = SQLAlchemy(app)


#Creating model table for our CRUD database
class Data(db.Model):
    __searchable__=['name','lastname', 'home', 'email'] 
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    lastname =db.Column(db.String(100))
    home =db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    createdOn = db.Column(db.DateTime)
    updatedOn = db.Column(db.DateTime)
    def __init__(self, name, lastname, home, email, phone,created,updatedOn):

        self.name = name
        self.lastname = lastname
        self.home = home
        self.email = email
        self.phone = phone
        self.createdOn=created





#This is the index route where we are going to
#query on all our employee data
@app.route('/')
def Index():
    all_data = Data.query.all()

    return render_template("index.html", employees = all_data)



#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        name = request.form['name']
        lastname= request.form['lastname']
        home = request.form['home']
        email = request.form['email']
        phone = request.form['phone']
        today = date.today()
        created =today
        updated =''

        my_data = Data(name, lastname, home, email, phone, created,updated)
        db.session.add(my_data)
        db.session.commit()

        flash("Employee Inserted Successfully")

        return redirect(url_for('Index'))


#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET', 'POST'])
def update():
 
    if request.method == 'POST':
       
        my_data = Data.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.lastname = request.form['lastname']
        my_data.home = request.form['home']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
        
        today = date.today()
        my_data.updatedOn= today

        db.session.commit()
        flash("Employee Updated Successfully")

        return redirect(url_for('Index'))




#This route is for deleting our employee
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")

    return redirect(url_for('Index'))


#@app.route('/search/<key>')
#def search(key):
   # my_data = Data.query.get(request.args.get('query'))
   # my_data = Data.query.get(key)
   # return render_template("index.html", employees = my_data)
    # my_data = mysql.connection.cursor()
    # my_data.execute("SELECT * FROM data ")
    # emp=my_data.fetchall()
    # my_data.close()
    # return render_template("index.html", employees = emp)
#@app.route('/search/<key>', methods=['GET', 'POST'])
    
#def search(key):
    #searchForm = searchForm()
    
   # my_data = Data.query.filter(Data.name.like('%' + key + '%'))


   # return render_template('index.html', employees = my_data)


if __name__ == "__main__":
    app.run(debug=True)