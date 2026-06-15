# School Management System

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/kristindev02-dev/School-Management-System-.git
cd School-Management-System-
```

### 2. Create a virtual environment
```bash
python -m venv venv
```

Activate it:

**Windows**
```bash
venv\Scripts\activate
```

**macOS/Linux**
```bash
source venv/bin/activate
```

### 3. Install dependencies
Install Flask:
```bash
pip install flask
```

If you later add a `requirements.txt` file, you can use:
```bash
pip install -r requirements.txt
```

### 4. Set up the database
This project uses SQLite, so no separate database server is required.

- Make sure the database file is created automatically when the app runs, or
- If the project includes SQL setup logic, run the app once to initialize the tables

### 5. Configure the project
Before running, check the Python files for settings such as:
- database file path
- debug mode
- host and port

### 6. Run the project
```bash
python app.py
```

### 7. Open in browser
After the server starts, open:
```bash
http://127.0.0.1:5000
```

## Usage
1. Open the application in your browser
2. Use the menu or dashboard to move between sections
3. Add, edit, search, or delete records as needed
4. Save changes and review feedback messages shown in the app

## Troubleshooting
- **Flask not installed**: run `pip install flask`
- **Python not recognized**: verify Python is installed and added to PATH
- **Port already in use**: stop the other app using port 5000 or change the port
- **App not loading**: confirm `python app.py` is running without errors
