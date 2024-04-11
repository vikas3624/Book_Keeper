from datetime import datetime
from flask import Flask, request, jsonify, render_template,flash,redirect,url_for
from LibraryManagementServices import LibraryManagementServices

app = Flask(__name__)
app.secret_key = 'your_secret_key'


library_management_services = LibraryManagementServices()


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        book_name= request.form['bookName']
        year_of_publication= request.form['publicationYear']
        genre= request.form['genre']
        author= request.form['author']
        available_quantity= request.form['quantity']
        response = library_management_services.add_books_table(book_name, year_of_publication, genre, author, available_quantity)
        print(response)
        flash(response, 'success')
        return redirect(url_for('add_book'))
    return render_template('addbook.html')

@app.route('/register_students', methods=['GET', 'POST'])
def register_students():
    if request.method == 'POST':
        firstName= request.form['studentfName']
        lastName= request.form['studentlName']
        course= request.form['studentCourse']
        email= request.form['studentEmail']
        mobile= request.form['studentMobile']
        dob = request.form['dob']
        response = library_management_services.add_students_table(firstName, lastName, course, email, mobile,dob)
        print(response)
        flash(response, 'success')
        return redirect(url_for('show_students'))
    return render_template('student.html')

@app.route('/issue_book', methods=['GET', 'POST'])
def issue_book():
    if request.method == 'POST':
        book_id = request.form['bookID']
        student_id = request.form['studentId']
        
        issue_date = request.form['issueDate']
        return_date = request.form['returnDate']
        quantity = 1
        response = library_management_services.issue_books(book_id, student_id, issue_date,return_date,quantity)
        print(response)
        flash(response, 'success')
        return redirect(url_for('issue_book'))    
    return render_template('issuebook.html')

@app.route('/show_books')
def show_books():
     books = library_management_services.display_books()
     print(books)
     return render_template('allbooks.html', books=books)

@app.route('/show_students')
def show_students():
     students = library_management_services.display_students()
     print(students) 
     return render_template('student.html',students=students)

@app.route('/delete_books',methods=['GET', 'POST'])
def delete_books():
    if request.method == 'POST':
        student_id = request.form['student_id']
        book_id = request.form['book_id']
        response = library_management_services.delete_books(student_id,book_id)
        flash(response, 'success')
        books = library_management_services.return_books(student_id)
        print(books)
        return redirect(url_for('return_books', books=books))
    return render_template('returnbook.html')

@app.route('/delete_all_books',methods=['GET', 'POST'])
def delete_all_books():
    if request.method == 'POST':
        book_id = request.form['book_id']
        response = library_management_services.delete_all_books(book_id)
        flash(response, 'success')
        books = library_management_services.display_books()
        print(books)
        return redirect(url_for('show_books'))
    return render_template('allbooks.html')

@app.route('/return_books',methods=['GET', 'POST'])
def return_books():
    if request.method == 'POST':
        student_id = request.form['studentId']
        books = library_management_services.return_books(student_id)
        print(books)
        return render_template('returnbook.html', books=books)
    return render_template('returnbook.html')

@app.route('/search_books', methods=['GET', 'POST'])
def search_books():
    # Fetch all books from database and display
    #books = execute_query("SELECT * FROM book_list", fetch_all=True)
    #return render_template('show_books.html', books=books)
    if request.method == 'POST':
        book_name = request.form['bookName']
        # Ensure book_name is sanitized to prevent SQL injection
        books = library_management_services.search_books(book_name)
        if books:
            return render_template('searchbook.html', books=books)
        else:
            error_message = f"No books found with the name '{book_name}'."
            return render_template('searchbook.html', error=error_message)
    
    return render_template('searchbook.html')

@app.route('/search_students', methods=['GET', 'POST'])
def search_students():
    # Fetch all books from database and display
    #books = execute_query("SELECT * FROM book_list", fetch_all=True)
    #return render_template('show_books.html', books=books)
    if request.method == 'POST':
        student_id = request.form['searchInput']
        # Ensure book_name is sanitized to prevent SQL injection
        students = library_management_services.search_students(student_id)
        if students:
            return render_template('student.html', students=students)
        else:
            error_message = f"No Students found with the id '{student_id}'."
            return render_template('student.html', error=error_message)
    
    return render_template('student.html')

@app.route('/aboutus')
def aboutus():
    # Fetch all books from database and display
    #books = execute_query("SELECT * FROM book_list", fetch_all=True)
    #return render_template('show_books.html', books=books)
    
    return render_template('aboutus.html')

@app.route('/contatcus')
def contatcus():
    # Fetch all books from database and display
    #books = execute_query("SELECT * FROM book_list", fetch_all=True)
    #return render_template('show_books.html', books=books)
    
    return render_template('contactus.html')


