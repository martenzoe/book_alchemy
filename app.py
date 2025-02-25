from flask import Flask, render_template, request, redirect, flash
from sqlalchemy.exc import SQLAlchemyError
from data_models import db, Author, Book
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for flash messages

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'data', 'library.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoid unnecessary warnings

# Bind the database to the app
db.init_app(app)

# Create the tables (run once)
with app.app_context():
    db.create_all()

    # Ensure "Unknown Author" exists in the database
    if not Author.query.filter_by(name="Unknown Author").first():
        unknown_author = Author(name="Unknown Author", birth_date=None, date_of_death=None)
        db.session.add(unknown_author)
        db.session.commit()


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Handle adding a new author to the database.

    GET: Render the form to add a new author.
    POST: Process the form data and add the new author to the database.
          Display a success message upon successful addition.
    """
    try:
        if request.method == 'POST':
            # Get data from the form
            name = request.form.get('name')
            birth_date = request.form.get('birthdate')
            date_of_death = request.form.get('date_of_death')

            # Validate input
            if not name:
                flash("Author name is required.", "error")
                return redirect('/add_author')

            # Create a new Author object
            new_author = Author(
                name=name,
                birth_date=birth_date,
                date_of_death=date_of_death if date_of_death else None
            )

            # Add the new author to the database
            db.session.add(new_author)
            db.session.commit()

            # Success message
            flash(f"Author '{name}' was successfully added!", "success")
            return redirect('/add_author')

        # Render the HTML for GET requests
        return render_template('add_author.html')
    except SQLAlchemyError as e:
        flash("A database error occurred while adding the author.", "error")
        print(f"Database error: {e}")
        return redirect('/add_author')
    except Exception as e:
        flash("An unexpected error occurred.", "error")
        print(f"Unexpected error: {e}")
        return redirect('/add_author')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Handle adding a new book to the database.

    GET: Render the form to add a new book and fetch all authors for the dropdown menu.
    POST: Process the form data and add the new book to the database.
          If no author is selected, assign it to "Unknown Author".
          Display a success message upon successful addition.
    """
    try:
        if request.method == 'POST':
            # Get data from the form
            isbn = request.form.get('isbn')
            title = request.form.get('title')
            publication_year = request.form.get('publication_year')
            author_id = request.form.get('author_id')  # Get the selected author's ID

            # Validate input
            if not title:
                flash("Book title is required.", "error")
                return redirect('/add_book')

            # Assign to "Unknown Author" if no author is selected
            if not author_id or author_id == "unknown":
                unknown_author = Author.query.filter_by(name="Unknown Author").first()
                author_id = unknown_author.author_id

            # Create a new Book object
            new_book = Book(
                isbn=isbn,
                title=title,
                publication_year=publication_year,
                author_id=author_id  # Link the book to the selected or default author
            )

            # Add the new book to the database
            db.session.add(new_book)
            db.session.commit()

            # Success message
            flash(f"Book '{title}' was successfully added!", "success")
            return redirect('/add_book')

        # For GET requests, fetch all authors for the dropdown menu
        authors = Author.query.all()
        return render_template('add_book.html', authors=authors)
    except SQLAlchemyError as e:
        flash("A database error occurred while adding the book.", "error")
        print(f"Database error: {e}")
        return redirect('/add_book')
    except ValueError as e:
        flash("Invalid input provided.", "error")
        print(f"Value error: {e}")
        return redirect('/add_book')
    except Exception as e:
        flash("An unexpected error occurred.", "error")
        print(f"Unexpected error: {e}")
        return redirect('/add_book')


@app.route('/home', methods=['GET', 'POST'])
def home():
    """
    Handle displaying the home page with a list of books.

    GET: Fetch books, apply sorting and search filters, then render the home page.
    POST: Process the search keyword to filter books.
          Display an error message if something goes wrong.
    """
    try:
        sort_by = request.args.get('sort_by', 'title')
        search_keyword = request.form.get('search_keyword', '')

        query = Book.query

        if search_keyword:
            query = query.filter(Book.title.ilike(f"%{search_keyword}%"))

        if sort_by == 'author':
            books = query.join(Author).order_by(Author.name).all()
        else:
            books = query.order_by(Book.title).all()

        for book in books:
            if book.isbn:
                book.cover_url = f"https://covers.openlibrary.org/b/isbn/{book.isbn}-L.jpg"
            else:
                book.cover_url = None

        return render_template('home.html', books=books, sort_by=sort_by, search_keyword=search_keyword)
    except SQLAlchemyError as e:
        flash("A database error occurred while loading books.", "error")
        print(f"Database error: {e}")
        return redirect('/home')
    except Exception as e:
        flash("An unexpected error occurred.", "error")
        print(f"Unexpected error: {e}")
        return redirect('/home')


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """
    Handle deleting a book from the database.

    Check if the author has any remaining books. If no books are left, delete the author.
          Display a success message upon successful deletion.
          Handle errors gracefully with an error message.
    """
    try:
        book = Book.query.get_or_404(book_id)
        author = book.author

        db.session.delete(book)
        db.session.commit()

        if not author.books and author.name != "Unknown Author":  # Do not delete default author
            db.session.delete(author)
            db.session.commit()

        flash(f"Book '{book.title}' was successfully deleted!", "success")
        return redirect('/home')
    except SQLAlchemyError as e:
        flash("A database error occurred while deleting the book.", "error")
        print(f"Database error: {e}")
        return redirect('/home')
    except Exception as e:
        flash("An unexpected error occurred.", "error")
        print(f"Unexpected error: {e}")
        return redirect('/home')


if __name__ == '__main__':
    app.run(debug=True)