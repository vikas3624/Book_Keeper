from datetime import datetime


from LibraryManagementDao import LibraryManagementDao


class LibraryManagementServices:

    def __init__(self):
        self.library_management_dao = LibraryManagementDao()
        
    def add_students_table(self, firstName, lastName, course, email, mobile,dob):

        student_id = self.library_management_dao.add_students_in_table(firstName, lastName, course, email, mobile,dob)
        return f"New Student Added successfully! Student ID: {student_id}"
    
    def add_books_table(self, book_name, year_of_publication, genre, author, available_quantity):

        book_id = self.library_management_dao.add_books_in_table(book_name, year_of_publication, genre, author, available_quantity)
        return f"New Book Added successfully! Book ID: {book_id}"
    
    def issue_books(self,book_id, student_id, issue_date,return_date,quantity):
        print("entered")
        response = self.library_management_dao.issue_books_in_table(book_id, student_id, issue_date,return_date,quantity)
        return response
    
    def display_books(self):
        books = self.library_management_dao.show_books_from_table()
        return books
    
    def display_students(self):
        students = self.library_management_dao.show_students_from_table()
        return students
    
    def delete_books(self,student_id,book_id):
        response = self.library_management_dao.delete_books_from_table(student_id,book_id)
        return response
    
    def delete_all_books(self,book_id):
        response = self.library_management_dao.delete_all_books_from_table(book_id)
        return response
    
    def return_books(self,student_id):
        books = self.library_management_dao.return_books_from_table(student_id)
        return books
    
    def search_books(self,book_name):
        books = self.library_management_dao.search_books_from_table(book_name)
        return books
    
    def search_students(self,student_id):
        students = self.library_management_dao.search_students_from_table(student_id)
        return students
    

