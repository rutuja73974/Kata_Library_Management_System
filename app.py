from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'secret_key'


# Book Class
class Book:
    def __init__(self, isbn, title, author, year, quantity):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.quantity = quantity  # New attribute to track the number of copies
    
    def __str__(self):
        return f"ISBN: {self.isbn}, Title: {self.title}, Author: {self.author}, Year: {self.year}, Available Copies: {self.quantity}"

# Library Class
class Library:
    def __init__(self):
        self.books = []

    def add_book(self, isbn, title, author, year, quantity):
        for book in self.books:
            if book.isbn == isbn:
                book.quantity += quantity  # If the book already exists, increase its quantity
                return f"Updated quantity for '{title}'. Now we have {book.quantity} copies."
        new_book = Book(isbn, title, author, year, quantity)
        self.books.append(new_book)
        return f"Book '{title}' added with {quantity} copies."

    def borrow_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                if book.quantity > 0:
                    book.quantity -= 1
                    return f"You have successfully borrowed '{book.title}'. {book.quantity} copies left."
                else:
                    return f"Sorry, all copies of '{book.title}' are currently borrowed."
        return "Book not found!"

    def return_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                book.quantity += 1
                return f"You have successfully returned '{book.title}'. Now we have {book.quantity} copies."
        return "Book not found!"

    def view_available_books(self):
        available_books = [book for book in self.books if book.quantity > 0]
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
        quantity = int(request.form['quantity'])  # Get the number of copies

        # Check if the ISBN already exists
        for book in library.books:
            if book.isbn == isbn:
                flash(f"Book with ISBN {isbn} already exists as '{book.title}'.")
                
                # Asking user if they want to add more copies
                flash(f"Do you want to add more copies to this book?")
                return render_template('confirm_add_copies.html', book=book, quantity=quantity)  # Render a confirmation page

        # If ISBN does not exist, add the book as usual
        if isbn and title and author and year and quantity:
            library.add_book(isbn, title, author, year, quantity)
            flash(f"Book '{title}' added successfully with {quantity} copies!")
            return redirect(url_for('index'))
        else:
            flash('All fields are required!')
    return render_template('add_book.html')

@app.route('/confirm_add_copies', methods=['POST'])
def confirm_add_copies():
    isbn = request.form['isbn']
    additional_quantity = int(request.form['additional_quantity'])  # Get the additional copies

    # Find the book and update the quantity
    for book in library.books:
        if book.isbn == isbn:
            book.quantity += additional_quantity
            flash(f"Added {additional_quantity} more copies to '{book.title}'. Now we have {book.quantity} copies.")
            return redirect(url_for('index'))

    flash("Book not found!")  # This shouldn't happen under normal flow
    return redirect(url_for('index'))


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
