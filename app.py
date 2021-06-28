from flask import Flask, render_template, request, redirect, url_for, session
from data import *

app = Flask(__name__)

app.secret_key = 'watubs'

#----------------------------------------Fundamental Display Pages---------------------------------------------------------- #

#Homepage Display
@app.route('/')
def home():
    return render_template("home.html")

#Task Master Page
@app.route("/task")
def task():
    return render_template("task.html")

#Account Registration Page
@app.route('/account/register')
def account_register():
    return render_template("register.html")

#Login Pge
@app.route("/account/login")
def login():
    return render_template("login.html")

#Login Page with an error due to credential access
@app.route("/account_login/failed/retry")
def retry():
    return render_template("retry.html")

#Account Registration Page with an error with an error due to credential access - email is already used
@app.route("/account/creation/failed")
def dupe():
    return render_template("dupe.html")



#----------------------------------------- Handling Functions of the System ---------------------------------------------------#

#Input account credentials into the account database
@app.route('/creating', methods=['POST'])
def account_creation():
    account_data = {'email': request.form['email'].lower(),
                    'password': request.form['password'].lower(),
                    'type': 'Regular'
                    }

    #Checking of email in the database.
    dupe = check_dupe(account_data['email'])
    if dupe is False:
        return redirect(url_for('dupe'))
    else:
        insert_account(account_data)
        return redirect(url_for('home'))

#Verifies login credentials. Success application declares session variables
@app.route("/verifying", methods=['POST'])
def signin():
    account_data = {'email': request.form['email'].lower(),
                    'password': request.form['password'].lower(),
                    'type': 'Regular'
                    }
    verify = login_account(account_data['email'], account_data['password'])

    #Error! Redirects to login failed.
    if verify is False:
        return redirect(url_for('retry'))
    else:
        #Create session data.
        session['loggedin'] = True
        session['id'] = verify['id']
        session['email'] = verify['email']
        session['type'] = verify['type']
        #Redirect to home page
        return redirect(url_for('home'))

#Terminate session variables
@app.route("/accountlogout")
def logout():
    #Remove session data, this will log the users out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('email', None)
   session.pop('type', None)
   #Redirect to login page
   return redirect(url_for('home'))


#-------------------------------------------Membership Application Form-----------------------------------------------------------#

#Application form Page
@app.route("/application/<email>")
@app.route("/application")
def application():
    #Checks if user is logged in.
    #If they are logged in, they can access the form.
    #If not logged in, redirects to login page
    #Admin can view the applications on the masterlist
    if 'loggedin' in session:
        #Checks if the user has already filled out the form
        verify = check_application(session['email'])
        if session['type'] == "Admin":
            return redirect(url_for('masterlist'))
        #If the user has not filled out the form, he will directs to the membership application portal
        elif verify is False:
            return render_template("application.html")
        #If user has already filled out the form, directs to the application review page
        else:
            return render_template('review.html', account=verify)
    else:
        return redirect(url_for('login'))

#Receives data from membership application portal and stores in the database
@app.route('/inputting', methods=['post'])
def apply():
    app_data = {
                'firstname': request.form['firstname'],
                'lastname': request.form['lastname'],
                'sex': request.form['sex'],
                'civil': request.form['marital'],
                'birthdate': request.form['birthdate'],
                'age': request.form['age'],
                'birthplace': request.form['birthplace'],
                'citizenship': request.form['citizen'],
                'religion': request.form['religion'],
                'mobile': request.form['mobilephone'],
                'street1': request.form['street1'],
                'street2': request.form['street2'],
                'city': request.form['city'],
                'state': request.form['state'],
                'country': request.form['country'],
                'url': request.form['imageurl'],
                'apptype': request.form['applicationtype'],
                'advocacy': request.form['advocacy'],
                'email': session['email']
                }
    insert_application(app_data)
    return redirect(url_for('application'))


#----------------------------------------Viewing of the Membership Application Forms--------------------------------------------------------#

#Retreives all membership form from the database and renders the masterlist of applicants
@app.route('/masterlist')
def masterlist():
    application = retreive_masterlist()
    return render_template('masterlist.html', applications=application)

#Shows the Application Review Page
@app.route("/processing/<appid>")
def adminview(appid):
    application = read_app_by_id(appid)
    return render_template('review.html', account=application)

#Receives and returm search query from the masterlist
@app.route('/search', methods=['POST'])
def fieldsearch():
    field = request.form['field']
    search = request.form['search']
    result = field_search(field, search)
    if result is False:
        return render_template('noresult.html')
    else:
        return render_template('searchtoML.html', applications=result)


#----------------------------------------Editing the Application Forms--------------------------------------------------------#

#Receives application data, redirects user to the application's edit page or deletes section.
@app.route('/modify/<email>', methods=['POST'])
def modify(email):
    application = check_application(email)
    if request.form['action'] == 'Edit':
        return render_template('edit.html', account=application)
    elif request.form['action'] == 'Delete':
        delete_application(email)
        return redirect(url_for('application'))

#Upon editing and confirmation of application's data, the values in the database must updated
@app.route('/update/<email>', methods=['POST'])
def update(email):
    app_data = {
        'firstname': request.form['firstname'],
        'lastname': request.form['lastname'],
        'sex': request.form['sex'],
        'civil': request.form['marital'],
        'birthdate': request.form['birthdate'],
        'birthplace': request.form['birthplace'],
        'age': request.form['age'],
        'citizenship': request.form['citizen'],
        'religion': request.form['religion'],
        'mobile': request.form['mobilephone'],
        'street1': request.form['street1'],
        'street2': request.form['street2'],
        'city': request.form['city'],
        'state': request.form['state'],
        'country': request.form['country'],
        'url': request.form['imageurl'],
        'apptype': request.form['applicationtype'],
        'advocacy': request.form['advocacy'],
        'email': email
    }
    update_application(app_data)
    return redirect(url_for('application'))


if __name__ == '__main__':
    app.run(debug=True)