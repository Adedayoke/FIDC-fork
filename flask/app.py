from flask import Flask, render_template, flash, request, redirect, url_for, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from payment import Pay
from flask_login import UserMixin, login_user, LoginManager, logout_user, login_required, current_user
from status import Verify
from payment import Pay
from forms import LoginForm, PaymentForm, SignupForm
from werkzeug.utils import secure_filename
import os 
import uuid as uuid

#Secrete Token for CSRF so hackers doesen't hijack forms
 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my super secret key' #Created an environment variable to store configurations
#Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#Upload Folder
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#SQLAlchemy Configuration
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ALLOWED_IPS = ['52.31.139.75', '52.49.173.169', '52.214.14.220', '102.88.81.244', '127.0.0.1']


#Some Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = u"Please Login to continue"

@login_manager.user_loader
def user_loader(user_id):
    try:
        user = Users.query.get(int(user_id))
        return user
    except ValueError:
        return None
#Created a User Model



@app.route('/delete/<int:id>')
def delete(id):
    surname = None
    form = SignupForm()
    user_to_delete = Users.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully!!")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("signup.html", form=form, our_users=our_users,surname=surname)
    except:
        flash("Whoops Error Occured")
        return render_template("signup.html", form=form, our_users=our_users, surname=surname)


#Update Database Record

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = SignupForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        surname = request.form['surname']
        lastnames = request.form['lastname']
        middlename = request.form['middlename']
        email = request.form['email']
        matric = request.form['matric']
        gender = request.form['gender']

        name_to_update.surname = surname
        name_to_update.lastname = lastnames
        name_to_update.middlename = middlename
        name_to_update.email = email
        name_to_update.matric = matric
        name_to_update.gender = gender
        try:
            db.session.commit()
            flash("User Updated Successfullys")
            return render_template("update.html", form=form, name_to_update=name_to_update)
        except:
            flash("Error,Try again!!!!")
            return render_template("update.html", form=form, name_to_update=name_to_update)
    else:
        return render_template("update.html", form=form, name_to_update=name_to_update)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    matric_no = None
    password=None
    passed = None
    if request.method == 'POST':
        matric_no = request.form['matric_no']
        password = request.form['password']
        #Clear the forms
        users = Users.query.filter_by(matric=matric_no).first()
        if users is None:
            flash('Invalid Matric or password')
            return render_template('login.html', form=form)
        passed = check_password_hash(users.password_hash, password)
        if passed:
            login_user(users)
            return render_template('login.html', form=form, matric_no=matric_no, users=users)
        else:
            flash('Invalid username or password')
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form, matric_no=matric_no)

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/dashboard/', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = SignupForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)
    payment = Payment.query.filter_by(matric_no=current_user.matric).all()
    if request.method == "POST":
        surname = request.form['surname']
        lastnames = request.form['lastname']
        middlename = request.form['middlename']
        email = request.form['email']
        matric = request.form['matric']
        gender = request.form['gender']
        
        name_to_update.surname = surname
        name_to_update.lastname = lastnames
        name_to_update.middlename = middlename
        name_to_update.email = email
        name_to_update.matric = matric
        name_to_update.gender = gender
        if request.files['profile_pic']:
            profile = request.files['profile_pic']
            
            #Grab Image name
            pic_filename = secure_filename(profile.filename)
            #Set uuid
            pic_name = str(uuid.uuid1()) + '_' + pic_filename
            

            name_to_update.surname = surname
            name_to_update.lastname = lastnames
            name_to_update.middlename = middlename
            name_to_update.email = email
            name_to_update.matric = matric
            name_to_update.gender = gender
            name_to_update.profile = pic_name
            try:
                db.session.commit()
                #Save the image
                profile.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
                flash("User Updated Successfullys")
                return render_template("dashboard.html", form=form, name_to_update=name_to_update)
            except:
                flash("Error,Try again!!!!")
                return render_template("dashboard.html", form=form, name_to_update=name_to_update)
        else:
            db.session.commit()
            flash("User Updated Successfullys")
            return render_template("dashboard.html", form=form, name_to_update=name_to_update)
    else:
        return render_template("dashboard.html", form=form, name_to_update=name_to_update, payments=payment)

@app.route('/') 
def home():
    return render_template('index.html', name='satar')

