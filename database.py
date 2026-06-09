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

        # ENROLLMENTS
        c.execute('''
            CREATE TABLE IF NOT EXISTS enrollments (
                enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                course_id INTEGER,
                status TEXT,
                enrollment_date DATE,
                FOREIGN KEY (student_id) REFERENCES students (student_id),
                FOREIGN KEY (course_id) REFERENCES courses (course_id)
            )
        ''')

        # Reset auto-increment counters for empty tables
        def reset_sequence(table, pk_name, base_id):
            c.execute(f'SELECT COUNT(*) FROM {table}')
            if c.fetchone()[0] == 0:
                c.execute('DELETE FROM sqlite_sequence WHERE name = ?', (table,))
                c.execute(f'INSERT OR IGNORE INTO {table} ({pk_name}) VALUES (?)', (base_id,))
                c.execute(f'DELETE FROM {table} WHERE {pk_name} = ?', (base_id,))

        reset_sequence('students', 'student_id', 1000)
        reset_sequence('teachers', 'teacher_id', 2000)
        reset_sequence('courses', 'course_id', 3000)
        reset_sequence('enrollments', 'enrollment_id', 4000)

        # Seed initial sample data when tables are empty
        c.execute('SELECT COUNT(*) FROM students')
        students_count = c.fetchone()[0]
        c.execute('SELECT COUNT(*) FROM teachers')
        teachers_count = c.fetchone()[0]
        c.execute('SELECT COUNT(*) FROM courses')
        courses_count = c.fetchone()[0]
        c.execute('SELECT COUNT(*) FROM enrollments')
        enrollments_count = c.fetchone()[0]

        if (
            students_count == 0
            and teachers_count == 0
            and courses_count == 0
            and enrollments_count == 0
        ):
            teacher_rows = [
                ('Alice Roberts', 'alice.roberts@example.com', 'Mathematics', '2022-08-15'),
                ('Brian Chen', 'brian.chen@example.com', 'Physics', '2021-09-01'),
                ('Clara Patel', 'clara.patel@example.com', 'English Literature', '2023-01-10'),
            ]
            teacher_ids = []
            for name, email, degree, hire_date in teacher_rows:
                c.execute(
                    'INSERT INTO teachers (name, email, degree, hire_date) VALUES (?, ?, ?, ?)',
                    (name, email, degree, hire_date),
                )
                teacher_ids.append(c.lastrowid)

            student_rows = [
                ('Mia Suzuki', 15, '2008-04-20', 'mia.suzuki@example.com', '123 Sakura St.', '09012345678'),
                ('Noah Tanaka', 17, '2006-11-05', 'noah.tanaka@example.com', '456 Maple Ave.', '08023456789'),
                ('Emma Yamamoto', 16, '2007-07-18', 'emma.yamamoto@example.com', '789 Cherry Rd.', '07034567890'),
            ]
            student_ids = []
            for name, age, dob, email, address, phone in student_rows:
                c.execute(
                    'INSERT INTO students (name, age, date_of_birth, email, address, phone) VALUES (?, ?, ?, ?, ?, ?)',
                    (name, age, dob, email, address, phone),
                )
                student_ids.append(c.lastrowid)

            course_rows = [
                ('Algebra I', teacher_ids[0], 4, 'Fundamentals of algebra and problem solving'),
                ('Physics I', teacher_ids[1], 3, 'Mechanics, motion, and energy'),
                ('English Composition', teacher_ids[2], 3, 'Writing, reading, and literary analysis'),
            ]
            course_ids = []
            for course_name, teacher_id, credits, description in course_rows:
                c.execute(
                    'INSERT INTO courses (course_name, teacher_id, credits, description) VALUES (?, ?, ?, ?)',
                    (course_name, teacher_id, credits, description),
                )
                course_ids.append(c.lastrowid)

            enrollment_rows = [
                (student_ids[0], course_ids[0], 'Active', '2024-09-01'),
                (student_ids[1], course_ids[1], 'Active', '2024-09-02'),
                (student_ids[2], course_ids[2], 'Completed', '2024-02-15'),
            ]
            for student_id, course_id, status, enrollment_date in enrollment_rows:
                c.execute(
                    'INSERT INTO enrollments (student_id, course_id, status, enrollment_date) VALUES (?, ?, ?, ?)',
                    (student_id, course_id, status, enrollment_date),
                )


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
    students, _ = get_students(page=None, per_page=None)
    return students


