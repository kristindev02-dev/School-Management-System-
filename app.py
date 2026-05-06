from flask import Flask, render_template, request, redirect, url_for, flash
import re  # ✅ IMPORTANT
import database
import sqlite3  # ✅ IMPORTANT

app = Flask(__name__)
app.secret_key = "secret_key_for_session"

# ==========================================================
# DATABASE INIT
# ==========================================================
database.init_db()


# ==========================================================
# HOME
# ==========================================================
@app.route("/")
def index():
    return redirect(url_for("students_page"))


@app.route("/dashboard")
def dashboard_page():
    students, total_students = database.get_students(page=None, per_page=None)
    teachers, total_teachers = database.get_teachers(page=None, per_page=None)
    courses, total_courses = database.get_courses(page=None, per_page=None)
    enrollments, total_enrollments = database.get_enrollments(page=None, per_page=None) 
    
    unique_enrollment_count = database.get_unique_student_count()

    return render_template(
        "dashboard.html",
        total_students=total_students,
        total_teachers=total_teachers,
        total_courses=total_courses,
        unique_total=unique_enrollment_count
    )


# ==========================================================
# STUDENTS
# ==========================================================

@app.route("/students", methods=["GET", "POST"])
def students_page():
    if request.method == "POST":
        try:
            name = request.form.get("name", "").strip()
            age = request.form.get("age", "").strip()
            dob = request.form.get("date_of_birth", "").strip()
            email = request.form.get("email", "").strip()
            address = request.form.get("address", "").strip()
            phone = request.form.get("phone", "").strip()

            # =========================
            # VALIDATION
            # =========================

            if not re.match(r'^[A-Za-z .- 0-9]{2,50}$', name):
                flash("Enter a valid name (2–50 characters).", "danger")
                return redirect(url_for("students_page"))

            if not age.isdigit() or not (10 < int(age) <= 100):
                flash("Age must be greater than 10", "danger")
                return redirect(url_for("students_page"))

            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                flash("Invalid email format", "danger")
                return redirect(url_for("students_page"))

            if not re.match(r'^\d{7,15}$', phone):
                flash("Phone must be 7–15 digits", "danger")
                return redirect(url_for("students_page"))

            if len(address) < 5:
                flash("Address must be at least 5 characters", "danger")
                return redirect(url_for("students_page"))

            # =========================
            # ORIGINAL LOGIC (UNCHANGED)
            # =========================
            database.add_student(
                name,
                age,
                dob,
                email,
                address,
                phone,
            )

            flash("Student added successfully!", "success")

        except Exception as e:
            flash(f"Error adding student: {e}", "danger")

        return redirect(url_for("students_page"))
    
    
    search = request.args.get("search", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 5

    students, total = database.get_students(
        search_text=search or None, page=page, per_page=per_page
    )
    total_pages = (total + per_page - 1) // per_page
    start = ((page or 1) - 1) * per_page + 1 if total > 0 else 0
    end = min((page or 1) * per_page, total)

    return render_template(
        "students.html",
        students=students,
        search=search,
        page=page,
        total_pages=total_pages,
        total=total,
        start=start,
        end=end,
    )


@app.route("/students/<int:student_id>/update", methods=["POST"])

def update_student(student_id):
    try:
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        dob = request.form.get("date_of_birth", "").strip()
        email = request.form.get("email", "").strip()
        address = request.form.get("address", "").strip()
        phone = request.form.get("phone", "").strip()

        # =========================
        # VALIDATION
        # =========================

        # Name (allow letters, spaces, dots, hyphens, and numbers)
        if not re.match(r'^[A-Za-z .- 0-9]{2,50}$', name):
            flash("Enter a valid name (2–50 characters).", "danger")
            return redirect(url_for("students_page"))

        # Age
        if not age.isdigit() or not (10 < int(age) <= 100):
            flash("Age must be greater than 10", "danger")
            return redirect(url_for("students_page"))

        # Email
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            flash("Enter a valid email address.", "danger")
            return redirect(url_for("students_page"))

        # Phone
        if not re.match(r'^\d{7,15}$', phone):
            flash("Phone must be 7–15 digits", "danger")
            return redirect(url_for("students_page"))

        # Address
        if len(address) < 5:
            flash("Address must be at least 5 characters", "danger")
            return redirect(url_for("students_page"))

        # =========================
        # ORIGINAL LOGIC (UNCHANGED)
        # =========================
        database.update_student(
            student_id,
            request.form.get("name"),
            request.form.get("age"),
            request.form.get("date_of_birth") or None,
            request.form.get("email"),
            request.form.get("address"),
            request.form.get("phone"),
        )

        flash("Student updated successfully!", "info")

    except Exception as e:
        flash(f"Error updating student: {e}", "danger")

    return redirect(url_for("students_page"))


@app.route("/students/<int:id>/delete", methods=["POST"])
def remove_student(id):
    try:
        database.delete_student(id)
        flash("Student deleted successfully!", "warning")

    except sqlite3.IntegrityError:
        flash("Cannot delete student: enrolled in courses.", "danger")

    except sqlite3.OperationalError as e:
        flash(f"Database error: {e}", "danger")

    return redirect(url_for("students_page"))


@app.route("/students/delete_selected", methods=["POST"])
def delete_selected_students():
    selected_ids = request.form.getlist("selected_students")
    if selected_ids:
        try:
            for student_id in selected_ids:
                database.delete_student(int(student_id))
            flash(f"Deleted {len(selected_ids)} student(s) successfully!", "warning")
        except sqlite3.IntegrityError:
            flash(
                "Cannot delete one or more selected students: enrolled in courses.",
                "danger",
            )
        except sqlite3.OperationalError as e:
            flash(f"Database error deleting students: {e}", "danger")
        except Exception as e:
            flash(f"Error deleting students: {e}", "danger")
    else:
        flash("No students selected for deletion.", "info")

    return redirect(url_for("students_page"))


# ==========================================================
# TEACHERS
# ==========================================================
@app.route("/teachers", methods=["GET", "POST"])
def teachers_page():
    if request.method == "POST":
        try:
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip()
            degree = request.form.get("degree", "").strip()

            # =========================
            # VALIDATION
            # =========================

            # Name
            if not re.match(r'^[A-Za-z0-9 .- ()\]{2,50}$', name):
                flash("Enter a valid name (2–50 characters).", "warning")
                return redirect(url_for("teachers_page"))

            # Email
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                flash("Enter a valid email address.", "warning")
                return redirect(url_for("teachers_page"))

            # Degree
            if len(degree) < 2 or len(degree) > 100:
                flash("Degree must be 2–100 characters.", "warning")
                return redirect(url_for("teachers_page"))

            # =========================
            # ORIGINAL LOGIC (UNCHANGED)
            # =========================
            database.add_teacher(
                request.form.get("name"),
                request.form.get("email"),
                request.form.get("degree"),
                request.form.get("hire_date") or None,
            )

            flash("Teacher added successfully!", "success")

        except Exception as e:
            flash(f"Error adding teacher: {e}", "danger")

        return redirect(url_for("teachers_page"))

    query = request.args.get("query", "").strip()
    start_date = request.args.get("start_date", "").strip()
    end_date = request.args.get("end_date", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 5

    teachers, total = database.get_teachers(
        search_text=query or None,
        start_date=start_date or None,
        end_date=end_date or None,
        page=page,
        per_page=per_page,
    )
    total_pages = (total + per_page - 1) // per_page
    start = (page - 1) * per_page + 1 if total > 0 else 0
    end = min(page * per_page, total)

    return render_template(
        "teachers.html",
        teachers=teachers,
        query=query,
        start_date=start_date,
        end_date=end_date,
        page=page,
        total_pages=total_pages,
        total=total,
        start=start,
        end=end,
    )


@app.route("/teachers/<int:teacher_id>/update", methods=["POST"])

def update_teacher(teacher_id):
    try:
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        degree = request.form.get("degree", "").strip()

        # =========================
        # VALIDATION
        # =========================

        # Name (allow (), but no empty ())
        if not re.match(r'^(?!.*\(\))[A-Za-z0-9 .()\-]{2,50}$', name):
            flash("Name must be 2–50 characters (no empty ()).", "warning")
            return redirect(url_for("teachers_page"))

        # Email
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            flash("Enter a valid email address.", "warning")
            return redirect(url_for("teachers_page"))

        # Degree
        if len(degree) < 2 or len(degree) > 100:
            flash("Degree must be 2–100 characters.", "warning")
            return redirect(url_for("teachers_page"))

        # =========================
        # ORIGINAL LOGIC (UNCHANGED)
        # =========================
        database.update_teacher(
            teacher_id,
            request.form.get("name"),
            request.form.get("email"),
            request.form.get("degree"),
            request.form.get("hire_date"),
        )

        flash("Teacher updated successfully!", "info")

    except Exception as e:
        flash(f"Error updating teacher: {e}", "danger")

    return redirect(url_for("teachers_page"))


@app.route("/teachers/<int:id>/delete", methods=["POST"])
def remove_teacher(id):
    try:
        database.delete_teacher(id)
        flash("Teacher deleted successfully!", "warning")

    except sqlite3.IntegrityError:
        flash("Cannot delete teacher: assigned to a course.", "danger")

    except sqlite3.OperationalError as e:
        flash(f"Database error: {e}", "danger")

    return redirect(url_for("teachers_page"))


@app.route("/teachers/delete_selected", methods=["POST"])
def delete_selected_teachers():
    selected_ids = request.form.getlist("selected_teachers")
    if selected_ids:
        try:
            for teacher_id in selected_ids:
                database.delete_teacher(int(teacher_id))
            flash(f"Deleted {len(selected_ids)} teacher(s) successfully!", "warning")
        except Exception as e:
            flash(f"Error deleting teachers: {e}", "danger")
    else:
        flash("No teachers selected for deletion.", "info")

    return redirect(url_for("teachers_page"))


# ==========================================================
# COURSES
# ==========================================================
@app.route("/courses", methods=["GET", "POST"])
def courses_page():
    if request.method == "POST":
        try:
            name = request.form.get("name", "").strip()
            description = request.form.get("description", "").strip()

            # =========================
            # VALIDATION
            # =========================

            # Name
            if not re.match(r'^[A-Za-z0-9 .()\-]{2,100}$', name):
                flash("Name must be 2–100 characters.", "warning")
                return redirect(url_for("courses_page"))

            # Description
            if len(description) < 5 or len(description) > 255:
                flash("Description must be 5–255 characters.", "warning")
                return redirect(url_for("courses_page"))

            # =========================
            # ORIGINAL LOGIC (UNCHANGED)
            # =========================
            database.add_course(
                request.form.get("name"),
                request.form.get("teacher_id"),
                request.form.get("credits"),
                request.form.get("description"),
            )

            flash("Course added successfully!", "success")

        except Exception as e:
            flash(f"Error adding course: {e}", "danger")

        return redirect(url_for("courses_page"))

    search = request.args.get("search", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 5

    courses, total = database.get_courses(
        search_text=search or None, page=page, per_page=per_page
    )
    total_pages = (total + per_page - 1) // per_page
    start = (page - 1) * per_page + 1 if total > 0 else 0
    end = min(page * per_page, total)

    return render_template(
        "courses.html",
        courses=courses,
        teachers=database.get_all_teachers(),
        search=search,
        page=page,
        total_pages=total_pages,
        total=total,
        start=start,
        end=end,
    )

@app.route("/courses/<int:course_id>/update", methods=["POST"])
def update_course(course_id):
    try:
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()

        # =========================
        # VALIDATION
        # =========================

        # Name
        if not re.match(r'^[A-Za-z0-9 .()\-]{2,100}$', name):
            flash("Name must be 2–100 characters.", "warning")
            return redirect(url_for("courses_page"))

        # Description
        if len(description) < 5 or len(description) > 255:
            flash("Description must be 5–255 characters.", "warning")
            return redirect(url_for("courses_page"))

        # =========================
        # ORIGINAL LOGIC (UNCHANGED)
        # =========================
        database.update_course(
            course_id,
            request.form.get("name"),
            request.form.get("teacher_id"),
            request.form.get("credits"),
            request.form.get("description"),
        )

        flash("Course updated successfully!", "info")

    except Exception as e:
        flash(f"Error updating course: {e}", "danger")

    return redirect(url_for("courses_page"))


@app.route("/courses/<int:id>/delete", methods=["POST"])
def remove_course(id):
    try:
        database.delete_course(id)
        flash("Course deleted successfully!", "warning")

    except sqlite3.IntegrityError:
        flash("Cannot delete course: students are enrolled.", "danger")

    except sqlite3.OperationalError as e:
        flash(f"Database error: {e}", "danger")

    return redirect(url_for("courses_page"))


@app.route("/courses/delete_selected", methods=["POST"])
def delete_selected_courses():
    selected_ids = request.form.getlist("selected_courses")
    if selected_ids:
        try:
            for course_id in selected_ids:
                database.delete_course(int(course_id))
            flash(f"Deleted {len(selected_ids)} course(s) successfully!", "warning")
        except Exception as e:
            flash(f"Error deleting courses: {e}", "danger")
    else:
        flash("No courses selected for deletion.", "info")

    return redirect(url_for("courses_page"))


# ==========================================================
# ENROLLMENT
# ==========================================================
@app.route("/enrollment")
def enrollment_page():
    search_query = request.args.get("query", "").strip()
    status_filter = request.args.get("status", "").strip()
    start_date = request.args.get("start_date", "").strip()
    end_date = request.args.get("end_date", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 5

    enrollment, total = database.get_enrollments(
        search_text=search_query or None,
        status=status_filter or None,
        start_date=start_date or None,
        end_date=end_date or None,
        page=page,
        per_page=per_page,
    )
    total_pages = (total + per_page - 1) // per_page
    start = (page - 1) * per_page + 1 if total > 0 else 0
    end = min(page * per_page, total)
    
    # NEW: Get the unique count for the dashboard
    unique_count = database.get_unique_student_count()

    return render_template(
        "enrollment.html",
        enrollment=enrollment,
        students=database.get_all_students(),
        courses=database.get_all_courses(),
        query=search_query,
        status=status_filter,
        start_date=start_date,
        end_date=end_date,
        page=page,
        total_pages=total_pages,
        total=total,
        unique_total=unique_count,
        start=start,
        end=end,
    )


@app.route("/enrollment", methods=["POST"])
def add_enrollment():
    try:
        database.add_enrollment(
            request.form.get("student_id"),
            request.form.get("course_id"),
            request.form.get("status"),
            request.form.get("enrollment_date") or None,
        )
        flash("Enrollment added successfully!", "success")

    except Exception as e:
        flash(f"Error adding enrollment: {e}", "danger")

    return redirect(
        url_for(
            "enrollment_page",
            query=request.form.get("query") or None,
            status=request.form.get('filter_status') or None,
            start_date=request.form.get("start_date") or None,
            end_date=request.form.get("end_date") or None,
            page=int(request.form.get("page") or 1),
        )
    )


@app.route("/enrollment/<int:enrollment_id>/update", methods=["POST"])
def update_enrollment(enrollment_id):
    try:
        database.update_enrollment(
            enrollment_id,
            request.form.get("student_id"),
            request.form.get("course_id"),
            request.form.get("status"),
            request.form.get("enrollment_date") or None,
        )
        flash("Enrollment updated successfully!", "info")

    except Exception as e:
        flash(f"Error updating enrollment: {e}", "danger")


    return redirect(
    url_for(
        "enrollment_page",
        query=request.form.get("query") or None,
        status=request.form.get("filter_status") or None,
        start_date=request.form.get("start_date") or None,
        end_date=request.form.get("end_date") or None,
        page=int(request.form.get("page") or 1),
    )
)


@app.route("/enrollment/<int:enrollment_id>/delete", methods=["POST"])
def delete_enrollment(enrollment_id):
    try:
        database.delete_enrollment(enrollment_id)
        flash("Enrollment deleted successfully!", "warning")

    except Exception as e:
        flash(f"Error deleting enrollment: {e}", "danger")

    return redirect(url_for("enrollment_page"))


@app.route("/enrollment/delete_selected", methods=["POST"])
def delete_selected_enrollments():
    selected_ids = request.form.getlist("selected_enrollments")
    if selected_ids:
        try:
            for enrollment_id in selected_ids:
                database.delete_enrollment(int(enrollment_id))
            flash(f"Deleted {len(selected_ids)} enrollment(s) successfully!", "warning")
        except Exception as e:
            flash(f"Error deleting enrollments: {e}", "danger")
    else:
        flash("No enrollments selected for deletion.", "info")

    return redirect(url_for("enrollment_page"))


# ==========================================================
# RUN
# ==========================================================
if __name__ == "__main__":
    app.run(debug=True)
