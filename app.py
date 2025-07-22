from MySQLdb.cursors import DictCursor
from flask import Flask, render_template, request , redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Tamil$93'
app.config['MYSQL_DB'] = 'dummy'

mysql = MySQL(app)

# user form
@app.route('/')
def index():

    return render_template('home.html')

# user table
@app.route('/table')
def table():

    cursor = mysql.connection.cursor()
    cursor.execute("select * from register")
    user = cursor.fetchall()
    return render_template('table.html' , users = user)

#user update
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        email = request.form.get('email').strip().lower()
        mobilenumber = request.form.get('mobilenumber')
        course = request.form.get('course')

        # check same email

        cursor = mysql.connection.cursor()
        cursor.execute("select * from register where email=%s and id !=%s", (email,id))
        result = cursor.fetchall()

        if result:
            return "Already  registered use another email "

        # check same number

        cursor.execute("select * from register where mobilenumber=%s and id !=%s", (mobilenumber, id))
        res = cursor.fetchall()

        if res:
            return "Already registered use another number "

        else:
            cursor = mysql.connection.cursor()

        cursor.execute("""
             UPDATE register
             SET name         = %s,
                 age          = %s,
                 gender       = %s,
                 email        = %s,
                 mobilenumber = %s,
                 course       = %s
             WHERE id = %s
             """, (name, age, gender, email, mobilenumber, course, id))

        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('table'))
    # to get form
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM register WHERE id = %s", (id,))
    user = cursor.fetchone()

    return render_template('update.html', user=user,use=user)

@app.route('/edit/<int:id>' ,methods =['GET','POST'])
def edit(id):

    return redirect(url_for('update', id=id))

#delete user
@app.route('/delete/<int:id>' ,methods =['GET','POST'])
def delete(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM register WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('table'))

#user submit
@app.route('/submit',methods=['POST','GET'])
def submit():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        email = request.form.get('email').strip().lower()
        mobilenumber = request.form.get('mobilenumber')
        course = request.form.get('course')

        # check same email

        cursor = mysql.connection.cursor()
        cursor.execute("select * from register where email=%s", (email,))
        result = cursor.fetchall()

        if result:
            return "Already  registered use another email "

        # check same number

        cursor.execute("select * from register where mobilenumber=%s", (mobilenumber,))
        res = cursor.fetchall()

        if res:
            return "Already registered use another number "

        else:
            cursor = mysql.connection.cursor()

        cursor.execute("""insert into register (name,age,gender,email,mobilenumber,course)
                           values (%s, %s, %s, %s, %s, %s)""", (name, age, gender, email, mobilenumber, course))

        mysql.connection.commit()
        cursor.close()

        return redirect('/table')

    return "register success"


if __name__ == '__main__':
    app.run(debug=True)