from datetime import datetime
import mysql.connector


class LibraryManagementDao:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="library"
        )
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute('''create table if not exists books(
	book_id integer primary key,
    book_name varchar(100),
    year_of_publication integer,
    genre varchar(100),
    author varchar(100),
    available_quantity integer
                            )''')
        self.connection.commit()

    def add_books_in_table(self, book_name, year_of_publication, genre, author, available_quantity):
        # Retrieve the last book_id
        self.cursor.execute('''
            SELECT book_id 
            FROM books 
            ORDER BY book_id DESC 
            LIMIT 1
        ''')
        book_id = self.cursor.fetchone()[0]

        # Insert the new appointment
        query = '''insert into books (book_id,book_name,year_of_publication
                    ,genre,author,available_quantity)
                    values(%s,%s,%s,%s,%s,%s);'''
        values = (book_id+1, book_name, year_of_publication, genre, author, available_quantity)
        print("Query"+query)
        self.cursor.execute(query, values)
        self.connection.commit()
        return book_id+1

    def add_students_in_table(self, firstName, lastName, course, email, mobile,dob):
        # Retrieve the last book_id
        self.cursor.execute('''
            SELECT student_id 
            FROM student 
            ORDER BY student_id DESC 
            LIMIT 1
        ''')
        student_id = self.cursor.fetchone()[0]

        # Insert the new appointment
        query = '''insert into student (student_id,student_name,date_of_birth,course,email,phone_number)
                    values(%s,%s,CAST(%s AS DATE),%s,%s,%s);'''
        values = (student_id+1, firstName+lastName,dob, course, email, mobile)
        print("Query"+query)
        self.cursor.execute(query, values)
        self.connection.commit()
        return student_id+1
    
    def issue_books_in_table(self, book_id, student_id, issue_date, return_date, quantity):
        try:
            # Check if the book exists in the books table
            self.cursor.execute('''
                SELECT COUNT(*) 
                FROM books 
                WHERE book_id = %s''', (book_id,))
            book_exists = self.cursor.fetchone()[0]
            
            # Check if the book exists in the books table
            self.cursor.execute('''
                SELECT COUNT(*) 
                FROM student 
                WHERE student_id = %s''', (student_id,))
            student_exists = self.cursor.fetchone()[0]

            if book_exists == 0:
                # Book does not exist in the books table
                error_message = "Book ID not found in the library"
                return error_message
            
            if student_exists == 0:
                # Student does not exist in the database
                error_message = "Student ID not found in the database.Please Register the Student"
                return error_message

            # Check if the same book_id and student_id exist in BookIssue table
            self.cursor.execute('''
                SELECT book_id, student_id, quantity_taken
                FROM BookIssue 
                WHERE book_id = %s AND student_id = %s
            ''', (book_id, student_id))
            existing_record = self.cursor.fetchone()

            if existing_record:
                # Update the quantity_taken if the record exists
                error_message = "Book ID: "+book_id+" have been already issued to the Student ID: "+student_id
                return error_message
            else:
                # Retrieve the available quantity of the book
                self.cursor.execute('''
                    SELECT available_quantity 
                    FROM books 
                    WHERE book_id = %s''', (book_id,))
                available_quantity = self.cursor.fetchone()[0]

                # Check if there are enough books available
                if int(quantity) > int(available_quantity):
                    error_message = "Not enough books available"
                    return error_message

                # Insert the data
                query = '''
                    INSERT INTO BookIssue (book_id, student_id, date_of_issue, date_of_return, quantity_taken)
                    VALUES (%s, %s, CAST(%s AS DATE), CAST(%s AS DATE), %s);
                '''
                values = (book_id, student_id, issue_date, return_date, quantity)
                self.cursor.execute(query, values)

                # Update available_quantity in the books table
                new_available_quantity = available_quantity - int(quantity)
                update_query = '''
                    UPDATE books
                    SET available_quantity = %s
                    WHERE book_id = %s
                '''
                print(new_available_quantity)
                self.cursor.execute(update_query, (new_available_quantity, book_id))
            
            # Commit the transaction
            self.connection.commit()

            # Success message
            success_message = "Book issued successfully"
            return success_message

        except Exception as e:
            # Handle exceptions
            self.connection.rollback()
            error_message = f"Error: {e}"
            return error_message


    
    def show_books_from_table(self):
        # Retrieve the last book_id
        self.cursor.execute('''SELECT * FROM books''')
        return self.cursor.fetchall()
    
    def show_students_from_table(self):
        # Retrieve the last book_id
        self.cursor.execute('''SELECT * FROM student''')
        return self.cursor.fetchall()
    
    def delete_all_books_from_table(self, book_id):
        """
        Delete all book entries from the 'books' table with the specified book_id.

        Args:
            book_id (int): The ID of the book to be deleted from the table.

        Returns:
            str: A string indicating the result of the deletion operation.
        """
        try:
            sql = "DELETE FROM books WHERE book_id = %s"
            self.cursor.execute(sql, (book_id,))
            # Commit the transaction
            self.connection.commit()
            return "Book entry deleted successfully."
        except mysql.connector.Error as e:
            # Handle foreign key constraint violation
            if e.errno == mysql.connector.errorcode.ER_ROW_IS_REFERENCED_2:
                self.connection.rollback()
                return "Error: Cannot delete book due to book borrowed by student."
            else:
                # Handle other exceptions
                self.connection.rollback()
                return f"Error occurred: {e}"

    
    def return_books_from_table(self,student_id):
        
        query = '''
            SELECT 
        BookIssue.book_id AS `Book ID`,
        books.book_name AS `Book Name`,
        books.author AS `Author`,
        books.genre AS `Genre`,
        books.year_of_publication AS `Publication Year`,
        BookIssue.date_of_issue AS `Date of issue`,
        BookIssue.date_of_return AS `Date of return`,
        BookIssue.student_id as Student_ID
    FROM 
        BookIssue
    INNER JOIN 
        books ON BookIssue.book_id = books.book_id
    WHERE
        BookIssue.student_id = %s
        '''

        # Execute the query with the student_id parameter
        self.cursor.execute(query, (student_id,))

        # Fetch the results if needed
        results = self.cursor.fetchall()

        return results
    
    def delete_books_from_table(self, student_id, book_id):
        try:
            # Fetch the current available quantity of the book
            self.cursor.execute('''
                SELECT available_quantity
                FROM books
                WHERE book_id = %s
            ''', (book_id,))
            available_quantity = self.cursor.fetchone()[0]

            # Construct the SQL query with DELETE statement
            query_delete = '''
                DELETE FROM BookIssue
                WHERE book_id = %s AND student_id = %s
            '''

            # Execute the DELETE query with the book_id and student_id parameters
            self.cursor.execute(query_delete, (book_id, student_id))
            
            # Increment the available quantity in the books table
            new_available_quantity = available_quantity + 1
            query_increment = '''
                UPDATE books
                SET available_quantity = %s
                WHERE book_id = %s
            '''
            self.cursor.execute(query_increment, (new_available_quantity, book_id))

            # Commit the transaction
            self.connection.commit()

            # Return a success message
            return "Book returned successfully"
        except Exception as e:
            # Handle exceptions
            self.connection.rollback()
            return f"Error occurred: {e}"


    
    def search_books_from_table(self,book_name):
        # Retrieve the last book_id
        self.cursor.execute("SELECT * FROM books WHERE book_name LIKE %s", ('%' + book_name + '%',))
        return self.cursor.fetchall()
    
    def search_students_from_table(self,student_id):
        # Retrieve the last book_id
        self.cursor.execute("SELECT * FROM student WHERE student_id LIKE %s", ('%' + student_id + '%',))
        return self.cursor.fetchall()


    def cancel_appointment(self, appointment_id):
        query = '''DELETE FROM appointments WHERE id = %s'''
        values = (appointment_id,)
        self.cursor.execute(query, values)
        self.connection.commit()

    def display_schedule(self):
        self.cursor.execute('''SELECT * FROM appointments''')

        return self.cursor.fetchall()
