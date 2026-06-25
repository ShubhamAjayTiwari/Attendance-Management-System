# Attendance Management System

A web-based **Attendance Management System** built with **Python Flask** and **MySQL**. This application was designed for a Database Management System (DBMS) course project, allowing staff to log in, manage/mark daily attendance for students, and generate attendance reports with percentage calculations.

---

## 🚀 Features

- **Staff Authentication:** Secure login for faculty/staff members.
- **Interactive Dashboard:** Simple and clean user interface to navigate actions.
- **Mark Attendance:** Dynamic form to record student status (Present, Absent, Medical Leave, On Duty) for any specific date.
- **Real-Time Reports:** View cumulative attendance percentage and visual alerts for students falling below the 75% attendance threshold.
- **Responsive Design:** Clean styling optimized for modern web browsers.

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Database:** MySQL (using `mysql-connector-python`)
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)

---

## 📂 Project Structure

```text
attendance_system/
│
├── app.py              # Main Flask application and database routing
├── static/
│   ├── style.css       # Premium custom stylesheet
│   └── theme.js        # Theme and layout logic
│
├── templates/
│   ├── dashboard.html  # Staff dashboard page
│   ├── login.html      # Authentication portal
│   ├── mark_attendance.html # Daily attendance grid
│   └── report.html     # Analytics and attendance reports
│
└── .gitignore          # Git exclusion rules
```

---

## 💾 Database Setup

The application connects to a MySQL database using the credentials defined in `app.py`.

### Schema Configuration

Ensure MySQL is running locally and create the database and tables:

```sql
CREATE DATABASE attendance_db;
USE attendance_db;

-- 1. Staff Table
CREATE TABLE staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    subject VARCHAR(100) NOT NULL
);

-- 2. Students Table
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    register_no VARCHAR(50) NOT NULL UNIQUE,
    department VARCHAR(50) NOT NULL,
    year INT NOT NULL
);

-- 3. Attendance Table
CREATE TABLE attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    staff_id INT NOT NULL,
    date DATE NOT NULL,
    status VARCHAR(20) NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id) ON DELETE CASCADE
);
```

### Sample Data

```sql
-- Insert Staff Accounts
INSERT INTO staff (name, username, password, subject) VALUES 
('Dr. Raju', 'raju', 'raju123', 'DBMS'),
('Dr. Sathya', 'sathya', 'sathya123', 'Digital Image Processing');

-- Insert Students
INSERT INTO students (name, register_no, department, year) VALUES 
('Harish Kumar', 'RA2411026020148', 'CSE', 2),
('Shubham Tiwari', 'RA2411026020153', 'CSE', 2),
('Udit Kumar Nayak', 'RA2411026020125', 'CSE', 2),
('Jude Bellingham', 'RA2411026020000', 'CSE', 2),
('Kylian Mbappe', 'RA2411026020001', 'CSE', 2);
```

---

## ⚙️ Installation & Running Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ShubhamAjayTiwari/Attendance-Management-System.git
   cd Attendance-Management-System
   ```

2. **Install Dependencies:**
   ```bash
   pip install Flask mysql-connector-python
   ```

3. **Set up MySQL Database:**
   Import the schema details above in your local MySQL instance. If you need to adjust database login details, modify `db_config` in `app.py`:
   ```python
   db_config = {
       'host': 'localhost',
       'user': 'root',
       'password': 'YOUR_PASSWORD',
       'database': 'attendance_db'
   }
   ```

4. **Run the Application:**
   ```bash
   python app.py
   ```
   Open your browser and navigate to `http://127.0.0.1:5000/`.
