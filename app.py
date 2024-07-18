from flask import Flask, request, render_template,redirect,url_for,flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mysqldb import MySQL # It allows Flask applications to interact with MySQL databases.
from flask_bcrypt import Bcrypt # Bcrypt is a password hashing library used for securely hashing passwords before storing them in a database.

import uuid  # For generating unique tokens, universally unique identifiers (UUIDs)
import smtplib  # smtplib is a module used for sending emails using the Simple Mail Transfer Protocol (SMTP).
from email.mime.text import MIMEText  # MIMEText is a class for creating email message objects with plain text content.
from email.mime.multipart import MIMEMultipart  # MIMEMultipart is a class for creating email message objects with multiple parts, such as both plain text and HTML content.

import numpy as np ## This line imports the NumPy library and assigns it the alias 'np'. Numpy ia a fundamental package for numerical computing in Python, provading support for large multi-dimensional arrays and matrices, along with a collection of mathematical funcation to operate on these array.

import pandas # This line imports the pandas library , Pandas is a powerful data manipulation and analysis library for Python.

import sklearn # scikit-learn is a machine learning library for Python that provides simple and efficent tools for data mining and data analysis. The 'metrics' module contains various metrics for evaluating the performance of machine learning models.

import pickle   # pickle is used for serializing and deserializing Python objects, effectively converting them into byte streams for storage or transmission. In this case, it's loading a pre-trained Random Forest model from a file.

import warnings  ## This line imports the warnings module, which provides a mechanism to control the behavior of warnings in Python code.

''' 
{%...%} condations, for loops
{{   }} expressions to print output
{#...#} this is for comments
'''

warnings.filterwarnings("ignore", category=DeprecationWarning) # In this case, it's ignoring warnings of the DeprecationWarning category,

model = pickle.load(open('models/RandomForest.pkl','rb')) #This line loads a machine learning model from a file named 'RandomForest.pkl' 

app = Flask(__name__) #Here, you're creating an instance of the Flask class and assigning it to the variable app
app.secret_key = "4949skjdjfdjfjfkfkksd" #This line sets the secret key for the Flask application.It's important for security purposes, such as protecting against cross-site request forgery (CSRF) attacks. 

#These lines configure the MySQL database connection settings for the Flask application
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'flask'

mysql = MySQL(app) #Here, you're creating an instance of the MySQL class,passing the Flask application instance app to it.allowing the Flask application to interact with the MySQL database.
bcrypt = Bcrypt(app) #This line creates an instance of the Bcrypt class from the Flask-Bcrypt extension and passes the Flask application instance app to it. allowing you to use Bcrypt for password hashing and verification within your Flask application.

login_manager = LoginManager() #These lines initialize the LoginManager instance login_manager and associate it with the Flask application instance app.The LoginManager manages the user authentication system in Flask applications. 
login_manager.init_app(app)

#User Loader funcation
@login_manager.user_loader #This is a decorator used to register a user loader function    
                           # with the login_manager. 
def load_user(email): 
    return User.get(email)
#the user_loader callback is used to reload the user object from the    user ID stored in the session,load_user that takes an email as an argument and returns the corresponding User object. This function is used by Flask-Login to retrieve the user object based on the user's email.

class User(UserMixin):
    def __init__(self, user_id,name, email):  
        self.id = user_id
        self.name = name
        self.email = email

        #This defines a User class that inherits from UserMixin, which is provided by Flask-Login. The UserMixin class provides default implementations for the methods required by the user model. Inside the User class, you're defining an __init__ method to initialize the user object with user_id, name, and email attributes. This class represents the user model in your application.
     
       
 

    @staticmethod  #This decorator is used to declare a method as a static method within the User class. Static methods in Python are methods that are bound to the class rather than the instance of the class. They can be called on the class itself without needing an instance.
    def get(user_id):
        cursor = mysql.connection.cursor() #Here, you're obtaining a cursor object from the MySQL connection using the cursor() method. The cursor object allows you to execute SQL queries and fetch data from the database.

        cursor.execute('select name, email from users where id = %s',(user_id,)) #This line executes an SQL query to select the name and email columns from the users table where the id matches the provided user_id. The %s placeholder is used for parameterized queries to prevent SQL injection attacks. The user_id value is passed as a parameter to the query.

        result = cursor.fetchone() #After executing the query, this line fetches the row of the result set returned by the query and assigns it to the result variable. 

        cursor.close() #This line closes the cursor object to release the database resources. 

        if result: #This conditional block checks if result contains any data. 

            return User(user_id, result[0],result[1]) #This method essentially retrieves a user from the database based on the provided user_id and returns a corresponding User object.




