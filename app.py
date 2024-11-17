from flask import Flask, render_template, request
from attendance import mark_attendance, get_attendance_report

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/mark-attendance', methods=['POST'])
def mark_attendance_route():
    student_id = request.form['student_id']
    status = request.form['status']
    mark_attendance(student_id, status)
    return render_template('attendance_form.html', message="Attendance marked!")

@app.route('/attendance-report')
def attendance_report():
    report = get_attendance_report()
    return render_template('student_list.html', report=report)

if __name__ == "__main__":
    app.run(debug=True)
