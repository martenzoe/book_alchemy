from flask import Flask, render_template, request, redirect
from data_models import db, Author, Book

# Initialize the Flask app
app = Flask(__name__)

# Configure the SQLite database
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/martenzollner/Desktop/new_projects/book_alchemy/data/library.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoid unnecessary warnings

# Bind the database to the app
db.init_app(app)

# Create the tables (run once)
with app.app_context():
    db.create_all()


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Handle adding a new author to the database.

    GET: Render the form to add a new author.
    POST: Process the form data and add the new author to the database.
    """
    if request.method == 'POST':
        # Get data from the form
        name = request.form.get('name')
        birth_date = request.form.get('birthdate')
        date_of_death = request.form.get('date_of_death')

        # Create a new Author object
        new_author = Author(
            name=name,
            birth_date=birth_date,
            date_of_death=date_of_death if date_of_death else None  # Handle empty input
        )

        # Add the new author to the database
        db.session.add(new_author)
        db.session.commit()

        # Redirect to the same page after adding the author
        return redirect('/add_author')

    # Render the HTML for GET requests
    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Handle adding a new book to the database.

    GET: Render the form to add a new book and fetch all authors for the dropdown menu.
    POST: Process the form data and add the new book to the database.
    """
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

        # Add the new book to the database
        db.session.add(new_book)
        db.session.commit()

        # Redirect to the same page after adding the book
        return redirect('/add_book')

    # For GET requests, fetch all authors for the dropdown menu
    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)


@app.route('/home', methods=['GET', 'POST'])
def home():
    """
    Handle displaying the home page with a list of books.

    GET: Fetch books, apply sorting and search filters, then render the home page.
    POST: Process the search keyword to filter books.
    """
    # Standardwerte für Sortierung und Suche
    sort_by = request.args.get('sort_by', 'title')
    search_keyword = request.form.get('search_keyword', '')

    # Basisabfrage für Bücher
    query = Book.query

    # Filter hinzufügen, wenn ein Suchbegriff eingegeben wurde
    if search_keyword:
        query = query.filter(Book.title.ilike(f"%{search_keyword}%"))

    # Sortierung anwenden
    if sort_by == 'author':
        books = query.join(Author).order_by(Author.name).all()
    else:
        books = query.order_by(Book.title).all()

    # Dynamische Cover-URLs generieren
    for book in books:
        if book.isbn:
            book.cover_url = f"https://covers.openlibrary.org/b/isbn/{book.isbn}-L.jpg"
        else:
            book.cover_url = None  # Fallback für fehlende ISBN

    # Bücher und Suchbegriff an das Template übergeben
    return render_template('home.html', books=books, sort_by=sort_by, search_keyword=search_keyword)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """
    Handle deleting a book from the database.

    Check if the author has any remaining books. If no books are left, delete the author.
    """
    # Suche das Buch in der Datenbank
    book = Book.query.get_or_404(book_id)

    # Speichere den Autor des Buchs
    author = book.author

    # Lösche das Buch
    db.session.delete(book)
    db.session.commit()

    # Prüfe, ob der Autor noch weitere Bücher hat
    if not author.books:  # Wenn die Liste leer ist
        db.session.delete(author)
        db.session.commit()

    # Erfolgsnachricht und Weiterleitung zur Homepage
    return redirect('/home')


if __name__ == '__main__':
    # Run the app in debug mode
    app.run(debug=True)
