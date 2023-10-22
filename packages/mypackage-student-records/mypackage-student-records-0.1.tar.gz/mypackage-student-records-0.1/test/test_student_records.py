from src.mypackage.student_records import add_student, add_grade, view_grades, view_students, update_grade, delete_student, establish_connection

def test_establish_connection():
    connection = establish_connection()
    assert connection is not None
    connection.close()

def test_add_student():
    connection = establish_connection()
    assert connection is not None
    
    student_name = "John Doe"
    student_email = "john.doe@example.com"
    
    result = add_student(connection, student_name, student_email)
    assert result is True
    
    connection.close()

def test_add_grade():
    connection = establish_connection()
    assert connection is not None
    
    # Add a grade for the test student
    student_id = 1  # Assuming this is the ID of the newly added student
    course_name = "Math"
    grade = 90
    result = add_grade(connection, student_id, course_name, grade)
    assert result is True
    
    connection.close()

def test_view_grades():
    connection = establish_connection()
    student_id = 1  # Replace with a valid student_id
    
    # Act
    grades = view_grades(connection, student_id)
    
    assert isinstance(grades, list)


def test_view_student():
    connection = establish_connection()
    assert connection is not None

    students = view_students(connection)

    assert isinstance(students, list)

def test_update_grade():
    connection = establish_connection()
    assert connection is not None

    # Test updating a student's grade
    result = update_grade(connection, 1, "B")
    assert result is True

def test_delete_student():
    connection = establish_connection()
    assert connection is not None

    result = delete_student(connection, 1)
    assert result is True