@app.route('/') # THis is decoreater its use for create a url.
def index1():
    return render_template('index1.html') #This route decorator binds the URL '/' to the index1() function. When a user navigates to the root URL of your website (e.g., http://yourdomain.com/), Flask will call the index1() function, which renders the index1.html template using the render_template function.

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/features.html')
def features():
    return render_template('features.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/det.html')
def det():
    return render_template('det.html')

@app.route('/login', methods = ['GET','POST']) #The route decorator binds the URL '/login' to the 'login()' function and specifies that this route should respond to both GET and POST requests.

def login():
    if request.method == 'POST': #This condition checks if the incoming request method is POST. If it is, it means that the user has submitted the login form.
        
        email = request.form['email'] #These lines extract the email and password entered 
        password = request.form['password'] #by the user from the form submitted with the POST request.
        cursor = mysql.connection.cursor()
        cursor.execute('select id,name,email, password from users where email = %s', (email,))
        user_data = cursor.fetchone()
        cursor.close()
        if user_data and bcrypt.check_password_hash(user_data[3], password): #This condition checks if 'user_data' contains any data (i.e., if a user with the provided email exists in the database) and if the provided password matches the hashed password stored in the database. It uses 'bcrypt.check_password_hash()' to compare the provided password with the hashed password retrieved from the database.

            user = User(user_data[0],user_data[1],user_data[2]) #If the email and password are valid, a new User object is created using the user's id, name, and email retrieved from the database. Then, this user is logged in using 'login_user(user)', which is a function provided by Flask-Login for logging in users.

            login_user(user)
            flash('login successfully insert the data and predict the crop', 'success') #A flash message is added to provide feedback to the user that they have successfully logged in. The 'success' category is used for styling purposes.

            return render_template('new.html') #If the login is successful, the user is redirected to the 'new.html' template,

        else:
            flash('Invalid email or password. Please try again.', 'error') #If the provided email or password is invalid, a flash message is added to inform the user that their login attempt was unsuccessful.

      
    return render_template('login.html')



@app.route('/signup', methods = ['GET','POST']) #The route decorator binds the URL '/signup' to the 'signup()' function and specifies that this route should respond to both GET and POST requests.

