import sys
import csv
import json
#this file contains the pyqt5 gui by alexander menassa
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTabWidget, QTableWidget, QTableWidgetItem,
                             QFileDialog, QMessageBox, QComboBox, QInputDialog)
from db import create_tables, add_student, add_instructor, add_course, register_student, get_students, get_instructors, get_courses

class FormTab(QWidget):
    def __init__(self, button_text, action):
        super().__init__()
        self.action = action

        # Main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Form layout
        self.form_layout = QVBoxLayout()
        self.layout.addLayout(self.form_layout)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter Name")
        self.name_input.setFixedSize(300, 30)
        self.form_layout.addWidget(self.name_input)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter ID")
        self.id_input.setFixedSize(300, 30)
        self.form_layout.addWidget(self.id_input)

        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Enter Age")
        self.age_input.setFixedSize(300, 30)
        self.form_layout.addWidget(self.age_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter Email")
        self.email_input.setFixedSize(300, 30)
        self.form_layout.addWidget(self.email_input)

        self.submit_button = QPushButton(button_text)
        self.submit_button.setFixedSize(150, 40)
        self.form_layout.addWidget(self.submit_button)
        self.submit_button.clicked.connect(self.action)

class RecordsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by ID, Name, Email, or Course")
        self.search_input.setFixedSize(300, 30)
        self.layout.addWidget(self.search_input)

        self.table = QTableWidget()
        self.table.setRowCount(0)
        self.table.setColumnCount(7)  # Increased column count for Edit and Delete buttons
        self.table.setHorizontalHeaderLabels(["Name", "ID", "Age", "Email", "Course", "Edit", "Delete"])
        self.layout.addWidget(self.table)

        self.records = []
        self.search_input.textChanged.connect(self.search_records)

    def add_record(self, name, id_, age, email, course):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(name))
        self.table.setItem(row_position, 1, QTableWidgetItem(id_))
        self.table.setItem(row_position, 2, QTableWidgetItem(str(age)))
        self.table.setItem(row_position, 3, QTableWidgetItem(email))
        self.table.setItem(row_position, 4, QTableWidgetItem(course))

        # Add Edit and Delete buttons
        edit_button = QPushButton("Edit")
        delete_button = QPushButton("Delete")
        edit_button.clicked.connect(lambda: self.edit_record(row_position))
        delete_button.clicked.connect(lambda: self.delete_record(row_position))
        self.table.setCellWidget(row_position, 5, edit_button)
        self.table.setCellWidget(row_position, 6, delete_button)

        self.records.append({'name': name, 'id': id_, 'age': age, 'email': email, 'course': course})

    def search_records(self, search_term):
        search_term = search_term.lower()
        for row in range(self.table.rowCount()):
            name = self.table.item(row, 0).text().lower()
            id_ = self.table.item(row, 1).text().lower()
            email = self.table.item(row, 3).text().lower()
            course = self.table.item(row, 4).text().lower()
            if search_term in id_ or search_term in name or search_term in email or search_term in course:
                self.table.showRow(row)
            else:
                self.table.hideRow(row)

    def edit_record(self, row):
        # Get the current values
        name = self.table.item(row, 0).text()
        id_ = self.table.item(row, 1).text()
        age = self.table.item(row, 2).text()
        email = self.table.item(row, 3).text()
        course = self.table.item(row, 4).text()

        # Prompt the user to edit the values
        new_name, ok_name = QInputDialog.getText(self, "Edit Name", "Name:", QLineEdit.Normal, name)
        new_age, ok_age = QInputDialog.getInt(self, "Edit Age", "Age:", int(age))
        new_email, ok_email = QInputDialog.getText(self, "Edit Email", "Email:", QLineEdit.Normal, email)

        if ok_name and ok_age and ok_email:
            # Update the table with the new values
            self.table.setItem(row, 0, QTableWidgetItem(new_name))
            self.table.setItem(row, 2, QTableWidgetItem(str(new_age)))
            self.table.setItem(row, 3, QTableWidgetItem(new_email))

            # Update the record in the records list
            self.records[row]['name'] = new_name
            self.records[row]['age'] = new_age
            self.records[row]['email'] = new_email

    def delete_record(self, row):
        # Remove the row from the table
        self.table.removeRow(row)

        # Remove the record from the records list
        del self.records[row]

    def export_to_csv(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Export CSV", "", "CSV Files (*.csv)")
        if file_name:
            with open(file_name, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "ID", "Age", "Email", "Course"])
                for record in self.records:
                    writer.writerow([record['name'], record['id'], record['age'], record['email'], record['course']])
            QMessageBox.information(self, "Export Successful", f"Records exported to {file_name} successfully!")

