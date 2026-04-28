import sqlite3

DB_NAME = 'school.db'

# ==========================================================
# INIT DATABASE
# ==========================================================
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('PRAGMA foreign_keys = ON')
        c = conn.cursor()

        # STUDENTS
        c.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                date_of_birth DATE,
                email TEXT,
                address TEXT,
                phone TEXT
            )
        ''')

        # TEACHERS
        c.execute('''
            CREATE TABLE IF NOT EXISTS teachers (
                teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                degree TEXT,
                hire_date DATE
            )
        ''')

        # COURSES
        c.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_name TEXT NOT NULL,
                teacher_id INTEGER,
                credits INTEGER,
                description TEXT,
                FOREIGN KEY (teacher_id) REFERENCES teachers (teacher_id)
            )
        ''')

        # ENROLLMENTS (NO CASCADE → will show error)
        c.execute('''
            CREATE TABLE IF NOT EXISTS enrollments (
                enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                course_id INTEGER,
                status TEXT,
                enrollment_date TEXT,
                FOREIGN KEY (student_id) REFERENCES students (student_id),
                FOREIGN KEY (course_id) REFERENCES courses (course_id)
            )
        ''')


# ==========================================================
# CONNECTION
# ==========================================================
def get_connection():
    conn = sqlite3.connect(DB_NAME, timeout=30)
    conn.execute('PRAGMA foreign_keys = ON')
    conn.row_factory = sqlite3.Row
    return conn


# ==========================================================
# STUDENTS
# ==========================================================
def get_all_students():
    with get_connection() as conn:
        return conn.execute(
            'SELECT * FROM students ORDER BY student_id ASC'
        ).fetchall()


def add_student(name, age, date_of_birth, email, address, phone):
    with get_connection() as conn:
        conn.execute('''
            INSERT INTO students (name, age, date_of_birth, email, address, phone)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, age, date_of_birth, email, address, phone))


def update_student(student_id, name, age, date_of_birth, email, address, phone):
    with get_connection() as conn:
        conn.execute('''
            UPDATE students
            SET name=?, age=?, date_of_birth=?, email=?, address=?, phone=?
            WHERE student_id=?
        ''', (name, age, date_of_birth, email, address, phone, student_id))


def delete_student(student_id):
    with get_connection() as conn:
        conn.execute(
            'DELETE FROM students WHERE student_id=?',
            (student_id,)
        )


# ==========================================================
# TEACHERS
# ==========================================================
def get_all_teachers():
    with get_connection() as conn:
        return conn.execute(
            'SELECT * FROM teachers ORDER BY teacher_id ASC'
        ).fetchall()


def add_teacher(name, email, degree, hire_date):
    with get_connection() as conn:
        conn.execute('''
            INSERT INTO teachers (name, email, degree, hire_date)
            VALUES (?, ?, ?, ?)
        ''', (name, email, degree, hire_date))


def update_teacher(teacher_id, name, email, degree, hire_date):
    with get_connection() as conn:
        conn.execute('''
            UPDATE teachers
            SET name=?, email=?, degree=?, hire_date=?
            WHERE teacher_id=?
        ''', (name, email, degree, hire_date, teacher_id))


def delete_teacher(teacher_id):
    with get_connection() as conn:
        conn.execute(
            'DELETE FROM teachers WHERE teacher_id=?',
            (teacher_id,)
        )


# ==========================================================
# COURSES
# ==========================================================
def get_all_courses():
    with get_connection() as conn:
        return conn.execute('''
            SELECT c.*, t.name as teacher_name, t.degree
            FROM courses c
            LEFT JOIN teachers t ON c.teacher_id = t.teacher_id
            ORDER BY c.course_id ASC
        ''').fetchall()


def add_course(course_name, teacher_id, credits, description):
    with get_connection() as conn:
        conn.execute('''
            INSERT INTO courses (course_name, teacher_id, credits, description)
            VALUES (?, ?, ?, ?)
        ''', (course_name, teacher_id, credits, description))


def update_course(course_id, course_name, teacher_id, credits, description):
    with get_connection() as conn:
        conn.execute('''
            UPDATE courses
            SET course_name=?, teacher_id=?, credits=?, description=?
            WHERE course_id=?
        ''', (course_name, teacher_id, credits, description, course_id))


def delete_course(course_id):
    with get_connection() as conn:
        conn.execute(
            'DELETE FROM courses WHERE course_id=?',
            (course_id,)
        )


# ==========================================================
# ENROLLMENTS
# ==========================================================
def get_all_enrollments():
    with get_connection() as conn:
        return conn.execute('''
            SELECT e.*, s.name as student_name, c.course_name
            FROM enrollments e
            LEFT JOIN students s ON e.student_id = s.student_id
            LEFT JOIN courses c ON e.course_id = c.course_id
            ORDER BY e.enrollment_id ASC
        ''').fetchall()


def add_enrollment(student_id, course_id, status, enrollment_date):
    with get_connection() as conn:
        conn.execute('''
            INSERT INTO enrollments (student_id, course_id, status, enrollment_date)
            VALUES (?, ?, ?, ?)
        ''', (student_id, course_id, status, enrollment_date))


def update_enrollment(enrollment_id, student_id, course_id, status, enrollment_date):
    with get_connection() as conn:
        conn.execute('''
            UPDATE enrollments
            SET student_id=?, course_id=?, status=?, enrollment_date=?
            WHERE enrollment_id=?
        ''', (student_id, course_id, status, enrollment_date, enrollment_id))


def delete_enrollment(enrollment_id):
    with get_connection() as conn:
        conn.execute(
            'DELETE FROM enrollments WHERE enrollment_id=?',
            (enrollment_id,)
        )