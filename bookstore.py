#====Importing Libraries====
import sqlite3


#====Functions & Classes====
class Ebooks:
    """This class provides functionality to update and delete records
    from the database ebookstore.db
    """

    # Constructor Method
    def  __init__(self, id_key, title, author, qty):
        self.id = id_key
        self.title = title
        self.author = author
        self.qty = qty

    def update_title(self, new_title):
        """Updates the title of a record in the database

        Args:
            new_title (string): new title for a selected record
        """

        self.title = new_title
        with sqlite3.connect("ebookstore.db") as ebookstore:
            monkey = ebookstore.cursor()

            monkey.execute("""
            UPDATE book
            SET title = ?
            WHERE id = ?""", (self.title, self.id))
            ebookstore.commit()

    def update_author(self, new_author):
        """Updates the author of a record in the database

        Args:
            new_author (string): new author for a selected record
        """

        self.author = new_author
        with sqlite3.connect("ebookstore.db") as ebookstore:
            monkey = ebookstore.cursor()

            monkey.execute("""
            UPDATE book
            SET author = ?
            WHERE id = ?""", (self.author, self.id))
            ebookstore.commit()

    def update_qty(self, new_qty):
        """Updates the quantity of a record in the database

        Args:
            new_qty (string): new quantity for a selected record
        """

        self.qty = new_qty
        with sqlite3.connect("ebookstore.db") as ebookstore:
            monkey = ebookstore.cursor()

            monkey.execute("""
            UPDATE book
            SET qty = ?
            WHERE id = ?""", (self.qty, self.id))
            ebookstore.commit()

    def delete_book(self):
        """Deletes a selected record in the database
        """

        with sqlite3.connect("ebookstore.db") as ebookstore:
            monkey = ebookstore.cursor()

            monkey.execute("""
                DELETE FROM book
                WHERE id = ?
            """, (self.id,))
            ebookstore.commit()


def ebookstore_dict():
    """Creates a dictionary holding the records of a database
    as objects and the id as dictionary keys.

    Returns:
        dict: Dictionary containing records from the database
    """
    
    books = {}
    try:
        ebookstore = sqlite3.connect("ebookstore.db")
        monkey = ebookstore.cursor()

        monkey.execute("""
            SELECT *
            FROM book
        """)
    
        for book in monkey:
            books[book[0]] = Ebooks(book[0], book[1], book[2], book[3])
    
    except Exception as error:
        print(error)
        ebookstore.rollback()
    
    finally:
        ebookstore.close()

    return books


def menu_display():
    """Main Menu for the application"""

    print("""\nE-MENU\n
1. Enter book
2. Update book
3. Delete book
4. Search books
0. Exit""")


def display_books(order):
    """Displays the records of the database ebookstore.db in a specific
    order.

    Args:
        order (string): determines the order of the records
    """

    with sqlite3.connect("ebookstore.db") as ebookstore:
        monkey = ebookstore.cursor()

        if order == "ii":
            monkey.execute("""
            SELECT * FROM book ORDER BY title
        """)

        elif order == "i":
            monkey.execute("""
            SELECT * FROM book ORDER BY id
        """)

        elif order == "iii":
            monkey.execute("""
            SELECT * FROM book ORDER BY author
        """)

        elif order == "iv":
            monkey.execute("""
            SELECT * FROM book ORDER BY qty
        """)   
        else:
            monkey.execute("""
            SELECT * FROM book
        """) 

        print("..........\nAvailable Books")
        for book in monkey:
            print()
            print(f"{book[1]}")
            print(f"ID\t\t: {book[0]}")
            print(f"Author\t\t: {book[2]}")
            print(f"Quantity\t: {book[3]}")


def display_book(id_key):
    """Display one records based on the id_key.

    Args:
        id_key (int): Id of a record in the database
    """

    print(f"{ebookstore_dict()[id_key].title}")
    print(f"ID\t\t: {ebookstore_dict()[id_key].id}")
    print(f"Author\t\t: {ebookstore_dict()[id_key].author}")
    print(f"Quantity\t: {ebookstore_dict()[id_key].qty}")


