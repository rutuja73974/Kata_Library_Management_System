from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'secret_key'

# Book Class
class Book:
    def __init__(self, isbn, title, author, year):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.is_borrowed = False

# Library Class
class Library:
    def __init__(self):
        self.books = []

    def add_book(self, isbn, title, author, year):
        new_book = Book(isbn, title, author, year)
        self.books.append(new_book)
        return f"Book '{title}' added to the library."

    def borrow_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                if not book.is_borrowed:
                    book.is_borrowed = True
                    return f"You have successfully borrowed '{book.title}'."
                else:
                    return f"Sorry, the book '{book.title}' is currently borrowed."
        return "Book not found!"

    def return_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                if book.is_borrowed:
                    book.is_borrowed = False
                    return f"You have successfully returned '{book.title}'."
                else:
                    return f"The book '{book.title}' was not borrowed."
        return "Book not found!"

    def view_available_books(self):
        available_books = [book for book in self.books if not book.is_borrowed]
        if available_books:
            return available_books
        else:
            return []

# Initialize Library
library = Library()

@app.route('/')
def index():
    return render_template('index.html')

# Route for adding a book
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        isbn = request.form['isbn']
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        if isbn and title and author and year:
            library.add_book(isbn, title, author, year)
            flash(f"Book '{title}' added successfully!")
            return redirect(url_for('index'))
        else:
            flash('All fields are required!')
    return render_template('add_book.html')

# Route for borrowing a book
@app.route('/borrow_book', methods=['GET', 'POST'])
def borrow_book():
    if request.method == 'POST':
        isbn = request.form['isbn']
        result = library.borrow_book(isbn)
        flash(result)
        return redirect(url_for('index'))
    return render_template('borrow_book.html')

# Route for returning a book
@app.route('/return_book', methods=['GET', 'POST'])
def return_book():
    if request.method == 'POST':
        isbn = request.form['isbn']
        result = library.return_book(isbn)
        flash(result)
        return redirect(url_for('index'))
    return render_template('return_book.html')

# Route for viewing available books
@app.route('/available_books')
def available_books():
    books = library.view_available_books()
    return render_template('available_books.html', books=books)

if __name__ == '__main__':
    app.run(debug=True)
