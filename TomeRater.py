# Tome Rater Project
# by JP Brichta
# 4 July 2018
# Capstone project for Codecademy Pro course on Introduction to Python
#
# In my version of the project, I have chosen to implement the most sophisticated analysis methods and
# also some of the more sophisticated error testing  

class User(object):
    """User base class.

    Usage:
    foo = User(name, email)
    """   
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print ("This user's email has been updated.")

    def __repr__(self):
        return "User " + self.name + ", email: " + self.email + ", books read: " + str(len(self.books))

    def __eq__(self, other_user):
        if self.email == other_user.email:
            return True
        else:
            return False

    def read_book(self, book, rating=None):
        self.books[book] = rating

    def get_average_rating(self):
        """Return user's average rating, rounded to one decimal place."""
        total_rating = 0
        number_rated_books = 0
        for rating in self.books.values():
            try:
                total_rating += rating
                number_rated_books += 1
            except TypeError: #book has rating of None
                pass
        return round(total_rating / number_rated_books, 1)               

class Book(object):
    """Book base class.

    Usage:
    foo = Book(title, isbn)
    title should be str, isbn should be int
    """ 
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print ("This book's ISBN has been updated.")

    def add_rating(self, rating):
        if not isinstance(rating, type(None)):
            if 0 <= rating <= 4:
                self.ratings.append(rating)
            else:
                print ("Invalid rating. Must be between 0 and 4.")

    def get_average_rating(self):
        total_rating = 0
        for rating in self.ratings:
            total_rating += rating
        return round(total_rating / len(self.ratings), 1)

    def __eq__(self, other_book):
        if self.title == other_book.title and self.isbn == other_book.isbn:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.title, self.isbn))

    def __repr__(self):
        return self.title


class Fiction(Book):
    """Fiction subclass

    Usage:
    foo = Fiction(title, author, isbn)
    title, author should be str, isbn should be int
    """
    def __init__(self, title, author, isbn):
        super().__init__(title, author)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return self.title + " by " + self.author


class Non_Fiction(Book):
    """Non-Fiction subclass

    Usage:
    foo = Non_Fiction(title, subject, level, isbn)
    title, subject, level should be str, isbn should be int
    """
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return self.title + ", a " + self.level + " manual on " + self.subject


class TomeRater(object):
    """TomeRater base class

    Usage:
    foo = TomeRater()
    """
    def __init__(self):
        self.users = {}
        self.books = {}

    def create_book(self, title, isbn):
        return Book(title, isbn)
        
    def create_novel(self, title, author, isbn):
        return Fiction(title, author, isbn)

    def create_non_fiction(self, title, subject, level, isbn):
        return Non_Fiction(title, subject, level, isbn)

    def add_book_to_user(self, book, email, rating=None):
        if email in self.users:
            self.users[email].read_book(book, rating)
            book.add_rating(rating)
            if book in self.books:
                self.books[book] += 1
            else:
                self.books[book] = 1
        else:
            print ("No user with email " + email + "!")

    def add_user(self, name, email, user_books=None):
        if email in self.users:
            print("WARNING: A user with email {email} already exists.".format(email=email))
        elif "@" not in email:
            print("WARNING: The email {email} does not contain the @ symbol.".format(email=email))
        else:
            self.users[email] = User(name, email)
            if not isinstance(user_books, type(None)):
                for book in user_books:
                    self.add_book_to_user(book, email)

    def print_catalog(self):
        for key in self.books.keys():
            print(key)

    def print_users(self):
        for value in self.users.values():
            print(value)

    def most_read_book(self):
        max_read_book = None
        max_read = float("-inf")
        for key, value in self.books.items():
            if value > max_read:
                max_read = value
                max_read_book = key
        return max_read_book

    def highest_rated_book(self):
        highest_book = None
        highest_rating = float("-inf")
        for book in self.books.keys():
            if book.get_average_rating() > highest_rating:
                highest_rating = book.get_average_rating()
                highest_book = book
        return highest_book

    def most_positive_user(self):
        highest_user = None
        highest_rating = float("-inf")
        for user in self.users.values():
            if user.get_average_rating() > highest_rating:
                highest_user = user
                highest_rating = user.get_average_rating()
        return highest_user

    def get_n_most_read_books(self, n):
        if n > len(self.books):
            print("WARNING: There aren't that many books in Tome Rater. I will give you the top {num} instead.".format(num=len(self.books)))
            n = len(self.books)
        previous_max = float("inf")
        output = []
        for i in range(n):
            max_times_read = float("-inf")
            for book, times_read in self.books.items():
                if times_read > max_times_read and times_read <= previous_max and book not in output: 
                    top_book = book
                    max_times_read = times_read
                    
            output.append(top_book)
            previous_max = max_times_read
        return output

    def get_n_most_prolific_readers(self, n):
        if n > len(self.users):
            print("WARNING: There aren't that many users in Tome Rater. I will give you the top {num} instead.".format(num=len(self.users)))
            n = len(self.users)
        previous_max = float("inf")
        output = []
        for i in range(n):
            max_books_read = float("-inf")
            for user in self.users.values():
                if max_books_read < len(user.books) <= previous_max and user not in output: 
                    top_user = user
                    max_books_read = len(user.books)
                    
            output.append(top_user)
            previous_max = max_books_read
        return output

                
