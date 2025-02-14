from flask import Flask, render_template, request, redirect
from data_models import db, Author, Book

# Initialize the Flask app
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/martenzollner/Desktop/new_projects/book_alchemy/data/library.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoid unnecessary warnings

# Bind the database to the app
db.init_app(app)

# Create the tables (run once)
with app.app_context():
    db.create_all()

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        # Get data from the form
        name = request.form.get('name')
        birth_date = request.form.get('birthdate')
        date_of_death = request.form.get('date_of_death')

        # Create new Author object
        new_author = Author(
            name=name,
            birth_date=birth_date,
            date_of_death=date_of_death if date_of_death else None  # Handle empty input
        )

        # Add new author to the database
        db.session.add(new_author)
        db.session.commit()

        # Redirect to the same page after adding the author
        return redirect('/add_author')

    # Render the HTML for GET requests
    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        # Get data from the form
        isbn = request.form.get('isbn')
        title = request.form.get('title')
        publication_year = request.form.get('publication_year')
        author_id = request.form.get('author_id')  # Get the selected author's ID

        # Create a new Book object
        new_book = Book(
            isbn=isbn,
            title=title,
            publication_year=publication_year,
            author_id=author_id  # Link the book to the selected author
        )

        # Add new book to the database
        db.session.add(new_book)
        db.session.commit()

        # Redirect to the same page after adding the book
        return redirect('/add_book')

    # For GET requests, fetch all authors for the dropdown menu
    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)


@app.route('/home', methods=['GET'])
def home():
    # Query all books from the database
    books = Book.query.all()

    # Generate cover URLs for each book
    for book in books:
        if book.isbn:
            book.cover_url = f"https://covers.openlibrary.org/b/isbn/{book.isbn}-L.jpg"
        else:
            book.cover_url = None  # Fallback, falls keine ISBN vorhanden ist

    # Render the home.html template with the books data
    return render_template('home.html', books=books)


if __name__ == '__main__':
    # Run the app in debug mode
    app.run(debug=True)
