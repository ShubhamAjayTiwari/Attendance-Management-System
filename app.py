from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from functools import wraps

app = Flask(__name__)
app.secret_key = 'attendance_system_secret_key_2026'

# ─── Database Configuration ─────────────────────────────────────────────────────
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password@12',
    'database': 'attendance_db'
}


def get_db():
    """Create and return a database connection."""
    return mysql.connector.connect(**db_config)


# ─── Auth Decorator ──────────────────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'staff_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


# ─── Routes ──────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    if 'staff_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'staff_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash('Please enter both username and password.', 'error')
            return render_template('login.html')

        try:
            conn = get_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM staff WHERE username = %s AND password = %s",
                (username, password)
            )
            staff = cursor.fetchone()
            cursor.close()
            conn.close()

            if staff:
                session['staff_id'] = staff['staff_id']
                session['staff_name'] = staff['name']
                session['staff_subject'] = staff['subject']
                flash(f'Welcome back, {staff["name"]}!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password.', 'error')
        except mysql.connector.Error as e:
            flash(f'Database error: {str(e)}', 'error')

    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template(
        'dashboard.html',
        staff_name=session.get('staff_name'),
        staff_subject=session.get('staff_subject')
    )


@app.route('/mark_attendance', methods=['GET', 'POST'])
@login_required
def mark_attendance():
    if request.method == 'POST':
        staff_id = session['staff_id']
        date = request.form.get('date')

        if not date:
            flash('Please select a date.', 'error')
            return redirect(url_for('mark_attendance'))

        try:
            conn = get_db()
            cursor = conn.cursor()

            # Get all student IDs to iterate
            cursor.execute("SELECT student_id FROM students ORDER BY name")
            students = cursor.fetchall()

            records_inserted = 0
            for (student_id,) in students:
                status = request.form.get(f'status_{student_id}')
                if status:
                    # Check if attendance already exists for this student/staff/date
                    cursor.execute(
                        "SELECT attendance_id FROM attendance "
                        "WHERE student_id = %s AND staff_id = %s AND date = %s",
                        (student_id, staff_id, date)
                    )
                    existing = cursor.fetchone()

                    if existing:
                        cursor.execute(
                            "UPDATE attendance SET status = %s "
                            "WHERE student_id = %s AND staff_id = %s AND date = %s",
                            (status, student_id, staff_id, date)
                        )
                    else:
                        cursor.execute(
                            "INSERT INTO attendance (student_id, staff_id, date, status) "
                            "VALUES (%s, %s, %s, %s)",
                            (student_id, staff_id, date, status)
                        )
                    records_inserted += 1

            conn.commit()
            cursor.close()
            conn.close()

            flash(f'Attendance marked successfully for {records_inserted} students.', 'success')
            return redirect(url_for('dashboard'))

        except mysql.connector.Error as e:
            flash(f'Database error: {str(e)}', 'error')

    # GET — fetch all students
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students ORDER BY name")
        students = cursor.fetchall()
        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        flash(f'Database error: {str(e)}', 'error')
        students = []

    return render_template('mark_attendance.html', students=students)


@app.route('/report')
@login_required
def report():
    staff_id = session['staff_id']

    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        # Get all students with their attendance stats for the logged-in staff
        cursor.execute("""
            SELECT
                s.student_id,
                s.name,
                s.register_no,
                s.department,
                s.year,
                COUNT(a.attendance_id) AS total_classes,
                SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) AS present_count
            FROM students s
            LEFT JOIN attendance a
                ON s.student_id = a.student_id AND a.staff_id = %s
            GROUP BY s.student_id, s.name, s.register_no, s.department, s.year
            ORDER BY s.name
        """, (staff_id,))

        students = cursor.fetchall()

        # Calculate percentage for each student
        for student in students:
            total = student['total_classes']
            present = student['present_count'] or 0
            student['present_count'] = present
            student['percentage'] = round((present / total) * 100, 1) if total > 0 else 0.0

        cursor.close()
        conn.close()

    except mysql.connector.Error as e:
        flash(f'Database error: {str(e)}', 'error')
        students = []

    return render_template('report.html', students=students)


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# ─── Run ─────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)
