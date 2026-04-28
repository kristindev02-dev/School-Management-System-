from flask import Flask, render_template, request, redirect, url_for, flash
import database
import sqlite3   # ✅ IMPORTANT

app = Flask(__name__)
app.secret_key = "secret_key_for_session"

# ==========================================================
# DATABASE INIT
# ==========================================================
database.init_db()

# ==========================================================
# HOME
# ==========================================================
@app.route('/')
def index():
    return redirect(url_for('students_page'))

# ==========================================================
# STUDENTS
# ==========================================================
@app.route('/students', methods=['GET', 'POST'])
def students_page():
    if request.method == 'POST':
        try:
            database.add_student(
                request.form.get('name'),
                request.form.get('age'),
                request.form.get('date_of_birth'),
                request.form.get('email'),
                request.form.get('address'),
                request.form.get('phone')
            )
            flash("Student added successfully!", "success")

        except Exception as e:
            flash(f"Error adding student: {e}", "danger")

        return redirect(url_for('students_page'))

    return render_template('students.html',
                           students=database.get_all_students())


@app.route('/students/<int:student_id>/update', methods=['POST'])
def update_student(student_id):
    try:
        database.update_student(
            student_id,
            request.form.get('name'),
            request.form.get('age'),
            request.form.get('date_of_birth') or None,
            request.form.get('email'),
            request.form.get('address'),
            request.form.get('phone')
        )
        flash("Student updated successfully!", "info")

    except Exception as e:
        flash(f"Error updating student: {e}", "danger")

    return redirect(url_for('students_page'))


@app.route('/students/<int:id>/delete', methods=['POST'])
def remove_student(id):
    try:
        database.delete_student(id)
        flash("Student deleted successfully!", "warning")

    except sqlite3.IntegrityError:
        flash("Cannot delete student: enrolled in courses.", "danger")

    except sqlite3.OperationalError as e:
        flash(f"Database error: {e}", "danger")

    return redirect(url_for('students_page'))

# ==========================================================
# TEACHERS
# ==========================================================
@app.route('/teachers', methods=['GET', 'POST'])
def teachers_page():
    if request.method == 'POST':
        try:
            database.add_teacher(
                request.form.get('name'),
                request.form.get('email'),
                request.form.get('degree'),
                request.form.get('hire_date') or None
            )
            flash("Teacher added successfully!", "success")

        except Exception as e:
            flash(f"Error adding teacher: {e}", "danger")

        return redirect(url_for('teachers_page'))

    return render_template('teachers.html',
                           teachers=database.get_all_teachers())


@app.route('/teachers/<int:teacher_id>/update', methods=['POST'])
def update_teacher(teacher_id):
    try:
        database.update_teacher(
            teacher_id,
            request.form.get('name'),
            request.form.get('email'),
            request.form.get('degree'),
            request.form.get('hire_date')
        )
        flash("Teacher updated successfully!", "info")

    except Exception as e:
        flash(f"Error updating teacher: {e}", "danger")

    return redirect(url_for('teachers_page'))


@app.route('/teachers/<int:id>/delete', methods=['POST'])
def remove_teacher(id):
    try:
        database.delete_teacher(id)
        flash("Teacher deleted successfully!", "warning")

    except sqlite3.IntegrityError:
        flash("Cannot delete teacher: assigned to a course.", "danger")

    except sqlite3.OperationalError as e:
        flash(f"Database error: {e}", "danger")

    return redirect(url_for('teachers_page'))

# ==========================================================
# COURSES
# ==========================================================
@app.route('/courses', methods=['GET', 'POST'])
def courses_page():
    if request.method == 'POST':
        try:
            database.add_course(
                request.form.get('name'),
                request.form.get('teacher_id'),
                request.form.get('credits'),
                request.form.get('description')
            )
            flash("Course added successfully!", "success")

        except Exception as e:
            flash(f"Error adding course: {e}", "danger")

        return redirect(url_for('courses_page'))

    return render_template('courses.html',
                           courses=database.get_all_courses(),
                           teachers=database.get_all_teachers())


@app.route('/courses/<int:course_id>/update', methods=['POST'])
def update_course(course_id):
    try:
        database.update_course(
            course_id,
            request.form.get('name'),
            request.form.get('teacher_id'),
            request.form.get('credits'),
            request.form.get('description')
        )
        flash("Course updated successfully!", "info")

    except Exception as e:
        flash(f"Error updating course: {e}", "danger")

    return redirect(url_for('courses_page'))


@app.route('/courses/<int:id>/delete', methods=['POST'])
def remove_course(id):
    try:
        database.delete_course(id)
        flash("Course deleted successfully!", "warning")

    except sqlite3.IntegrityError:
        flash("Cannot delete course: students are enrolled.", "danger")

    except sqlite3.OperationalError as e:
        flash(f"Database error: {e}", "danger")

    return redirect(url_for('courses_page'))

# ==========================================================
# ENROLLMENT
# ==========================================================
@app.route('/enrollment')
def enrollment_page():
    return render_template('enrollment.html',
                           enrollment=database.get_all_enrollments(),
                           students=database.get_all_students(),
                           courses=database.get_all_courses())


@app.route('/enrollment', methods=['POST'])
def add_enrollment():
    try:
        database.add_enrollment(
            request.form.get('student_id'),
            request.form.get('course_id'),
            request.form.get('status'),
            request.form.get('enrollment_date')
        )
        flash("Enrollment added successfully!", "success")

    except Exception as e:
        flash(f"Error adding enrollment: {e}", "danger")

    return redirect(url_for('enrollment_page'))


@app.route('/enrollment/<int:enrollment_id>/update', methods=['POST'])
def update_enrollment(enrollment_id):
    try:
        database.update_enrollment(
            enrollment_id,
            request.form.get('student_id'),
            request.form.get('course_id'),
            request.form.get('status'),
            request.form.get('enrollment_date')
        )
        flash("Enrollment updated successfully!", "info")

    except Exception as e:
        flash(f"Error updating enrollment: {e}", "danger")

    return redirect(url_for('enrollment_page'))


@app.route('/enrollment/<int:enrollment_id>/delete', methods=['POST'])
def delete_enrollment(enrollment_id):
    try:
        database.delete_enrollment(enrollment_id)
        flash("Enrollment deleted successfully!", "warning")

    except Exception as e:
        flash(f"Error deleting enrollment: {e}", "danger")

    return redirect(url_for('enrollment_page'))

# ==========================================================
# RUN
# ==========================================================
if __name__ == '__main__':
    app.run(debug=True)