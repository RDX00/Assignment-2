import json


class Person:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def display_person_info(self):
        print(f"Name: {self.name}\nAge: {self.age}\nAddress: {self.address}")


class Student(Person):
    def __init__(self, name, age, address, student_id):
        super().__init__(name, age, address)
        self.student_id = student_id
        self.grades = {}
        self.courses = []

    def add_grade(self, course_code, grade):
        self.grades[course_code] = grade

    def enroll_course(self, course):
        self.courses.append(course)
    
    def display_student_info(self):
        print(f"Student Information:\nName: {self.name}\nID: {self.student_id}\n"
              f"Age: {self.age}\nAddress: {self.address}\n"
              f"Enrolled Courses: {', '.join(self.courses)}\nGrades: {self.grades}")


class Course:
    def __init__(self, course_name, course_code, instructor):
        self.course_name = course_name
        self.course_code = course_code
        self.instructor = instructor
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def display_course_info(self):
        student_names = ', '.join(student.name for student in self.students)
        print(f"Course Information:\nCourse Name: {self.course_name}\n"
              f"Code: {self.course_code}\nInstructor: {self.instructor}\n"
              f"Enrolled Students: {student_names if student_names else 'None'}")



class StudentManagementSystem:
    def __init__(self):
        self.students = {}
        self.courses = {}

    def add_student(self):
        name = input("Enter Name: ")
        age = int(input("Enter Age: "))
        address = input("Enter Address: ")
        student_id = input("Enter Student ID: ")
        
        student = Student(name, age, address, student_id)
        self.students[student_id] = student
        print(f"Student {name} (ID: {student_id}) added successfully.")

    def add_course(self):
        course_name = input("Enter Course Name: ")
        course_code = input("Enter Course Code: ")
        instructor = input("Enter Instructor Name: ")

        course = Course(course_name, course_code, instructor)
        self.courses[course_code] = course
        print(f"Course {course_name} (Code: {course_code}) created with instructor {instructor}.")

    def enroll_student_in_course(self):
        student_id = input("Enter Student ID: ")
        course_code = input("Enter Course Code: ")
        
        if student_id in self.students and course_code in self.courses:
            student = self.students[student_id]
            course = self.courses[course_code]
            student.enroll_course(course_code)
            course.add_student(student)
            print(f"Student {student.name} (ID: {student_id}) enrolled in {course.course_name} (Code: {course_code}).")
        else:
            print("Error: Student ID or Course Code does not exist.")

    def add_grade(self):
        student_id = input("Enter Student ID: ")
        course_code = input("Enter Course Code: ")
        grade = input("Enter Grade: ")

        if student_id in self.students and course_code in self.courses:
            student = self.students[student_id]
            if course_code in student.courses:
                student.add_grade(course_code, grade)
                print(f"Grade {grade} added for {student.name} in {course_code}.")
            else:
                print("Error: Student is not enrolled in this course.")
        else:
            print("Error: Student ID or Course Code does not exist.")

    def display_student_details(self):
        student_id = input("Enter Student ID: ")
        if student_id in self.students:
            self.students[student_id].display_student_info()
        else:
            print("Error: Student ID does not exist.")

    def display_course_details(self):
        course_code = input("Enter Course Code: ")
        if course_code in self.courses:
            self.courses[course_code].display_course_info()
        else:
            print("Error: Course Code does not exist.")

    def save_data(self):
        data = {
            "students": {student_id: {
                "name": student.name,
                "age": student.age,
                "address": student.address,
                "grades": student.grades,
                "courses": student.courses
            } for student_id, student in self.students.items()},
            "courses": {course_code: {
                "course_name": course.course_name,
                "instructor": course.instructor,
                "students": [student.student_id for student in course.students]
            } for course_code, course in self.courses.items()}
        }
        with open('data.json', 'w') as f:
            json.dump(data, f)
        print("All student and course data saved successfully.")

    def load_data(self):
        try:
            with open('data.json', 'r') as f:
                data = json.load(f)
                for student_id, student_data in data['students'].items():
                    student = Student(student_data["name"], student_data["age"], student_data["address"], student_id)
                    student.grades = student_data["grades"]
                    student.courses = student_data["courses"]
                    self.students[student_id] = student
                
                for course_code, course_data in data['courses'].items():
                    course = Course(course_data["course_name"], course_code, course_data["instructor"])
                    for student_id in course_data["students"]:
                        if student_id in self.students:
                            course.add_student(self.students[student_id])
                    self.courses[course_code] = course
            print("Data loaded successfully.")
        except FileNotFoundError:
            print("No data file found. Starting with an empty system.")


def main():
    system = StudentManagementSystem()
    system.load_data()  

    while True:
        print("\n==== Student Management System ====")
        print("1. Add New Student")
        print("2. Add New Course")
        print("3. Enroll Student in Course")
        print("4. Add Grade for Student")
        print("5. Display Student Details")
        print("6. Display Course Details")
        print("7. Save Data to File")
        print("8. Load Data from File")
        print("0. Exit")
        
        option = input("Select Option: ")

        if option == "1":
            system.add_student()
        elif option == "2":
            system.add_course()
        elif option == "3":
            system.enroll_student_in_course()
        elif option == "4":
            system.add_grade()
        elif option == "5":
            system.display_student_details()
        elif option == "6":
            system.display_course_details()
        elif option == "7":
            system.save_data()
        elif option == "8":
            system.load_data()
        elif option == "0":
            print("Exiting Student Management System. Goodbye!")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
