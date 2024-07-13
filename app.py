from flask import Flask, render_template, url_for ,request,redirect
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

db = SQLAlchemy(app)
    
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500))
    short_url = db.Column(db.String(10), unique=True)
    
def generate_short_url():
    characters = string.ascii_letters + string.digits
    while True:
        short_url = ''.join(random.choices(characters, k=8))
        if not URL.query.filter_by(short_url=short_url).first():
            return short_url

with app.app_context():
    db.create_all()
    

@app.route("/", methods=['POST','GET'])
def index():
    if request.method == "POST":
        original_url = request.form["original-url"]
        short_url = generate_short_url()
        new_url = URL(original_url=original_url, short_url=short_url)
        db.session.add(new_url)
        db.session.commit()
        return render_template('index.html', short_url=short_url)
    else:
        return render_template('index.html')
    

@app.route('/<short_url>')
def redirect_to_url(short_url):
    url = URL.query.filter_by(short_url=short_url).first_or_404()
    return redirect(url.original_url)


if __name__ == "__main__":
    app.run(debug=True)
