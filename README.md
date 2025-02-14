# BookAlchemy

**BookAlchemy** is a web-based application developed using **Flask**, **SQLAlchemy**, and **SQLite**. It allows users to manage a library of books, including features for adding and deleting authors and books, sorting, and searching books by title or author.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies](#technologies)
- [Folder Structure](#folder-structure)
- [Contributing](#contributing)
- [License](#license)
- [Requirements](#requirements)

## Features

- **Add Author**: Allows adding authors to the library database.
- **Add Book**: Allows adding books and linking them to authors.
- **View Books**: Displays a list of books with their details, including cover images.
- **Search Books**: Search for books based on the title.
- **Sort Books**: Sort books by title or author.
- **Delete Books and Authors**: Remove books and authors from the database.

## Installation

### Prerequisites

- Python 3.x
- pip (Python package manager)

### Installation Steps

1. **Clone the repository**:

   ```bash
   git clone https://github.com/martenzoe/book_alchemy.git


2. **Create a virtual environment (recommended):**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. **Install the required dependencies:**:

   ```bash
   pip install -r requirements.txt
   
4. **Run the application:**:

   ```bash
   python app.py

5. **Navigate to http://127.0.0.1:5000 in your web browser to use the app.**:


### Usage

Once the app is running, you can interact with the application via the following routes:
- **Home** (`/home`): View, search, and sort the list of books.
- **Add Author** (`/add_author`): Add a new author to the database.
- **Add Book** (`/add_book`): Add a new book and link it to an author.
- **Delete Book**: Remove a book from the database.

Die App ist responsive und funktioniert auch auf mobilen Geräten.


## Contributing

Contributions are welcome! If you would like to contribute to BookAlchemy, follow these steps:
1. Fork the repository.
2. Create a new branch:  
   `git checkout -b feature-name`
3. Make your changes.
4. Commit your changes:  
   `git commit -am 'Add new feature'`
5. Push your branch:  
   `git push origin feature-name`
6. Open a pull request.


## License
This project is licensed under the MIT License – see the LICENSE file for details.

## Requirements
The following Python packages are required to run the application:

- Flask==2.1.1
- Flask-SQLAlchemy==2.5.1
- SQLAlchemy==1.4.32


