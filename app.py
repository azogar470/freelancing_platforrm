from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "your_secret_key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Define User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    description = db.Column(db.Text)

@login_manager.user_loader
def load_user(user_id):
    if user_id.isdigit():
        return User.query.get(int(user_id))
    return None

@app.route("/")
def home():
    return render_template('welcome.html')

@app.route("/home")
def hello_world():
    return render_template('front.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for("dashboard"))

        return "Invalid credentials!"
    
    return render_template("loginpage.html")

@app.route("/aboutus")
def about():
    return render_template("aboutus.html")

@app.route("/registermid")
def midR():
    return render_template("registermid.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        full_name = request.form["full_name"]
        phone = request.form.get("phone", "")
        description = request.form.get("description")



        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return "User already exists!"

        new_user = User(username=username, password=password, email=email, full_name=full_name, phone=phone, description=description)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))
    
    return render_template("register.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return f"Hello, {current_user.full_name} ({current_user.username})! Email: {current_user.email} <a href='/logout'>Logout</a>"

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
