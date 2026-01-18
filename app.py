from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random, string, validators

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Database Table
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500))
    short_url = db.Column(db.String(10))


# Create DB
with app.app_context():
    db.create_all()


# Generate short URL
def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


# Home Page
@app.route('/', methods=['GET', 'POST'])
def home():
    short_url = None
    error = None

    if request.method == 'POST':
        original_url = request.form['url']

        if not validators.url(original_url):
            error = "Invalid URL"
        else:
            short = generate_short_url()
            new_url = URL(original_url=original_url, short_url=short)
            db.session.add(new_url)
            db.session.commit()
            short_url = request.host_url + short

    return render_template('home.html', short_url=short_url, error=error)


# Redirect Short URL
@app.route('/<short>')
def redirect_url(short):
    data = URL.query.filter_by(short_url=short).first()
    if data:
        return redirect(data.original_url)
    return "URL not found"


# History Page
@app.route('/history')
def history():
    urls = URL.query.all()
    return render_template('history.html', urls=urls)


if __name__ == '__main__':
    app.run(debug=True)