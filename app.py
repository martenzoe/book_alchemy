from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book

# Initialize the Flask app
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/martenzollner/Desktop/new_projects/book_alchemy/data/library.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoid unnecessary warnings

# Bind the database to the app
db.init_app(app)

# Create the tables (run once)
'''with app.app_context():
    db.create_all()'''


if __name__ == '__main__':
    # Run the app in debug mode
    app.run(debug=True)
