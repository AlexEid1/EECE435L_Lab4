from Lab2_Part1 import Student, Instructor, Course, save_data_to_json, load_data_from_json, is_valid_email, is_valid_age
from Lab2_Part1 import students, instructors, courses
import tkinter as tk
from tkinter import ttk, messagebox
                                                #Part 2: GUI Development with Tkinter
                                   
#Step 1: Create a Tkinter Window
def main_menu():
    window = tk.Tk()
    window.title("Main Menu")
    window.geometry("500x400")

    add_student_button = tk.Button(window, text="Add Student", command=add_student_form)
    add_student_button.pack(pady=10)

    add_instructor_button = tk.Button(window, text="Add Instructor", command=add_instructor_form)
    add_instructor_button.pack(pady=10)

    add_course_button = tk.Button(window, text="Add Course", command=add_course_form)
    add_course_button.pack(pady=10)

    register_student_button = tk.Button(window, text="Student Registration", command=student_registration)
    register_student_button.pack(pady=10)

    assign_instructor_button = tk.Button(window, text="Instructor Assignment", command=instructor_assignment)
    assign_instructor_button.pack(pady=10)
    
    display_button = tk.Button(window, text="Display Records", command=lambda: display_records(window))
    display_button.pack(pady=10)
    
#Step 3: Implement Advanced Features
    load_button = tk.Button(window, text="Load Data", command=load_data)
    load_button.pack(side=tk.RIGHT, padx=5)

    save_button = tk.Button(window, text="Save Data", command=lambda: save_data_to_json())
    save_button.pack(side=tk.RIGHT, padx=5)

    window.mainloop()

def load_data():
    global students, instructors, courses
    result = load_data_from_json()
    if result[0]:
        students = result[1]
        instructors = result[2]
        courses = result[3]

#Step 2: Add GUI Components
def add_student_form():
    student_window = tk.Toplevel()
    student_window.title("Add Student")
    student_window.geometry("500x400")

    tk.Label(student_window, text="Name:").pack(pady=5)
    name_entry = tk.Entry(student_window)
    name_entry.pack(pady=5)

    tk.Label(student_window, text="Age:").pack(pady=5)
    age_entry = tk.Entry(student_window)
    age_entry.pack(pady=5)

    tk.Label(student_window, text="Email:").pack(pady=5)
    email_entry = tk.Entry(student_window)
    email_entry.pack(pady=5)

    tk.Label(student_window, text="Student ID:").pack(pady=5)
    student_id_entry = tk.Entry(student_window)
    student_id_entry.pack(pady=5)

    submit_button = tk.Button(student_window, text="Submit", command=lambda: (add_student(name_entry.get(), int(age_entry.get()), email_entry.get(), student_id_entry.get()), student_window.destroy()) )
    submit_button.pack(pady=20)

    back_button = tk.Button(student_window, text="Back", command=student_window.destroy)
    back_button.pack(pady=10)

def add_instructor_form():
    instructor_window = tk.Toplevel()
    instructor_window.title("Add Instructor")
    instructor_window.geometry("500x400")

    tk.Label(instructor_window, text="Name:").pack(pady=5)
    name_entry = tk.Entry(instructor_window)
    name_entry.pack(pady=5)

    tk.Label(instructor_window, text="Age:").pack(pady=5)
    age_entry = tk.Entry(instructor_window)
    age_entry.pack(pady=5)

    tk.Label(instructor_window, text="Email:").pack(pady=5)
    email_entry = tk.Entry(instructor_window)
    email_entry.pack(pady=5)

    tk.Label(instructor_window, text="Instructor ID:").pack(pady=5)
    instructor_id_entry = tk.Entry(instructor_window)
    instructor_id_entry.pack(pady=5)

    submit_button = tk.Button(instructor_window, text="Submit", command=lambda: (add_instructor(name_entry.get(), int(age_entry.get()), email_entry.get(), instructor_id_entry.get()),instructor_window.destroy()))
    submit_button.pack(pady=20)

    back_button = tk.Button(instructor_window, text="Back", command=instructor_window.destroy)
    back_button.pack(pady=10)

def add_course_form():
    course_window = tk.Toplevel()
    course_window.title("Add Course")
    course_window.geometry("500x400")

    tk.Label(course_window, text="Course ID:").pack(pady=5)
    course_id_entry = tk.Entry(course_window)
    course_id_entry.pack(pady=5)

    tk.Label(course_window, text="Course Name:").pack(pady=5)
    course_name_entry = tk.Entry(course_window)
    course_name_entry.pack(pady=5)

    tk.Label(course_window, text="Instructor:").pack(pady=5)
    instructor_combobox = ttk.Combobox(course_window, values=[f"{i.instructor_id} - {i.name}" for i in instructors])
    instructor_combobox.pack(pady=5)

    submit_button = tk.Button(course_window, text="Submit", command=lambda: (add_course(course_id_entry.get(), course_name_entry.get(), instructors[instructor_combobox.current()]), course_window.destroy()))
    submit_button.pack(pady=20)

    back_button = tk.Button(course_window, text="Back", command=course_window.destroy)
    back_button.pack(pady=10)
    
