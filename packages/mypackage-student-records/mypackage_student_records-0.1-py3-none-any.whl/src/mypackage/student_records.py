import mysql.connector
import os

# Import MySQL configuration from environment variables
mysql_database = os.environ.get("MYSQL_DATABASE")
mysql_user = os.environ.get("MYSQL_USER")
mysql_password = os.environ.get("MYSQL_PASSWORD")
mysql_host = os.environ.get("MYSQL_HOST")


def establish_connection():
    try:
        db_connection = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_database,
            port=3306
        )
        return db_connection
    except mysql.connector.Error:
        return None

# Function to add a new student
def add_student(db_connection, student_name, student_email):
    cursor = db_connection.cursor()
    query = "INSERT INTO students (student_name, student_email) VALUES (%s, %s)"
    values = (student_name, student_email)
    cursor.execute(query, values)
    db_connection.commit()
    print("Student added successfully!")
    return True

# Function to add a grade for a student
def add_grade(db_connection, student_id, course_name, grade):
    cursor = db_connection.cursor()
    query = "INSERT INTO grades (student_id, course_name, grade) VALUES (%s, %s, %s)"
    values = (student_id, course_name, grade)
    cursor.execute(query, values)
    db_connection.commit()
    print("Grade added successfully!")
    return True


# Function to view grades for a specific student
def view_grades(db_connection, student_id):
    cursor = db_connection.cursor()
    query = "SELECT * FROM grades WHERE student_id = %s"
    values = (student_id,)
    cursor.execute(query, values)
    grades = cursor.fetchall()

    return grades


# Function to view a list of all students
def view_students(db_connection):
    cursor = db_connection.cursor()
    query = "SELECT * FROM students"
    cursor.execute(query)
    students = cursor.fetchall()

    return students

# Function to update a student's grade
def update_grade(db_connection, grade_id, new_grade):
    cursor = db_connection.cursor()
    query = "UPDATE grades SET grade = %s WHERE grade_id = %s"
    values = (new_grade, grade_id)
    cursor.execute(query, values)
    db_connection.commit()
    print("Grade updated successfully!")
    return True

# Function to delete a student and their associated grades
def delete_student(db_connection, student_id):
    cursor = db_connection.cursor()
    query = "DELETE FROM students WHERE student_id = %s"
    values = (student_id,)
    cursor.execute(query, values)

    # Delete associated grades
    query = "DELETE FROM grades WHERE student_id = %s"
    cursor.execute(query, values)

    db_connection.commit()
    print("Student and associated grades deleted successfully!")
    return True