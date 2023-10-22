from src.mypackage.student_records import add_student, add_grade, view_grades, delete_student, view_students, establish_connection

def test_establish_connection():
    connection = establish_connection()
    assert connection is not None
    connection.close()

def test_add_student_and_grades():
    connection = establish_connection()
    assert connection is not None

    # Test viewing grades for a specific student
    add_student(connection, "Alice Johnson", "alice@example.com")
    add_grade(connection, 1, "History", "B")

    result = view_grades(connection, 1)

    assert (1, 1, 'History', 'B') in result  # Check if the added grade is in the result


def test_delete_student_and_grades():
    connection = establish_connection()
    assert connection is not None

    # Test deleting a student and their associated grades
    add_student(connection, "Bob Wilsonn", "bobb@example.com")
    add_grade(connection, 2, "Math", "C")

    result = delete_student(connection, 6)
    assert result is True


def test_add_student_and_view_students():
    connection = establish_connection()
    assert connection is not None

    # Test adding a new student
    add_student(connection, "John Poe", "johnn@example.com")
    add_student(connection, "Alice Johnsonn", "alicee@example.com")
    add_student(connection, "Bob Wilson", "bob@example.com")
    result = view_students(connection)

    assert (3, 'John Poe', 'johnn@example.com') in result
    assert (4, 'Alice Johnsonn', 'alicee@example.com') in result
    assert (5, 'Bob Wilson', 'bob@example.com') in result


