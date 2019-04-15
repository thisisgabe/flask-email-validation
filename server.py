from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
import re

app = Flask(__name__)
app.secret_key = 'ilikecoolstuffthatisfuntodo'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

def get_emails():
    mysql = connectToMySQL("flask_email_validation")
    return mysql.query_db("SELECT * FROM emails;")

@app.route('/')
def root():
    return render_template("index.html")

@app.route('/success')
def success():
    emails = get_emails()
    print(emails)
    return render_template("result.html", email_list = emails)

@app.route("/submit_email", methods=["POST"])
def add_email_to_db():
    print(request.form)
    if(len(request.form["email"]) < 1):
        flash("Email is not valid!")
    elif not EMAIL_REGEX.match(request.form['email']):    # test whether a field matches the pattern
        flash("Email is not valid!")
    
    query = "INSERT INTO emails (email_address) VALUES (%(email)s);"
    data = {
        "email": request.form["email"]
    }
    if not '_flashes' in session.keys():
        mysql = connectToMySQL("flask_email_validation")
        new_email = mysql.query_db(query, data)
        flash(f"The email address you entered ({request.form['email']}) is a VALID email address! Thank you!")
        return redirect('/success')
    else:
        return redirect('/')

if __name__=="__main__":
    app.run(debug=True)