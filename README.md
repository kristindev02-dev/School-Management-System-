# School Management System

This project is a simple web-based school management system built with Flask and SQLite. It helps manage students, teachers, courses, and enrollments in one place.

## Introduction

The purpose of this project is to reduce the difficulty of handling school records manually. In many schools, information about students, teachers, subjects, and enrollment is written on paper or stored in separate files. This can lead to errors, wasted time, and difficulty finding information quickly.

This system solves that problem by placing important school data into one organized application. The user can open the website, manage records, and view school information in a simple and structured way.

## What It Is Used For

The system is used to:

Solution:
- One web-based system with clean modules.
- Validated data input before saving.
- Structured relational database.
- Instant user feedback with toast    messages.

## Problem It Solves

This project helps solve common school management problems such as:

- scattered records in different places
- difficulty updating student or teacher information
- slow manual tracking of courses and enrollments
- lack of a quick summary of school data
- risk of mistakes when handling records manually

## How It Functions

The application works through a Flask web app connected to an SQLite database.

1. When the app starts, it creates the database tables if they do not already exist.
2. Sample data is inserted when the database is empty.
3. Users interact with pages for students, teachers, courses, and enrollment.
4. Form data is validated before being saved.
5. The system stores and retrieves data from the database and shows it in HTML pages.

## System Workflow

The system follows a simple workflow:

1. The user opens the application in the browser.
2. The user chooses a page such as Students, Teachers, Courses, or Enrollment.
3. The user fills in a form to add or update information.
4. Flask receives the form data from the page.
5. The application checks the data to make sure it is valid.
6. The data is saved into the SQLite database.
7. The updated records are displayed back on the page.

This means the project works as a complete cycle of input, processing, storage, and output.

## Main Features

- student management
- teacher management
- course management
- enrollment management
- search and filter options
- pagination for records
- dashboard summary cards
- input validation with error messages

## Detailed Function of Each Section

### Dashboard

The dashboard shows a quick summary of the system. It displays the total number of students, teachers, courses, and enrolled students. This helps the user understand the current state of the school records at a glance.

### Students

The student section is used to store and manage student information such as name, age, date of birth, email, address, and phone number. The user can add new students, update their details, search for them, and delete records when needed.

### Teachers

The teacher section keeps information about teachers, including their name, email, degree, and hire date. It also allows searching and filtering, which helps the user find teacher records more easily.

### Courses

The course section is used to create subjects or courses offered by the school. Each course can be connected to a teacher and can include credits and a short description.

### Enrollment

The enrollment section connects students to courses. It stores which student is enrolled in which course, the enrollment status, and the enrollment date. This helps the system track academic participation clearly.

## Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- Jinja templates

## Why These Technologies Were Used

- Python was used because it is simple and easy to understand.
- Flask was used to build the web application and handle routes.
- SQLite was used because it is lightweight and easy to set up.
- HTML and CSS were used to build the user interface.
- Jinja templates were used to connect backend data with frontend pages.

## Project Structure

- `app.py` - main Flask application and routes
- `database.py` - database setup and database functions
- `templates/` - HTML pages for the interface
- `static/` - CSS and image files

## Database Structure

The system uses four main tables:

- Students
- Teachers
- Courses
- Enrollments

These tables are connected so the system can manage relationships between students, teachers, and courses.

- A teacher can be assigned to a course.
- A student can be enrolled in a course.
- Enrollment acts as the link between students and courses.

## Pages in the System

- Dashboard
- Students
- Teachers
- Courses
- Enrollment

## How To Run

1. Install Python.
2. Install Flask:

```bash
pip install flask
```

3. Run the project:

```bash
python app.py
```

4. Open your browser and go to:

```text
http://127.0.0.1:5000
```

## Advantages of the System

- easy to use
- organized data storage
- faster record management
- reduced manual work
- simple and clean interface
- useful for demonstration and academic projects

## Presentation Summary

This system is designed to make school record management easier. Instead of storing information manually, the user can manage students, teachers, courses, and enrollments in one web application. The system also provides a dashboard for a quick overview of school data.

In simple terms, the project accepts school information from the user, processes it through Flask, stores it in SQLite, and displays the results on web pages. It is a practical example of how a database-driven web system can help manage real-world information efficiently.

## Conclusion

The School Management System is a simple but useful application that demonstrates how web development can be used to manage educational records. It combines a backend, a database, and a frontend interface into one complete system. This makes it suitable for learning, academic presentation, and basic record management tasks.