def get_students(search_text=None, page=None, per_page=5):
    with get_connection() as conn:
        query = 'SELECT * FROM students'
        count_query = 'SELECT COUNT(*) FROM students'
        filters = []
        params = []

        if search_text:
            filters.append('(name LIKE ? OR address LIKE ?)')
            params.extend([f'%{search_text}%', f'%{search_text}%'])

        if filters:
            where_clause = ' WHERE ' + ' AND '.join(filters)
            query += where_clause
            count_query += where_clause

        query += ' ORDER BY student_id ASC'

        if page and per_page:
            offset = (page - 1) * per_page
            query += f' LIMIT {per_page} OFFSET {offset}'

        results = conn.execute(query, params).fetchall()
        total = conn.execute(count_query, params).fetchone()[0]

        return results, total


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
    teachers, _ = get_teachers(page=None, per_page=None)
    return teachers


def get_teachers(search_text=None, start_date=None, end_date=None, page=None, per_page=5):
    with get_connection() as conn:
        query = 'SELECT * FROM teachers'
        count_query = 'SELECT COUNT(*) FROM teachers'
        filters = []
        params = []

        if search_text:
            filters.append('name LIKE ?')
            params.append(f'%{search_text}%')

        if start_date:
            filters.append('hire_date >= ?')
            params.append(start_date)

        if end_date:
            filters.append('hire_date <= ?')
            params.append(end_date)

        if filters:
            where_clause = ' WHERE ' + ' AND '.join(filters)
            query += where_clause
            count_query += where_clause

        query += ' ORDER BY teacher_id ASC'

        if page and per_page:
            offset = (page - 1) * per_page
            query += f' LIMIT {per_page} OFFSET {offset}'

        results = conn.execute(query, params).fetchall()
        total = conn.execute(count_query, params).fetchone()[0]

        return results, total


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
    courses, _ = get_courses(page=None, per_page=None)
    return courses


def get_courses(search_text=None, page=1, per_page=5):
    with get_connection() as conn:
        query = '''
            SELECT c.*, t.name as teacher_name, t.degree
            FROM courses c
            LEFT JOIN teachers t ON c.teacher_id = t.teacher_id
        '''
        count_query = 'SELECT COUNT(*) FROM courses c'
        filters = []
        params = []

        if search_text:
            filters.append('(c.course_name LIKE ? OR t.name LIKE ?)')
            params.extend([f'%{search_text}%', f'%{search_text}%'])
            count_query += ' LEFT JOIN teachers t ON c.teacher_id = t.teacher_id WHERE ' + ' AND '.join(filters)

        if filters:
            query += ' WHERE ' + ' AND '.join(filters)

        query += ' ORDER BY c.course_id ASC'

        if page and per_page:
            offset = (page - 1) * per_page
            query += f' LIMIT {per_page} OFFSET {offset}'

        results = conn.execute(query, params).fetchall()
        total = conn.execute(count_query, params).fetchone()[0]

        return results, total


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
    enrollments, _ = get_enrollments()
    return enrollments


def get_enrollments(search_text=None, status=None, start_date=None, end_date=None, page=1, per_page=5):
    with get_connection() as conn:
        base_query = '''
            SELECT e.*, s.name as student_name, c.course_name
            FROM enrollments e
            LEFT JOIN students s ON e.student_id = s.student_id
            LEFT JOIN courses c ON e.course_id = c.course_id
        '''
        count_query = '''
            SELECT COUNT(*)
            FROM enrollments e
            LEFT JOIN students s ON e.student_id = s.student_id
            LEFT JOIN courses c ON e.course_id = c.course_id
        '''
        filters = []
        params = []

        if search_text:
            filters.append('(s.name LIKE ? OR c.course_name LIKE ?)')
            params.extend([f'%{search_text}%', f'%{search_text}%'])

        if status:
            filters.append('e.status = ?')
            params.append(status)

        if start_date:
            filters.append('e.enrollment_date >= ?')
            params.append(start_date)

        if end_date:
            filters.append('e.enrollment_date <= ?')
            params.append(end_date)

        if filters:
            where_clause = ' WHERE ' + ' AND '.join(filters)
            base_query += where_clause
            count_query += where_clause

        base_query += ' ORDER BY e.enrollment_id ASC'
        if page and per_page:
            offset = (page - 1) * per_page
            base_query += f' LIMIT {per_page} OFFSET {offset}'

        results = conn.execute(base_query, params).fetchall()
        total = conn.execute(count_query, params).fetchone()[0]

        return results, total


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

def get_unique_student_count():
    with get_connection() as conn:
        # If you don't use DISTINCT, it just counts all rows
        cursor = conn.execute("SELECT COUNT(DISTINCT student_id) FROM enrollments")
        return cursor.fetchone()[0]
