# BookAlchemy

**BookAlchemy** is a web-based application developed using **Flask**, **SQLAlchemy**, and **SQLite**. It allows users to manage a library of books, including features for adding and deleting authors and books, sorting, and searching books by title or author.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Database Setup](#database-setup)
- [Technologies](#technologies)
- [Folder Structure](#folder-structure)
- [Contributing](#contributing)
- [License](#license)
- [Requirements](#requirements)

---

## Features

- **Add Author**: Allows adding authors to the library database.
- **Add Book**: Allows adding books and linking them to authors (or assigning them to "Unknown Author").
- **View Books**: Displays a list of books with their details, including cover images.
- **Search Books**: Search for books based on the title.
- **Sort Books**: Sort books by title or author.
- **Delete Books and Authors**: Remove books and authors from the database.

---

## Installation

### Prerequisites

- Python 3.x
- pip (Python package manager)

### Installation Steps

1. **Clone the repository**:

   ```bash
   git clone https://github.com/martenzoe/book_alchemy.git
   ```

2. **Create a virtual environment (recommended)**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   .\venv\Scripts\activate  # On Windows
   ```

3. **Install the required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:

   ```bash
   python app.py
   ```

5. Navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser to use the app.

---

## Usage

Once the app is running, you can interact with the application via the following routes:
- **Home** (`/home`): View, search, and sort the list of books.
- **Add Author** (`/add_author`): Add a new author to the database.
- **Add Book** (`/add_book`): Add a new book and link it to an author (or assign it to "Unknown Author").
- **Delete Book** (`/book/<id>/delete`): Remove a book from the database.

The app is responsive and works on mobile devices as well.

---

## Database Setup

To set up the database, follow these steps:

1. Ensure that your `data_models.py` file contains the following models:

   ```python
   from flask_sqlalchemy import SQLAlchemy
   from sqlalchemy import Integer, String, Column, ForeignKey
   from sqlalchemy.orm import relationship

   db = SQLAlchemy()

   class Author(db.Model):
       __tablename__ = "authors"
       author_id = Column(Integer, primary_key=True, autoincrement=True)
       name = Column(String, nullable=False)  # Name cannot be null
       birth_date = Column(String)
       date_of_death = Column(String)
       
       # Relationship to Book
       books = relationship("Book", back_populates="author")

   class Book(db.Model):
       __tablename__ = "books"
       book_id = Column(Integer, primary_key=True, autoincrement=True)
       author_id = Column(Integer, ForeignKey("authors.author_id"), nullable=False)
       isbn = Column(String)
       title = Column(String, nullable=False)  # Title cannot be null
       publication_year = Column(Integer)
       
       # Relationship to Author
       author = relationship("Author", back_populates="books")
   ```

2. In your `app.py`, ensure that you initialize the database and create tables:

   ```python
   with app.app_context():
       db.create_all()
   ```
Important!!! Only run this once for creating the tables, after first run please comment it out:   
with app.app_context():
       db.create_all()

3. Run the application once to create the tables in your SQLite database:

   ```bash
   python app.py
   ```

4. The database will now contain two tables:
   - `authors`: Stores information about authors.
   - `books`: Stores information about books and links them to authors.

---

## Technologies

The following technologies are used in this project:

- **Flask**: Web framework for Python.
- **SQLAlchemy**: ORM (Object Relational Mapping) for interacting with the database.
- **SQLite**: Lightweight database for storing authors and books.
- **HTML/CSS**: Frontend technologies for styling and layout.
- **Jinja2**: Template engine used by Flask.

---

## Folder Structure

```
/BookAlchemy
|-- /static
|   |-- /images
|   |-- library.jpg  # Background image for header (optional)
|-- /templates
|   |-- home.html  # Template for home page (view books)
|   |-- add_author.html  # Template for adding authors
|   |-- add_book.html  # Template for adding books
|-- app.py  # Main Flask application file with routes and logic
|-- data_models.py  # SQLAlchemy models for Author and Book tables
|-- requirements.txt  # List of dependencies required for the project
|-- README.md  # Project documentation (this file)
```

---

## Contributing

Contributions are welcome! If you would like to contribute to BookAlchemy, follow these steps:

1. Fork the repository:

   ```bash
   git clone https://github.com/martenzoe/book_alchemy.git
   ```

2. Create a new branch:

   ```bash
   git checkout -b feature-name
   ```

3. Make your changes.

4. Commit your changes:

   ```bash
   git commit -am 'Add new feature'
   ```

5. Push your branch:

   ```bash
   git push origin feature-name
   ```

6. Open a pull request.

---

## License

This project is licensed under the MIT License – see the LICENSE file for details.

---

## Requirements

The following Python packages are required to run the application:

```
Flask==2.1.1
Flask-SQLAlchemy==2.5.1
SQLAlchemy==1.4.32
```

---

## Notes on `requirements.txt`

To generate or update your `requirements.txt` file with all installed dependencies in your virtual environment, run:

```bash
pip freeze > requirements.txt
```

This will create a file listing all current dependencies needed to run the project.

---

