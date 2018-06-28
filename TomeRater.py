class User(object):
    def __init__(self, name, email):
        self.name  = name
        self.email = email
        self.books = {}
    # Method that returns the email associated with the user
    def get_email(self):
        return self.email
    # Method to change user's email
    def change_email(self, address):
        self.email = address
        print("The email address for {} has been changed to {}".format(self.name, self.email))
    # Print user object
    def __repr__(self):
        return "------\nUser: {}\nEmail: {}\nBooks Read: {}\n------".format(self.name, self.email, len(self.books))
    # Deep equality (compare if objects are equal not references to object) when name and email are equal
    def __eq__(self, other_user):
        return (self.name == other_user.name) and (self.email == other_user.email)
    # Method to add read books
    def read_book(self, book, rating=None,):
        self.books.update({book: rating})
    # Method to calculate the books average rating
    def get_average_rating(self):
        rating_sum = 0
        for value in self.books.values():
            if value:
                rating_sum += value
        return rating_sum / len(self.books)

class Book(object):
    # Create a class variable to keep track of the isbn
    # This will be the same across all Book instances
    uniq_isbn = []
    def __init__(self, title, isbn):
        self.title   = title
        self.isbn    = isbn
        self.ratings = []
    # Method to return book title
    def get_title(self):
        return self.title
    # Method to return book ISBN
    def get_isbn(self):
        return self.isbn
    # Method to set new isbn
    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print("The ISBN for the book {} has been changed to {}".format(self.title, self.isbn))
    # Add books ratings
    def add_rating(self, rating):
        # Check if the rating is valid
        #if rating > 0 and rating <= 4:
        if rating and rating > 0 and rating <= 4:
            self.ratings.append(rating)
        else:
            print("Invalid Rating")
    # Deep equality (compare if objects are equal not references to object) when title and isbn are equal
    def __eq__(self, other_book):
        return (self.title == other_book.title) and (self.isbn == other_book.isbn)
    # Method to print the book title
    def __repr__(self):
        return self.title
    # Method to calculate the ratings average
    def get_average_rating(self):
        rating_sum = 0
        for item in self.ratings:
            rating_sum += item
        return rating_sum / len(self.ratings)
    # Hash book object so it can be used as key on the user class
    def __hash__(self):
        return hash((self.title, self.isbn))

# Subclass of Book for fiction books
class Fiction(Book):
    def __init__(self, title, isbn, author):
        Book.__init__(self, title, isbn)
        self.author = author
    # Method to return the author
    def get_author(self):
        return self.author
    # Return string
    def __repr__(self):
        return "{} by {}".format(self.title, self.author)

# Subclass of Book for non fiction books
class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        Book.__init__(self, title, isbn)
        self.subject = subject
        self.level   = level
    # Method  to return the subject
    def get_subject(self):
        return self.subject
    # Method to return the level
    def get_level(self):
        return self.level
    # Return string
    def __repr__(self):
        return "{}, a {} manual on {}".format(self.title, self.level, self.subject)

# TomeRater class
class TomeRater(object):
    def __init__(self):
        # Dictionary to map user email to an User instance
        self.users = {}
        # Dictionary to map a Book instance to the number of user that have read it
        self.books = {}
    # Method to create Book instances
    def create_book(self, title, isbn):
        # Check that isbn is uniq
        if self.uniq_isbn(isbn):
            a_book = Book(title, isbn)
            return a_book
    # Method to create Fiction instances
    def create_novel(self, title, author, isbn):
        if self.uniq_isbn(isbn):
            a_novel = Fiction(title, isbn, author)
            return a_novel
    # Method to create Non_Fiction instances
    def create_non_fiction(self, title, subject, level, isbn):
        if self.uniq_isbn(isbn):
            a_non_fiction = Non_Fiction(title, subject, level, isbn)
            return a_non_fiction
    # Method to add book to user
    def add_book_to_user(self, book, email, rating=None):
        a_user = self.users.get(email, None)
        if a_user:
            # Add the book to read books
            a_user.read_book(book, rating)
            # Check if the book is not already in TomeRater
            if book not in self.books:
                self.books[book] = 1
                #self.books.update({book: 1})
            else:
                self.books[book] += 1
            # Add rating to the book if any
            book.add_rating(rating)
        else:
            print("No user with email {}".format(email))
    # Method to add a user (books should be passes as a list)
    def add_user(self, name, email, user_books=None):
        # Check email validity (@ exists and there is at least on . after it)
        if "@" in email and "." in email[email.find("@")+1:]:
            # Create a User instance
            new_user = User(name, email)
            # Add the user to the users dictionary
            # Check that the key (email) does not exists already
            if email not in self.users.keys():
                self.users[email] = new_user
            else:
                print("This email aready exists. Use another email address")
            # If book exists add to to books dictionary
            if user_books:
                for item in user_books:
                    self.add_book_to_user(item, email)
        else:
            print("Invalid email address")
    # Method to print all the books in the books dictionary
    def print_catalog(self):
        for item in self.books.keys():
            print(item)
    # Method to print all the users in the users dictionary
    def print_users(self):
        for item in self.users.values():
            print(item)
    # Method that returns the most read book
    def get_most_read_book(self):
        # Holder for the book with most reads
        reads_holder = 0
        book_holder = None
        for item in self.books:
            reads = self.books[item]
            if reads >= reads_holder:
                # Update the holders
                reads_holder = reads
                book_holder = item
        return book_holder
    # Method that returns the book with the biggest average rating
    def highest_rated_book(self):
        # Create holders for the highest rating and the book mapped to it
        rating_holder = 0
        book_holder = None
        for item in self.books:
            # Get the averagae rating of the book insntace
            # (keys in self.books are Book instances)
            avg = item.get_average_rating()
            if avg >= rating_holder:
                # Update the holders with the highest value
                rating_holder = avg
                book_holder = item
        return book_holder
    # Method that return the most positive (highest average rating) value
    def most_positive_user(self):
        # Create holders for the highest average ratign and the user mapped to it
        rating_holder = 0
        user_holder = None
        for item in self.users:
            # Get the average rating for the user instance
            # calling it's get_average_rating method
            avg = self.users[item].get_average_rating()
            if avg >= rating_holder:
                # Update the holders
                rating_holder = avg
                user_holder = self.users[item]
        return user_holder
    # For debugging
    def __repr__(self):
        return str(self.books) + "\n" + str(self.users)
    # Function to check that ISBN is uniq
    def uniq_isbn(self, isbn):
        if isbn not in Book.uniq_isbn:
            Book.uniq_isbn.append(isbn)
            return True
        else:
            print("ISBN already exists for another book. Same ISBN for different books is not allowed")
            return False