class CourseTab(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Form layout
        self.form_layout = QVBoxLayout()
        self.layout.addLayout(self.form_layout)

        # Course ID input
        self.course_id_input = QLineEdit()
        self.course_id_input.setPlaceholderText("Enter Course ID")
        self.course_id_input.setFixedSize(300, 30)
        self.form_layout.addWidget(self.course_id_input)

        # Course name input
        self.course_name_input = QLineEdit()
        self.course_name_input.setPlaceholderText("Enter Course Name")
        self.course_name_input.setFixedSize(300, 30)
        self.form_layout.addWidget(self.course_name_input)

        # Instructor dropdown
        self.instructor_dropdown = QComboBox()
        self.instructor_dropdown.setFixedSize(300, 30)
        self.form_layout.addWidget(self.instructor_dropdown)

        # Submit button
        self.submit_button = QPushButton("Add Course")
        self.submit_button.setFixedSize(150, 40)
        self.form_layout.addWidget(self.submit_button)

    def set_instructors(self, instructors):
        self.instructor_dropdown.clear()
        self.instructor_dropdown.addItems(instructors)


class RegistrationTab(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Student dropdown
        self.student_dropdown = QComboBox()
        self.student_dropdown.setFixedSize(300, 30)
        self.layout.addWidget(self.student_dropdown)

        # Course dropdown
        self.course_dropdown = QComboBox()
        self.course_dropdown.setFixedSize(300, 30)
        self.layout.addWidget(self.course_dropdown)

        # Register button
        self.register_button = QPushButton("Register")
        self.register_button.setFixedSize(150, 40)
        self.layout.addWidget(self.register_button)

    def set_students(self, students):
        self.student_dropdown.clear()
        self.student_dropdown.addItems(students)

    def set_courses(self, courses):
        self.course_dropdown.clear()
        self.course_dropdown.addItems(courses)


class AssignInstructorTab(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Instructor dropdown
        self.instructor_dropdown = QComboBox()
        self.instructor_dropdown.setFixedSize(300, 30)
        self.layout.addWidget(self.instructor_dropdown)

        # Course dropdown
        self.course_dropdown = QComboBox()
        self.course_dropdown.setFixedSize(300, 30)
        self.layout.addWidget(self.course_dropdown)

        # Assign button
        self.assign_button = QPushButton("Assign Instructor")
        self.assign_button.setFixedSize(150, 40)
        self.layout.addWidget(self.assign_button)

    def set_instructors(self, instructors):
        self.instructor_dropdown.clear()
        self.instructor_dropdown.addItems(instructors)

    def set_courses(self, courses):
        self.course_dropdown.clear()
        self.course_dropdown.addItems(courses)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 800, 600)

        # Initialize database
        create_tables()

        # Main layout
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Create tabs
        self.student_tab = FormTab("Add Student", self.add_student)
        self.instructor_tab = FormTab("Add Instructor", self.add_instructor)
        self.course_tab = CourseTab()
        self.registration_tab = RegistrationTab()
        self.records_tab = RecordsTab()
        self.assign_instructor_tab = AssignInstructorTab()

        self.tab_widget.addTab(self.student_tab, "Add Student")
        self.tab_widget.addTab(self.instructor_tab, "Add Instructor")
        self.tab_widget.addTab(self.course_tab, "Manage Courses")
        self.tab_widget.addTab(self.registration_tab, "Register for Course")
        self.tab_widget.addTab(self.records_tab, "View Records")
        self.tab_widget.addTab(self.assign_instructor_tab, "Assign Instructor")

        # Connect signals
        self.student_tab.submit_button.clicked.connect(self.add_student)
        self.instructor_tab.submit_button.clicked.connect(self.add_instructor)
        self.course_tab.submit_button.clicked.connect(self.add_course)
        self.registration_tab.register_button.clicked.connect(self.register_student)
        self.assign_instructor_tab.assign_button.clicked.connect(self.assign_instructor)

        # Adding Save and Load buttons
        self.save_button = QPushButton("Save Data", self)
        self.load_button = QPushButton("Load Data", self)
        self.save_button.clicked.connect(self.save_data)
        self.load_button.clicked.connect(self.load_data)

        # Add buttons to the layout or window
        self.tab_widget.addTab(self.save_button, "Save Data")
        self.tab_widget.addTab(self.load_button, "Load Data")

        # Initialize lists
        self.populate_dropdowns()

    def populate_dropdowns(self):
        self.students = [f"{name} ({id_})" for (id_, name) in get_students()]
        self.instructors = [f"{name} ({id_})" for (id_, name) in get_instructors()]
        courses = [name for (id_, name) in get_courses()]
        
        self.registration_tab.set_students(self.students)
        self.registration_tab.set_courses(courses)
        self.course_tab.set_instructors(self.instructors)
        self.assign_instructor_tab.set_courses(courses)
        self.assign_instructor_tab.set_instructors(self.instructors)

    def add_student(self):
        name = self.student_tab.name_input.text()
        age = self.student_tab.age_input.text()
        email = self.student_tab.email_input.text()
        add_student(name, age, email)
        self.records_tab.add_record(name, "N/A", age, email, "N/A")
        self.student_tab.name_input.clear()
        self.student_tab.age_input.clear()
        self.student_tab.email_input.clear()
        self.populate_dropdowns()

    def add_instructor(self):
        name = self.instructor_tab.name_input.text()
        age = self.instructor_tab.age_input.text()
        email = self.instructor_tab.email_input.text()
        add_instructor(name, age, email)
        self.records_tab.add_record(name, "N/A", age, email, "N/A")
        self.instructor_tab.name_input.clear()
        self.instructor_tab.age_input.clear()
        self.instructor_tab.email_input.clear()
        self.populate_dropdowns()

    def add_course(self):
        course_id = self.course_tab.course_id_input.text()
        course_name = self.course_tab.course_name_input.text()
        instructor_id = self.course_tab.instructor_dropdown.currentText().split('(')[-1].strip(')')
        
        add_course(course_id, course_name, instructor_id)
        self.records_tab.add_record(course_name, course_id, "N/A", "N/A", instructor_id)
        self.course_tab.course_id_input.clear()
        self.course_tab.course_name_input.clear()
        self.populate_dropdowns()

    def register_student(self):
        student_id = self.registration_tab.student_dropdown.currentText().split('(')[-1].strip(')')
        course_id = self.registration_tab.course_dropdown.currentText()
        
        register_student(student_id, course_id)
        self.records_tab.add_record(student_id, "N/A", "N/A", "N/A", course_id)

    def assign_instructor(self):
        course_id = self.assign_instructor_tab.course_dropdown.currentText()
        instructor_id = self.assign_instructor_tab.instructor_dropdown.currentText().split('(')[-1].strip(')')
        
        add_course(course_id, "N/A", instructor_id)
        self.records_tab.add_record("N/A", course_id, "N/A", "N/A", instructor_id)

    def save_data(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Data", "", "JSON Files (*.json)")
        if file_name:
            data = {
                'students': get_students(),
                'instructors': get_instructors(),
                'courses': get_courses()
            }
            with open(file_name, 'w') as file:
                json.dump(data, file)
            QMessageBox.information(self, "Save Successful", f"Data saved to {file_name} successfully!")

    def load_data(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Data", "", "JSON Files (*.json)")
        if file_name:
            with open(file_name, 'r') as file:
                data = json.load(file)

            # Load students
            for student in data.get('students', []):
                self.records_tab.add_record(student['name'], student['id'], student['age'], student['email'], "N/A")

            # Load instructors
            for instructor in data.get('instructors', []):
                self.records_tab.add_record(instructor['name'], instructor['id'], instructor['age'], instructor['email'], "N/A")

            # Load courses
            for course in data.get('courses', []):
                self.records_tab.add_record(course['name'], course['id'], "N/A", "N/A", "Course")

            QMessageBox.information(self, "Load Successful", f"Data loaded from {file_name} successfully!")
            self.populate_dropdowns()

            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