def student_registration():
    registration_window = tk.Toplevel()
    registration_window.title("Student Registration")
    registration_window.geometry("400x400")

    tk.Label(registration_window, text="Select Student:").pack(pady=5)
    student_combobox = ttk.Combobox(registration_window, values=[f"{s.student_id} - {s.name}" for s in students])
    student_combobox.pack(pady=5)

    tk.Label(registration_window, text="Select Course:").pack(pady=5)
    course_combobox = ttk.Combobox(registration_window, values=[f"{c.course_id} - {c.course_name}" for c in courses])
    course_combobox.pack(pady=5)

    def register_student_for_course():
        student_index = student_combobox.current()
        course_index = course_combobox.current()

        if student_index == -1 or course_index == -1:
            messagebox.showerror("Error", "Please select both a student and a course.")
            return

        student = students[student_index]
        course = courses[course_index]

        student.register_course(course)
        course.add_student(student)

        messagebox.showinfo("Success", f"{student.name} has been registered for {course.course_name}.")

    submit_button = tk.Button(registration_window, text="Register", command=lambda: (register_student_for_course(), registration_window.destroy()))
    submit_button.pack(pady=20)

    back_button = tk.Button(registration_window, text="Back", command=registration_window.destroy)
    back_button.pack(pady=10)

def instructor_assignment():
    assignment_window = tk.Toplevel()
    assignment_window.title("Instructor Assignment")
    assignment_window.geometry("400x400")

    tk.Label(assignment_window, text="Select Instructor:").pack(pady=5)
    instructor_combobox = ttk.Combobox(assignment_window, values=[f"{i.instructor_id} - {i.name}" for i in instructors])
    instructor_combobox.pack(pady=5)

    tk.Label(assignment_window, text="Select Course:").pack(pady=5)
    course_combobox = ttk.Combobox(assignment_window, values=[f"{c.course_id} - {c.course_name}" for c in courses])
    course_combobox.pack(pady=5)

    def assign_instructor_to_course():
        instructor_index = instructor_combobox.current()
        course_index = course_combobox.current()

        if instructor_index == -1 or course_index == -1:
            messagebox.showerror("Error", "Please select both an instructor and a course.")
            return

        instructor = instructors[instructor_index]
        course = courses[course_index]

        instructor.assign_course(course)
        messagebox.showinfo("Success", f"{instructor.name} has been assigned to {course.course_name}.")

    submit_button = tk.Button(assignment_window, text="Assign", command= lambda: (assign_instructor_to_course(), assignment_window.destroy()))
    submit_button.pack(pady=20)

    back_button = tk.Button(assignment_window, text="Back", command=assignment_window.destroy)
    back_button.pack(pady=10)