def add_book(title, author, qty):
    """Adds a new record in the database ebookstore.db

    Args:
        title (string): Title of the new record
        author (string): Author of the new record
        qty (int): Quantity of the new record
    """

    try:
        ebookstore = sqlite3.connect("ebookstore.db")
        monkey = ebookstore.cursor()

        monkey.execute("""
            INSERT INTO book (title, author, qty)
                       VALUES (?, ?, ?)""", (title, author, qty))
        
        ebookstore.commit()

    except Exception as error:
        ebookstore.rollback()
        print(error)

    finally:
        ebookstore.close()


def update_book(id_key):
    """Updates a selected record in the database by using the methods from
    the Ebook class

    Args:
        id_key (int): Id of the selected record
    """

    # Checks that id is in the database
    while id_key in ebookstore_dict():
        print("Selected:")
        display_book(id_key)

        print("..........\nUPDATE")
        print("i. Title\tii. Author\tiii. Quantity\tiv. Exit")
        update = input("\nSelection >> ").strip().strip(".").strip().lower()

        # UPDATE TITLE
        if update == "i":
            print("\nUpdate Title")
            print(f"\nCurrent Title\t: {ebookstore_dict()[id_key].title}")
            new_title = input("New Title\t: ")

            ebookstore_dict()[id_key].update_title(new_title)
            print("\nTitle Updated!!\n")

        # UPDATE AUTHOR
        elif update == "ii":
            print("\nUpdate Author")
            print(f"\nCurrent Author\t: {ebookstore_dict()[id_key].author}")
            new_author = input("New Author\t: ")

            ebookstore_dict()[id_key].update_author(new_author)
            print("\nAuthor Updated!!\n")

        # UPDATE QUANTITY
        elif update == "iii":
            print("\nUpdate Quantity")
            print(f"\nCurrent Quantity\t: {ebookstore_dict()[id_key].qty}")

            try:
                new_qty = int(input("New Quantity\t\t: "))

                ebookstore_dict()[id_key].update_qty(new_qty)
                print("\nQuantity Updated!!\n")

            except ValueError:
                print("\nOpps - Invalide input")
                print("Please enter only whole numbers for quantity\n")

        # EXIT FUNCTION
        elif update == "iv":
            break

        else:
            print("\nOpps - Invalid input, Please try again.\n")

    else:
        print("\nID is not recognised!!")


def delete_func(id_key):
    """Deletes a selected record from the database.

    Args:
        id_key (int): Id of the selected record.
    """

    # Checks if id is in the database
    while id_key in ebookstore_dict():
        print("Selected:")
        display_book(id_key)

        # CONFIRM DELETION
        print("\nConfirm to delete this book")
        delete = input("YES or NO\n.....\n").upper().strip()

        if delete == "YES":
            ebookstore_dict()[id_key].delete_book()
            print("\nBook Deleted!!")
            break

        elif delete == "NO":
            break
        else:
            print("\nOpps - Invalid input, Please Enter YES or NO\n")


def search_by(value, search):
    """Prints out the records based on certain condition
    as requested by the user.

    Args:
        value (any): Search condition
        search (int): Determines which conditional statement to execute
    """

    with sqlite3.connect("ebookstore.db") as ebookstore:
        monkey = ebookstore.cursor()

        if search == 1:
            monkey.execute("""
                SELECT * FROM book WHERE id LIKE ?
            """, (value,))

        elif search == 2:
                monkey.execute("""
                SELECT * FROM book WHERE title LIKE ?
            """, (value,))

        elif search == 3:
                monkey.execute("""
                SELECT * FROM book WHERE author LIKE ?
            """, (value,))
        
        for book in monkey:
            print()
            print(f"{book[1]}")
            print(f"ID\t\t: {book[0]}")
            print(f"Author\t\t: {book[2]}")
            print(f"Quantity\t: {book[3]}")


