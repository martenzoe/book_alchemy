from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship

# Initialize SQLAlchemy
db = SQLAlchemy()

# Author model
class Author(db.Model):
    __tablename__ = "authors"

    # Columns for the "authors" table
    author_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)  # Name cannot be null
    birth_date = Column(String)
    date_of_death = Column(String)

    # Relationship to Book
    books = relationship("Book", back_populates="author")

    def __repr__(self):
        """Official representation of the object (for debugging)"""
        return f"Author(id={self.author_id}, name={self.name})"

    def __str__(self):
        """User-friendly representation (for print/str)"""
        return self.name

# Book model
class Book(db.Model):
    __tablename__ = "books"

    # Columns for the "books" table
    book_id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey("authors.author_id"), nullable=False)
    isbn = Column(String)
    title = Column(String, nullable=False)  # Title cannot be null
    publication_year = Column(Integer)

    # Relationship to Author
    author = relationship("Author", back_populates="books")

    def __repr__(self):
        """Official representation of the object (for debugging)"""
        return f"Book(id={self.book_id}, title={self.title})"

    def __str__(self):
        """User-friendly representation (for print/str)"""
        return self.title