def signup():
    if request.method == 'POST': #This condition checks if the incoming request method is POST. If it is, it means that the user has submitted the signup form.
       
        name = request.form['name'] #These lines extract the name, email, and password entered by the user from 
        email = request.form['email'] #the form submitted with the POST request.
        password = request.form['password']

        # Check if email already exists in the database
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM users WHERE email = %s', (email,)) #If the provided email already exists in the database (i.e., count > 0), a flash message is added to inform the user that the email is already taken. The user is redirected back to the signup page using 'redirect(url_for('signup'))'.
        count = cursor.fetchone()[0]
        cursor.close()
        if count > 0:
            flash('Email already taken. Please choose a different email.', 'error')
            return redirect(url_for('signup'))
    

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') #Unicode Transformation Format - 8 bits.Unicode is a character set. It translates characters to numbers.
        cursor = mysql.connection.cursor()
        cursor.execute('insert into users (name,email,password) values(%s,%s,%s)',(name,email,hashed_password))
        mysql.connection.commit() #After validating the email, a new record is inserted into the 'users' table in the database with the provided name, email, and hashed password.
        cursor.close()
        flash('Account created successfully. You can now login.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route("/predict",methods=['GET','POST']) #This route decorator binds the URL '/predict' to the 'predict()' function and specifies that this route should respond only to POST requests. Additionally, 

#the @login_required decorator ensures that only authenticated users can access this route.
@login_required
def predict():

    N = request.form['Nitrogen'] #These lines extract the input data (Nitrogen, Phosphorus, Potassium,  
    P = request.form['Phosporus'] #Temperature, Humidity, pH, Rainfall) submitted via the POST request form.
    k = request.form['Potassium']
    temperature = request.form['Temperature']
    humidity = request.form['Humidity']
    ph = request.form['Ph']
    rainfall = request.form['Rainfall']

    N = float(N)
    P = float(P)
    k = float(k)
    temperature = float(temperature)
    humidity = float(humidity)
    ph = float(ph)
    rainfall = float(rainfall)

    if (N >0 and N <= 140) and  (P >0 and P <= 145) and  (k >0 and k <= 205) and  (temperature >0 and temperature <= 44) and  (humidity	>=0 and humidity <= 100) and  (ph >=0 and ph <= 10) and  (rainfall >=0 and rainfall <= 221):

         feature_list = [N,P,k,temperature,humidity,ph,rainfall] #Here, you're constructing a feature list containing the input data, which is then converted into a NumPy array and reshaped into the required format (1 sample, multiple features) for making predictions.

         features = np.array([[feature_list]]).reshape(1, -1) #Reshaping a dataset using reshape(1, -1) typically means converting a multi-dimensional array into a one-dimensional array, organized as a single row.

         prediction = model.predict(features)[0]
         print(prediction)
     
         crop_list = ["rice", "maize", "jute", "cotton", "coconut", "papaya", "orange",
                  "apple", "muskmelon", "watermelon", "grapes", "mango", "banana",
                  "pomegranate", "lentil", "blackgram", "mungbean", "mothbeans",
                  "pigeonpeas", "kidneybeans", "chickpea", "coffee"]
     
       
         if prediction in crop_list:
        
             result = "{} is a best crop to be cultivated. ".format(prediction)
    else:
        result = "Sorry, we could not determine the best crop to be cultivated with the provided data."
     
         # return render_template('crop.html',result = result)
    flash('Check the result.', 'succes')
    return render_template('new.html',result = result)
   


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('logout successful see you soon.', 'success')
    return redirect(url_for('index1'))


@app.route('/forgot_password', methods=['GET', 'POST'])  #This route decorator binds the URL '/forgot_password' to the 'forgot_password()' function and specifies that this route should respond to both GET and POST requests.
def forgot_password():                 #This function handles the logic for resetting a forgotten password.
    if request.method == 'POST':       #This condition checks if the incoming request method is POST. If it is, it means that the user has submitted the forgot password form.
        email = request.form['email']  #This line retrieves the email address entered by the user from the form submitted with the POST request.
        
        # Check if the email exists in the database
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT id FROM users WHERE email = %s', (email,)) #Here, you're querying the database to check if the provided email exists in the 'users' table. It executes an SQL SELECT statement to fetch the user's id based on the provided email. Then, it fetches the id using 'fetchone()' and stores it in 'user_id'.
        user_id = cursor.fetchone()
        cursor.close()

        if user_id:  #This condition checks if 'user_id' contains any data (i.e., if a user with the provided email exists in the database).
            # Generate a unique token for password reset
            token = str(uuid.uuid4())  #A unique token is generated for password reset using uuid.uuid4().

            # Save the token in the database
            cursor = mysql.connection.cursor()
            cursor.execute('UPDATE users SET reset_token = %s WHERE id = %s', (token, user_id[0]))
            mysql.connection.commit()
            cursor.close() #The generated token is saved in the database for the user with the corresponding id, allowing them to reset their password later.



            # Send email with password reset link
            send_reset_email(email, token) #An email containing the password reset instructions, including the unique token, is sent to the user's email address.
            flash('Password reset instructions have been sent to your email.', 'success')
        else:
            flash('Email address not found. Please try again.', 'error')

    return render_template('forgot_password.html')

def send_reset_email(email, token): #This function send_reset_email(email, token) is responsible for sending an email containing the password reset instructions to the provided email address with a unique token for password reset. Let's break down the logic:
    # Email sending logic goes here
    # Example using SMTP
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'abcd@gmail.com'
    sender_password = '*** *** *** ***'
    receiver_email = email  #This line sets the receiver's email address to the provided email parameter.

    message = MIMEMultipart()       #Here, you're creating an instance of MIMEMultipart() to compose the email 
    message['From'] = sender_email  #message. You set the sender, receiver, and subject of the email.
    message['To'] = receiver_email
    message['Subject'] = 'Password Reset Request'
                                                         #This is the body of the email message, which contains the password reset instructions along with the unique token. The token is appended to the reset password URL as a query parameter.

    body = f"""
    To reset your password, click the following link:     
    http://localhost:5000/reset_password?token={token}
    """

    message.attach(MIMEText(body, 'plain')) #The body of the email message is attached to the message object as plain text.

    with smtplib.SMTP(smtp_server, smtp_port) as server:  # This block establishes a connection to the SMTP server,
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)