#====Initializing Database====
try:
    ebookstore = sqlite3.connect("ebookstore.db")
    monkey = ebookstore.cursor()

    # Creating Table
    monkey.execute("""
        CREATE TABLE IF NOT EXISTS book(
                   id INTEGER PRIMARY KEY,
                   title TEXT,
                   author varchar(200),
                   qty int
        )
    """)
    ebookstore.commit()

    # Only enter values if records for the table are empty
    if len(monkey.execute("""SELECT * FROM book""").fetchall()) < 1:
        monkey.execute(

"""INSERT INTO book(id, title, author, qty)
            VALUES
                       
(3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
(3002, "Harry Potter and the Philosopher's Stone", 'J.K. Rowling', 40),
(3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25),
(3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
(3005, 'Alice in Wonderland', 'Lewis Carroll', 12),
(3006, 'A Song of Ice and Fire', 'George R. R. Martin', 50)

""")
        ebookstore.commit()

except Exception as error:
    ebookstore.rollback()
    print(error)

finally:
    ebookstore.close()

#====Application=====
print("Welcome To E-books")

while True:
    # DISPLAY MAIN MENU
    menu_display()
    print("..........\nWhat would you like to do")
    choice = input("Selection >> ")

    # ADD BOOK TO DATABASE
    if choice == "1":
        print("\nTo add a new book please enter the following details:")
        title = input("Title\t\t: ")
        author = input("Author\t\t: ")

        try:
            qty = int(input("Quantity\t: "))
            add_book(title, author, qty)
            print("\nBook added!")

        except ValueError:
            print("\nOpps - Invalid input")
            print("Please enter only whole numbers for quantity")

    # UPDATE RECORDS IN DATABASE
    elif choice == "2":
        order = "id"

        while True:
            display_books(order)
            print("..........")
            print("""
1. Select By ID
2. Sort By
3. Exit
""")        
            choice = input("Selection >> ")

            # SELECT BY ID
            if choice == "1":
                id_key = int(input("Please Enter ID: "))
                print("..........")
                print()

                # Initiate update function
                update_book(id_key)

            # SORT THE RECORDS
            elif choice == "2":
                print("..........\nSort by")
                print("""
i. ID\t  ii. Title\tiii. Author\tiv. Quantity\tv. Cancel
""")
                order = input("Selection >> ").strip().strip(".").lower()

            # EXIT UPDATE FUNCTION
            elif choice == "3":
                break

            else:
                print("Opps - Invalid input")

    # DELETE RECORDS FROM DATABASE
    elif choice == "3":
        order = "id"

        while True:
            display_books(order)
            print("..........")
            print("""
1. Select By ID
2. Sort By
3. Exit
""")
            choice = input("Selection >> ")

            # SELECT BY ID
            if choice == "1":
                id_key = int(input("Please Enter ID: "))
                print("..........")
                print()

                # Initiate delete function
                delete_func(id_key)

            # SORT THE RECORDS
            elif choice == "2":
                print("..........\nSort by")
                print("""
i. ID\t  ii. Title\tiii. Author\tiv. Quantity\tv. Cancel
""")
                order = input("Selection >> ").strip().strip(".").lower()

            # EXIT DELETE FUNCTION
            elif choice == "3":
                break

            else:
                print("Opps - Invalid input")

    # SEARCH DATABASE RECORDS
    elif choice == "4":

        while True:
            print("..........\nSEARCH MENU")
            print("""
Search By:
1. ID
2. Title
3. Author
4. Exit
""")
            try:
                search = int(input("Selection >> "))

                # SEARCH BY ID
                if search == 1:
                    id_key = int(input("Please enter ID: "))
                    search_by(id_key, search)

                # SEARCH BY TITLE
                elif search == 2:
                    title = (input("Please enter title: "))
                    title += "%"
                    search_by(title, search)

                # SEARCH BY AUTHOR
                elif search == 3:
                    author = (input("Please enter author: "))
                    author += "%"
                    search_by(author, search)

                # EXIT SEARCH FUNCTION
                elif search == 4:
                    break
            
                else:
                    print("\nOpps - Invalid input, Please try again.")

            except ValueError:
                print("\nOpps - Invalid input")
                print("Please Enter only numbers (1-4).")

    # EXIT APPLICATION
    elif choice == "0":
        print("Goodbye!!")
        exit()

    else:
        print("\nOpps - Invalid input, Please try again.")
        