def display_records(window):
    window.destroy()
    records_window = tk.Tk()
    records_window.title("Display Records")
    records_window.geometry("800x600")

    search_frame = tk.Frame(records_window)
    search_frame.pack(pady=10, fill=tk.X)

    search_label = tk.Label(search_frame, text="Search:")
    search_label.pack(side=tk.LEFT, padx=5)
    search_entry = tk.Entry(search_frame)
    search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

    button_frame = tk.Frame(records_window)
    button_frame.pack(pady=10, fill=tk.X)

    selected_type = tk.StringVar(value="All")

    def filter_records(record_type):
        selected_type.set(record_type)
        refresh_tree()

    student_button = tk.Radiobutton(button_frame, text="Student", variable=selected_type, value="Student", command=lambda: filter_records("Student"))
    student_button.pack(side=tk.LEFT, padx=5)
    
    instructor_button = tk.Radiobutton(button_frame, text="Instructor", variable=selected_type, value="Instructor", command=lambda: filter_records("Instructor"))
    instructor_button.pack(side=tk.LEFT, padx=5)
    
    course_button = tk.Radiobutton(button_frame, text="Course", variable=selected_type, value="Course", command=lambda: filter_records("Course"))
    course_button.pack(side=tk.LEFT, padx=5)
    
    course_button = tk.Radiobutton(button_frame, text="All", variable=selected_type, value="All", command=lambda: filter_records("All"))
    course_button.pack(side=tk.LEFT, padx=5)

    tree = ttk.Treeview(records_window, columns=("Type", "ID", "Name", "Details"), show="headings")
    tree.heading("Type", text="Type")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Details", text="Details")
    tree.pack(fill=tk.BOTH, expand=True)

    def refresh_tree():
        query = search_entry.get().lower()
        tree.delete(*tree.get_children())

        if selected_type.get() == "Student":
            for student in students:
                if query in student.name.lower() or query in student.student_id.lower():
                    tree.insert('', 'end', values=("Student", student.student_id, student.name, f"Age: {student.age}, Email: {student._email}, Registered Courses: {', '.join([c.course_name for c in student.registered_courses])}"))

        elif selected_type.get() == "Instructor":
            for instructor in instructors:
                if query in instructor.name.lower() or query in instructor.instructor_id.lower():
                    tree.insert('', 'end', values=("Instructor", instructor.instructor_id, instructor.name, f"Age: {instructor.age}, Email: {instructor._email}, Assigned Courses: {', '.join([c.course_name for c in instructor.assigned_courses])}"))

        elif selected_type.get() == "Course":
            for course in courses:
                if query in course.course_name.lower() or query in course.course_id.lower():
                    tree.insert('', 'end', values=("Course", course.course_id, course.course_name, f"Instructor: {course.instructor.name}, Enrolled Students: {', '.join([s.name for s in course.enrolled_students])}"))

        else:
            for student in students:
                if query in student.name.lower() or query in student.student_id.lower():
                    tree.insert('', 'end', values=("Student", student.student_id, student.name, f"Age: {student.age}, Email: {student._email}, Registered Courses: {', '.join([c.course_name for c in student.registered_courses])}"))
            for instructor in instructors:
                if query in instructor.name.lower() or query in instructor.instructor_id.lower():
                    tree.insert('', 'end', values=("Instructor", instructor.instructor_id, instructor.name, f"Age: {instructor.age}, Email: {instructor._email}, Assigned Courses: {', '.join([c.course_name for c in instructor.assigned_courses])}"))
            for course in courses:
                if query in course.course_name.lower() or query in course.course_id.lower():
                    tree.insert('', 'end', values=("Course", course.course_id, course.course_name, f"Instructor: {course.instructor.name}, Enrolled Students: {', '.join([s.name for s in course.enrolled_students])}"))

    refresh_tree()

    search_entry.bind('<KeyRelease>', lambda event: refresh_tree())

    control_frame = tk.Frame(records_window)
    control_frame.pack(pady=10, fill=tk.X)

    back_button = tk.Button(control_frame, text="Back", command=lambda: (records_window.destroy(), main_menu()))
    back_button.pack(side=tk.LEFT, padx=5)

#Step 3: Implement Advanced Features
    edit_button = tk.Button(control_frame, text="Edit Selected", command=lambda: edit_record(tree))
    edit_button.pack(side=tk.LEFT, padx=5)

    delete_button = tk.Button(control_frame, text="Delete Selected", command=lambda: delete_record(tree))
    delete_button.pack(side=tk.LEFT, padx=5)
    
    records_window.mainloop()

def add_student(name, age, email, student_id):
    if not is_valid_email(email):
        messagebox.showerror("Invalid Email", "Please provide a valid email.")
        return
    if not is_valid_age(age):
        messagebox.showerror("Invalid Age", "Age must be a non-negative integer.")
        return
    student = Student(name, int(age), email, student_id)
    students.append(student)
    messagebox.showinfo("Success", "Student added successfully!")

def add_instructor(name, age, email, instructor_id):
    if not is_valid_email(email):
        messagebox.showerror("Invalid Email", "Please provide a valid email.")
        return
    if not is_valid_age(age):
        messagebox.showerror("Invalid Age", "Age must be a non-negative integer.")
        return
    instructor = Instructor(name, int(age), email, instructor_id)
    instructors.append(instructor)
    messagebox.showinfo("Success", "Instructor added successfully!")

def add_course(course_id, course_name, instructor):
    course = Course(course_id, course_name, instructor)
    courses.append(course)
    instructor.assign_course(course)
    messagebox.showinfo("Success", "Course added successfully!")