@app.route('/signup/', methods=['GET', 'POST'])
#requesting for a response directly is Using a GET Method
#Submiting a form is Using a POST Method
def Signup():
    #When the page loads the name is equal to None
    surname = None #Setting a name variable to None 
    form = SignupForm() 
    if form.validate_on_submit():
        users = Users.query.filter_by(email=form.email.data).first()
        if users is None:
            hashed_pw = generate_password_hash(form.password.data)
            users = Users(surname=form.surname.data,email=form.email.data,lastname=form.lastname.data,middlename=form.middlename.data,gender=form.gender.data,
                          matric=form.matric.data, password_hash=hashed_pw)
            db.session.add(users)
            db.session.commit()
        surname = form.surname.data
        form.surname.data =  ''
        form.email.data = ''
        flash("User added Successfully")#Flashing messages to the screen
    our_users = Users.query.order_by(Users.date_added)
    return render_template('signup.html', surname=surname, form=form, our_users=our_users)

@app.route('/paystack/initialize', methods=['GET', 'POST'])
def initialize_paystack_transaction():
    # Get the email and amount from the request data
    form = PaymentForm()
    email = None
    amount = None
    if request.method == 'POST':
        email = request.form['email']
        amount = request.form['amount']
        matric = current_user.matric
        # Initialize payment
        secret_key = "sk_test_7e29975a8c0ab11466d50de28e3c3b29e6cfff85"
        #new_payment = Pay(email, amount, secret_key)
        #transaction_data = new_payment.initialize_transaction()
        #response = transaction_data
        response = {'status': True, 
            'message': 'Authorization URL created', 
            'data': 
            {'authorization_url': 'https://checkout.paystack.com/c8eh8rdqor6xyol', 'access_code': 'c8eh8rdqor6xyol', 
            'reference': 'f4o53g3pm5'}
                }
                
        if response:
            status = str(response['status'])
            message = str(response['message'])
            url = str(response['data']['authorization_url'])
            access_code = str(response['data']['access_code'])
            reference = str(response['data']['reference'])
            users = Payment(reference=reference, access_code=access_code, url=url, message=message,status=status, email=email, amount=amount, matric_no=matric)
            try:
                db.session.add(users)
                db.session.commit()
                flash("User Updated Successfully")
                return render_template("payment.html", form=form, response=response, status=url)
            except:
                flash("Error,Try again!!!!")
                return render_template("payment.html", form=form)    
        else:
            flash("Error,Try again!!!!")
            return render_template('payment.html', email=email, amount=amount, response=response, form=form, status=url)
    else:
        return render_template('payment.html', email=email, amount=amount, form=form)

secret_key = "sk_test_7e29975a8c0ab11466d50de28e3c3b29e6cfff85"
@app.route('/paystack/webhook', methods=['POST'])
def handle_paystack_webhook():
        try:
            event_data = request.get_json()
        except:
            return make_response('Invalid request payload', 400)
        if event_data['event'] == 'charge.success':
            transaction_id = event_data['data']['id']
            # Process the successful transaction to maybe fund wallet and update your WalletModel
            return make_response(f'SUCCESSFUL - {transaction_id}', 200)
        else:
            return make_response('BAD', 404)

@app.route('/verify/<string:reference>')
def verify(reference):
    secret_key = "sk_test_7e29975a8c0ab11466d50de28e3c3b29e6cfff85"
    verify = Verify(reference, secret_key)
    status = verify.status()
    return render_template('test.html', status=status)

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) 
    surname = db.Column(db.String(200), nullable=False)
    lastname = db.Column(db.String(200), nullable=False)
    middlename = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(200), nullable=False)
    matric = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.now())
    password_hash = db.Column(db.String(128))
    profile = db.Column(db.String(128), nullable=True)

    def __repr__(self):
        return f'<Name {self.surname}>'

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(128))
    access_code = db.Column(db.String(128))
    amount = db.Column(db.Integer())
    email = db.Column(db.String(128))
    url = db.Column(db.String(128))
    message = db.Column(db.String(128))
    status = db.Column(db.String(128))
    date_added = db.Column(db.DateTime, default=datetime.now())
    matric_no = db.Column(db.String(128))

if __name__ == '__main__':
    app.run(debug=True, port=4000)