@app.route('/reset_password', methods=['GET', 'POST']) #This route decorator binds the URL '/reset_password' to the 'reset_password()' function and specifies that this route should respond to both GET and POST requests.
def reset_password():                                  #This function handles the logic for resetting the 
                                                        #user's password.
    if request.method == 'POST':                      #This condition checks if the incoming request method is POST. If it is, it means that the user has submitted the reset password form.
        # Extract the token and new password from the form submission
        token = request.form['token']
        new_password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validate the new password and confirm password match
        if new_password != confirm_password:

              flash('Passwords do not match. Please try again.', 'error')
              return render_template('login.html')
        # Verify the token and update the user's password in the database
        else:
           cursor = mysql.connection.cursor()
           cursor.execute('SELECT id FROM users WHERE reset_token = %s', (token,)) #Here, you're querying the database to check if the provided token exists in the 'reset_token' column of the 'users' table. It executes an SQL SELECT statement to fetch the user's id based on the provided token. Then, it fetches the id using 'fetchone()' and stores it in 'user'.
           user = cursor.fetchone()
           cursor.close()

        if user: #This condition checks if 'user' contains any data (i.e., if a user with the provided token exists in the database).
            # Hash the new password
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8') #Here, you're generating a hashed version of the new password using Bcrypt's 'generate_password_hash()' function. The hashed password is decoded to UTF-8 format before storing it in the database.

            # Update the user's password and clear the reset token
            cursor = mysql.connection.cursor()
            cursor.execute('UPDATE users SET password = %s, reset_token = NULL WHERE id = %s',(hashed_password, user[0])) 
            #This block updates the user's password in the database with the new hashed password and clears the reset token associated with the user.
            mysql.connection.commit()
            cursor.close() 

            flash("Password reset successful. You can now login with your new password.", "success")
            return redirect(url_for('login'))
        else:
            flash("Invalid or expired token. Please request a new password reset.", "error")
            return redirect(url_for('forgot_password'))

        
     


    token = request.args.get('token') #This line retrieves the token value from the URL query parameters.
    return render_template('reset_password.html', token=token) #If the request method is GET or if there was an issue with the reset password form submission, the user is redirected back to the 'reset_password.html' template to display the reset password form again, with the token value passed to the template.

@app.after_request 
def add_header(response): 
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response   ##This function, decorated with @app.after_request, adds headers to the response to prevent caching. This is useful for ensuring that sensitive information, such as user authentication status, is not cached by the browser.
                             
@login_manager.unauthorized_handler   #This function specifies what happens when a user tries to access a protected route without being logged in. In this case, it adds a flash message to inform the user that they must be logged in to access the page and redirects them to the login page.
def unauthorized():
    flash('You must be logged in to access this page.', 'error')
    return redirect(url_for('login'))
      
if __name__ == "__main__":
            app.run(debug=True)

            #This conditional statement ensures that the Flask application is only run if the script is executed directly, not if it's imported as a module into another script. When the script is executed directly, the Flask application starts running in debug mode (debug=True), which provides helpful debugging information in case of errors.