#Step 3: Implement Advanced Features
def delete_record(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a record to delete.")
        return

    item_values = tree.item(selected_item, 'values')
    record_type, record_id, name, details = item_values

    if record_type == "Student":
        global students
        students = [s for s in students if s.student_id != record_id]
        messagebox.showinfo("Success", f"Student {name} deleted successfully.")

    elif record_type == "Instructor":
        global instructors
        instructors = [i for i in instructors if i.instructor_id != record_id]
        messagebox.showinfo("Success", f"Instructor {name} deleted successfully.")

    elif record_type == "Course":
        global courses
        courses = [c for c in courses if c.course_id != record_id]
        messagebox.showinfo("Success", f"Course {name} deleted successfully.")

    tree.delete(selected_item)

def edit_record(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a record to edit.")
        return
    
    item_values = tree.item(selected_item, 'values')
    record_type, record_id, name, details = item_values

    if record_type == "Student":
        student = next((s for s in students if s.student_id == record_id), None)
        if student:
            edit_student_form(student)

    elif record_type == "Instructor":
        instructor = next((i for i in instructors if i.instructor_id == record_id), None)
        if instructor:
            edit_instructor_form(instructor)

    elif record_type == "Course":
        course = next((c for c in courses if c.course_id == record_id), None)
        if course:
            edit_course_form(course)

def edit_student_form(student):
    student_window = tk.Toplevel()
    student_window.title("Edit Student")
    student_window.geometry("500x400")

    tk.Label(student_window, text="Name:").pack(pady=5)
    name_entry = tk.Entry(student_window)
    name_entry.insert(0, student.name)
    name_entry.pack(pady=5)

    tk.Label(student_window, text="Age:").pack(pady=5)
    age_entry = tk.Entry(student_window)
    age_entry.insert(0, str(student.age))
    age_entry.pack(pady=5)

    tk.Label(student_window, text="Email:").pack(pady=5)
    email_entry = tk.Entry(student_window)
    email_entry.insert(0, student._email)
    email_entry.pack(pady=5)

    submit_button = tk.Button(student_window, text="Submit", command=lambda: (update_student(student, name_entry.get(), int(age_entry.get()), email_entry.get()), student_window.destroy()))
    submit_button.pack(pady=20)

    back_button = tk.Button(student_window, text="Back", command=student_window.destroy)
    back_button.pack(pady=10)

def edit_instructor_form(instructor):
    instructor_window = tk.Toplevel()
    instructor_window.title("Edit Instructor")
    instructor_window.geometry("500x400")

    tk.Label(instructor_window, text="Name:").pack(pady=5)
    name_entry = tk.Entry(instructor_window)
    name_entry.insert(0, instructor.name)
    name_entry.pack(pady=5)

    tk.Label(instructor_window, text="Age:").pack(pady=5)
    age_entry = tk.Entry(instructor_window)
    age_entry.insert(0, str(instructor.age))
    age_entry.pack(pady=5)

    tk.Label(instructor_window, text="Email:").pack(pady=5)
    email_entry = tk.Entry(instructor_window)
    email_entry.insert(0, instructor._email)
    email_entry.pack(pady=5)

    submit_button = tk.Button(instructor_window, text="Submit", command=lambda: (update_instructor(instructor, name_entry.get(), int(age_entry.get()), email_entry.get()), instructor_window.destroy()))
    submit_button.pack(pady=20)

    back_button = tk.Button(instructor_window, text="Back", command=instructor_window.destroy)
    back_button.pack(pady=10)

def edit_course_form(course):
    course_window = tk.Toplevel()
    course_window.title("Edit Course")
    course_window.geometry("500x400")

    tk.Label(course_window, text="Course Name:").pack(pady=5)
    course_name_entry = tk.Entry(course_window)
    course_name_entry.insert(0, course.course_name)
    course_name_entry.pack(pady=5)

    tk.Label(course_window, text="Instructor:").pack(pady=5)
    instructor_combobox = ttk.Combobox(course_window, values=[f"{i.instructor_id} - {i.name}" for i in instructors])
    instructor_combobox.set(f"{course.instructor.instructor_id} - {course.instructor.name}")
    instructor_combobox.pack(pady=5)

    submit_button = tk.Button(course_window, text="Submit", command=lambda: (update_course(course, course_name_entry.get(), instructors[instructor_combobox.current()]), course_window.destroy()))
    submit_button.pack(pady=20)

    back_button = tk.Button(course_window, text="Back", command=course_window.destroy)
    back_button.pack(pady=10)

def update_student(student, name, age, email):
    student.name = name
    student.age = age
    student._email = email
    messagebox.showinfo("Success", "Student updated successfully!")

def update_instructor(instructor, name, age, email):
    instructor.name = name
    instructor.age = age
    instructor._email = email
    messagebox.showinfo("Success", "Instructor updated successfully!")

def update_course(course, course_name, instructor):
    course.course_name = course_name
    course.instructor = instructor
    messagebox.showinfo("Success", "Course updated successfully!")

if __name__ == "__main__":
    main_menu()