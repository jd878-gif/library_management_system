import mysql.connector
from mysql.connector import Error

from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
load_dotenv()

def create_connection():
    try:
        connection = mysql.connector.connect(
        host = os.getenv('DB_HOST'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD'),
        database = os.getenv('DB_NAME')
        )
        return connection
    except Error as e:
        print(f"The error '{e}' occurred")

# connection = create_connection("library_application.db")

def execute_query(query):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(query):
    connection = create_connection()
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

create_book_table = """
CREATE TABLE IF NOT EXISTS book(
    isbn_no int Primary Key,
    title TEXT,
    author TEXT,
    publisher TEXT,
    years_of_publication int,
    is_borrowed INT default 0,
    borrowed_by INT
);"""


create_member_table = """
CREATE TABLE IF NOT EXISTS member(
    member_id int Primary Key,
    name TEXT,
    age INT,
    email TEXT,
    years_of_experience int
);"""

def book_to_dict(book):
    return{
    "isbn_no": book[0], 
    "title" : book[1], 
    "author" : book[2], 
    "publisher" : book[3], 
    "years_of_publication" : book[4], 
    "is_borrowed" : book[5], 
    "borrowed_by" : book[6]
    }

def member_to_dict(member):
    return{
    "member_id" : member[0], 
    "name" : member[1], 
    "age" : member[2], 
    "email" : member[3], 
    "years_of_experience" : member[4]
    }

app = Flask(__name__)
@app.before_request
def startup():
    execute_query(create_book_table)
    execute_query(create_member_table)

@app.get('/books')
def get_books():
    books_get= f"SELECT  * FROM book" 
    result = execute_read_query(books_get)
    all_books = [book_to_dict(book) for book in result]
    return jsonify(all_books)

@app.get('/members')
def get_members():
    members_get = f"select * from member"
    result1 = execute_read_query(members_get)
    all_members = [member_to_dict(member) for member in result1]
    return jsonify(all_members)

@app.post('/books')
def create_book():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    isbn_no = data.get('isbn_no')
    title = data.get('title')
    author = data.get('author')
    publisher = data.get('publisher')
    years_of_publication = data.get('years_of_publication')

    if not isbn_no or not title or not author or not publisher or not years_of_publication:
        return jsonify({"error": "All fields are required"}), 400
    
    if isbn_no < 0:
        return jsonify({"error": "isbn_no must be positive"}), 400
    
    if years_of_publication < 0:
        return jsonify({"error": "years of publication must be positive"}), 400
    
    check_duplicate = f"SELECT  * FROM book WHERE isbn_no={isbn_no}" 
    result = execute_read_query(check_duplicate)
    if result:
        return jsonify({"error":"book already exist"}), 400
    else:
        insert_book = f"""insert into book (isbn_no, title, author,publisher,years_of_publication) values({isbn_no}, '{title}', '{author}', '{publisher}',{years_of_publication})"""
        execute_query(insert_book)
        return jsonify("Book inserted successfully!"),201

@app.delete('/books/<int:isbn_no>')
def delete_book(isbn_no):
    exist_book = f"SELECT * FROM book where isbn_no={isbn_no}"
    result1 = execute_read_query(exist_book)
    if not result1:
        return jsonify({"error":"book is not exist"}), 404
    else:
        delete_book = f""" delete from book where isbn_no = {isbn_no}"""
        execute_query(delete_book)
        select_book = "SELECT * from book"
        all_books = execute_read_query(select_book) 
        return jsonify("Book deleted successfully!"),200

@app.post('/members')
def create_member():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    member_id = data.get('member_id')
    name = data.get('name')
    age = data.get('age')
    email = data.get('email')
    years_of_experience = data.get('years_of_experience')

    if not member_id or not name or not age or not email or not years_of_experience:
        return jsonify({"error": "All fields are required"}), 400
    
    if member_id < 0:
        return jsonify({"error": "member_id must be positive"}), 400
    
    if years_of_experience < 0:
        return jsonify({"error": "years of experience must be positive"}), 400
    
    if age < 0 or age > 120:
        return jsonify({"error": "Please enter a valid age"}), 400

    exist_member = f"SELECT  * FROM member WHERE member_id={member_id}" 
    result2 = execute_read_query(exist_member)
    if result2:
        return jsonify({"error":"member already exist"}), 400
    else:
        insert_member = f"""insert into member (member_id, name, age, email, years_of_experience) values({member_id}, '{name}', {age}, '{email}',{years_of_experience})"""
        execute_query(insert_member)
        return jsonify("Member inserted successfully!"),201

@app.delete('/members/<int:member_id>')
def delete_member(member_id):
    exist_book = f"SELECT * FROM member where member_id={member_id}"
    result_delete_memebr = execute_read_query(exist_book)
    if not result_delete_memebr:
        return jsonify({"error":"member is not exist"}), 404
    else:
        delete_member = f""" delete from member where member_id = {member_id}"""
        execute_query(delete_member)
        select_member = "SELECT * from member"
        all_members = execute_read_query(select_member) 
        return jsonify("Member deleted successfully!"),200

@app.get('/books/<int:isbn_no>')
def get_book(isbn_no):
    search_query_by_id = f"SELECT * FROM book WHERE isbn_no = {isbn_no}"
    result_search = execute_read_query(search_query_by_id)
    if not result_search:
        return jsonify({"error":"Book is not exist"}), 404
    else:
        return jsonify(book_to_dict(result_search[0]))

@app.get('/books/search')
def search_book():
    title = request.args.get('title')
    author = request.args.get('author')
    
    if title:
        search_query_by_title = f"SELECT * FROM book WHERE title = '{title}'"
        result = execute_read_query(search_query_by_title)
        if result:
            return jsonify(book_to_dict(result[0])), 200
        else:
            return jsonify({"error": "No book found"}), 404
    elif author:
       search_query_by_author = f"SELECT * FROM book WHERE author = '{author}'"
       result = execute_read_query(search_query_by_author)
       if result:
            return jsonify(book_to_dict(result[0])), 200
       else:
            return jsonify({"error": "No book found"}), 404
    else:
        
        return jsonify({"message:" "provide title or author for search"}), 400

@app.get('/members/<int:member_id>')
def get_member(member_id):
    search_query_by_member_id = f"SELECT * FROM member WHERE member_id = {member_id}"
    result_search_member = execute_read_query(search_query_by_member_id) 
    if not result_search_member:
        return jsonify({"error": "Member not exist"}), 404
        
    else:
        return jsonify(member_to_dict(result_search_member[0]))


@app.put('/books/<int:isbn_no>/borrow')
def borrow_book(isbn_no):
    data = request.get_json()
    member_id = data['member_id']
    exist_member = f"SELECT * FROM member where member_id={member_id}"
    member_result = execute_read_query(exist_member)
    if not member_result:
        return jsonify({"error":"Member not registered"}), 404
    else:
        exist_book = f"SELECT * FROM book where isbn_no={isbn_no}"
        book_result = execute_read_query(exist_book)
        if not book_result:
            return jsonify({"error":"Book not found"}), 400
        else:
            already_borrowed_book = f"SELECT * FROM book where isbn_no = {isbn_no} AND is_borrowed=1"
            borrowed_result = execute_read_query(already_borrowed_book)
            if borrowed_result:
                return jsonify({"error":"Book is already borrowed"}), 400
            else:
                count_books_borrowed = f"SELECT * FROM book where borrowed_by = {member_id}"
                count_book_result = execute_read_query(count_books_borrowed)
                if len(count_book_result)>=2:
                    return jsonify({"error" : "you can't borrow more than 2 books"}), 400
                else:
                    update_book = f"update book set is_borrowed = 1, borrowed_by = {member_id} where isbn_no = {isbn_no}"
                    b_result = execute_query(update_book)
                    return jsonify({"Message" : "book is borrowed successfully"}), 200
                
@app.put('/books/<int:isbn_no>/return')
def return_book(isbn_no):
    data = request.get_json()
    member_id = data['member_id']
    exist_member = f"SELECT * FROM member where member_id={member_id}"
    member_result = execute_read_query(exist_member)
    if not member_result:
        return jsonify({"error" : "Member not registered"}), 404
    else:
        exist_book = f"SELECT * FROM book where isbn_no={isbn_no}"
        book_result = execute_read_query(exist_book)
        if not book_result:
            return jsonify({"error" : "Book not found"}), 400
        else:
            borrowed_book_by_member = f"SELECT * FROM book where isbn_no = {isbn_no} AND borrowed_by = {member_id}"
            borrowed_result_by_member = execute_read_query(borrowed_book_by_member)
            if not borrowed_result_by_member:
                return jsonify({"error":"This member didn't borrow the book"}), 400
            else:
                update_book1 = f"update book set is_borrowed = 0, borrowed_by = Null where isbn_no = {isbn_no}"
                update_book1_result = execute_query(update_book1)
                return jsonify({"Message" : "book returned successfully"}),200

    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)