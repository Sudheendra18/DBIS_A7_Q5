from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Meghana@685'
app.config['MYSQL_DB'] = 'iit_indore_users'

# Initialize MySQL
mysql = MySQL(app)

# Secret key for session
app.secret_key = 'your_secret_key'

# Sample courses data
courses = [
    {"code": "CS 203/MA 213", "name":"Data Structures and Algorithms", "credits": 3},
    {"code": "CS 207", "name": "Data Base & Information Systems", "credits": 3},
    {"code": "CS 209", "name": "Logic Design", "credits": 3},
    {"code": "CS 215", "name": "Mathematics for AI and ML", "credits": 3},
    {"code": "CS 253/MA 253", "name": "Mathematics for AI and ML", "credits": 1.5},
    {"code": "CS 257", "name": "Data Base & Information Systems Lab", "credits": 1.5},
    {"code": "MA 205", "name": "Complex Analysis", "credits": 2},
    {"code": "MA 207", "name": "Differential Equations II", "credits": 2},
    {"code": "MA 211/CS 201", "name": "Discrete Mathematical Structures", "credits": 3},
]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE userid = %s", (userid,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[3], password):
            session['userid'] = userid
            flash('Login successful!', 'success')
            return redirect(url_for('welcome'))
        else:
            flash('Login failed. Check your credentials.', 'error')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userid = request.form['userid']
        mobile = request.form['mobile']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO users (userid, mobile, password) VALUES (%s, %s, %s)", 
                        (userid, mobile, hashed_password))
            mysql.connection.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
        except:
            flash('Registration failed. User ID might already exist.', 'error')
        finally:
            cur.close()

    return render_template('register.html')

@app.route('/welcome')
def welcome():
    if 'userid' in session:
        return render_template('welcome.html', userid=session['userid'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('userid', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/courses')
def display_courses():
    if 'userid' in session:
        return render_template('courses.html', courses=courses)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)