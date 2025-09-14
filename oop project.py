import json
import getpass
import os
from abc import ABC, abstractmethod

def get_terminal_width():
    return os.get_terminal_size().columns

def center_text(text):
    return text.center(get_terminal_width())

class User(ABC):
    def __init__(self, name, password):
        self.name = name
        self.__password = password

    @property
    def password (self):
        return self.__password
    
    @password.setter
    def password (self,new_password):
        if len(new_password) >= 4:
            self.__password = new_password
        else:
            print("Password must be at least 4 characters long.")


    @abstractmethod
    def show_menu(self, system):
        pass
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

class Student(User):
    def __init__(self, name, password):
        super().__init__(name, password)
        self.courses = []
    
    def show_menu(self, system):          
        while True:                    
            self.clear_screen()
            terminal_width = get_terminal_width()
            print("=" * terminal_width)
            print(center_text(f"STUDENT PORTAL: {self.name}"))
            print("=" * terminal_width)
            print("=" * get_terminal_width())
            print("1. View Available Courses")
            print("2. Register for Course")
            print("3. Drop Course")
            print("4. View My Profile")
            print("5. Change Password")
            print("6. Logout")
            print("=" * get_terminal_width())
            
            choice = input("\nEnter your choice (1-6): ")
            self.clear_screen()
            
            if choice == "1":
                system.display_courses()
            elif choice == "2":
                self.register_course(system)
            elif choice == "3":
                self.drop_course(system)
            elif choice == "4":
                self.view_profile()
            elif choice == "5":
                self.change_password(system)
            elif choice == "6":
                print("Logging out...")
                system.save_data()
                break
            else:
                print("Invalid choice!")
            
            input("\nPress Enter to continue...")
    
    def register_course(self, system):
       system.display_courses()
       print("\nSelect course by number:")
       try:
           choice = int(input("Enter course number: ")) - 1
           course_names = list(system.courses.keys())
           if 0 <= choice < len(course_names):
               course = course_names[choice]
           else:
               print("Invalid course number!")
               return
       except ValueError:
           print("Please enter a valid number.")
           return
       if course in self.courses:
           print("You are already registered in this course.")
           return
       if len(system.courses[course]["students"]) >= system.courses[course]["capacity"]:
           print("Course is full!")
           return
       confirm = input(f"Are you sure you want to register for '{course}'? (yes/no): ").strip().lower()
       if confirm != "yes":
           print("Registration cancelled.")
           return
       self.courses.append(course)
       system.courses[course]["students"].append(self.name)
       print(f"Successfully registered in '{course}'!")
       system.save_data()

    
    def drop_course(self, system):
       if not self.courses:
            print("You are not registered in any course.")
            return
       print("\nYour Registered Courses:")
       for i, course in enumerate(self.courses, start=1):
            print(f"{i}. {course}")
       try:
           choice = int(input("Enter course number to drop: ")) - 1
           if 0 <= choice < len(self.courses):
               course = self.courses[choice]
           else:
               print("Invalid course number!")
               return
       except ValueError:
           print("Please enter a valid number.")
           return
       confirm = input(f"Are you sure you want to drop '{course}'? (yes/no): ").strip().lower()
       if confirm != "yes":
           print("Drop cancelled.")
           return
       self.courses.remove(course)
       if course in system.courses and self.name in system.courses[course]["students"]:
           system.courses[course]["students"].remove(self.name)
       print(f"Dropped course: '{course}'")
       system.save_data()


    def view_profile(self):
       print("=" * get_terminal_width())
       print(f"{'PROFILE':^50}")
       print("=" * get_terminal_width())
       print(f"Name: {self.name}")
       print("Registered Courses:")
       if self.courses:
          for course in self.courses:
              print(f"- {course}")
       else:
          print("No courses registered.")
       print("=" * get_terminal_width())

   
    def change_password(self, system):
        old_pass = getpass.getpass("Enter old password: ")
        if old_pass == self.password:
            new_pass = getpass.getpass("Enter new password: ")
            confirm_pass = getpass.getpass("Confirm new password: ")
            if new_pass == confirm_pass:
                self.password = new_pass
                system.save_data()
                print("Password changed successfully!")
            else:
                print("Passwords don't match!")
        else:
            print("Incorrect old password!")

class Admin(User):
    def __init__(self):
        super().__init__("admin", "admin123")
    
    def show_menu(self, system):
        while True:
            self.clear_screen()
            terminal_width = get_terminal_width()
            print("=" * terminal_width)
            print(center_text(f"ADMIN PORTAL: {self.name}"))
            print("=" * terminal_width)
            print("=" * get_terminal_width())
            print("1. Add New Course")
            print("2. Remove Course")
            print("3. Update Course")
            print("4. View All Courses")
            print("5. View All Students")
            print("6. Logout")
            print("=" * get_terminal_width())
            
            choice = input("\nEnter your choice (1-6): ")
            self.clear_screen()
            
            if choice == "1":
                self.add_course(system)
            elif choice == "2":
                self.remove_course(system)
            elif choice == "3":
                self.update_course(system)
            elif choice == "4":
                system.display_courses()
            elif choice == "5":
                system.display_all_students()
            elif choice == "6":
                print("Logging out...")
                system.save_data()
                break
            else:
                print("Invalid choice!")
            
            input("\nPress Enter to continue...")
    
    def add_course(self, system):
        course = input("Enter new course name: ")
        if course in system.courses:
            print("Course already exists!")
            return
        try:
            capacity = int(input("Enter course capacity: "))
            system.courses[course] = {"students": [], "capacity": capacity}
            print(f"Course '{course}' added successfully!")
        except ValueError:
            print("Invalid capacity! Must be a number.")
    
    def remove_course(self, system):           
       system.display_courses()
       print("\nSelect course by number to remove:")
       try:
           choice = int(input("Enter course number: ")) - 1
           course_names = list(system.courses.keys())
           if 0 <= choice < len(course_names):
               course = course_names[choice]
           else:
               print("Invalid course number!")
               return
       except ValueError:
           print("Please enter a valid number.")
           return
       confirm = input(f"Are you sure you want to remove '{course}'? (yes/no): ").strip().lower()
       if confirm != "yes":
           print("Removal cancelled.")
           return
       for student in system.students.values():
           if course in student.courses:
               student.courses.remove(course)
       if course in system.courses:
         del system.courses[course]
       print(f"Course '{course}' removed successfully!")
       system.save_data()

    def update_course(self, system):
       system.display_courses()
       print("\nSelect course by number to update:")
       try:
           choice = int(input("Enter course number: ")) - 1
           course_names = list(system.courses.keys())
           if 0 <= choice < len(course_names):
               course = course_names[choice]
           else:
               print("Invalid course number!")
               return
       except ValueError:
           print("Please enter a valid number.")
           return
       new_name = input("Enter new course name (press Enter to keep unchanged): ").strip()
       capacity_input = input("Enter new capacity (press Enter to keep unchanged): ").strip()
       if not new_name:
           new_name = course
       elif new_name != course:
           if new_name in system.courses:
               print("Course with this name already exists!")
               return
           system.courses[new_name] = system.courses.pop(course)
           for student in system.students.values():
               if course in student.courses:
                   student.courses.remove(course)
                   student.courses.append(new_name)
           course = new_name
       if capacity_input:
           try:
               new_capacity = int(capacity_input)
               if new_capacity < len(system.courses[course]['students']):
                   print(f"New capacity cannot be less than enrolled students ({len(system.courses[course]['students'])})!")
                   return
               system.courses[course]['capacity'] = new_capacity
           except ValueError:
               print("Invalid capacity! Must be a number.")
               return
       print(f"Course '{course}' updated successfully!")
       system.save_data()

class CourseRegistrationSystem:
    def __init__(self):
        self.students = {}
        self.admin = Admin()
        self.courses = {}
        self.data_file = "registration_data.json"
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)          
                self.courses = data.get('courses', {})                
                students_data = data.get('students', {})
                for name, student_data in students_data.items():
                    student = Student(name, student_data['password'])
                    student.courses = student_data.get('courses', [])
                    self.students[name] = student
    
    def save_data(self):
        data = {
            'courses': self.courses,
            'students': {
                name: {
                    'password': student.password,
                    'courses': student.courses
                }
                for name, student in self.students.items()
            }
        }
        
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def display_courses(self):
       print("\nAVAILABLE COURSES")
       terminal_width = get_terminal_width()
       print("=" * terminal_width)
       if not self.courses:
           print("No courses available.")
           return
       header = "{:<10} {:<30} {:<10} {:<10}".format("No.", "Course Name", "Enrolled", "Capacity")
       print(header)
       print("-" * 50)
       for i, (course, data) in enumerate(self.courses.items(), start=1):
          row = "{:<10} {:<30} {:<10} {:<10}".format(i, course, len(data['students']), data['capacity'])
          print(row)
    
    def display_all_students(self):
        print("\nREGISTERED STUDENTS")
        print("=" * get_terminal_width())
        if not self.students:
            print("No students registered.")
            return
        
        print("{:<20} {:<30}".format("Student Name", "Courses"))
        print("-" * 50)
        for student in self.students.values():
            courses = ', '.join(student.courses) if student.courses else "None"
            print("{:<20} {:<30}".format(student.name, courses))

    def register_student(self):
        print("\nSTUDENT REGISTRATION")
        print("=" * get_terminal_width())
        name = input("Enter your name: ")
        if name in self.students:
            print("Student already registered!")
            return
    
        password = getpass.getpass("Set a password: ")
        confirm = getpass.getpass("Confirm password: ")
        if password != confirm:
            print("Passwords don't match!")
            return
    
        student = Student(name, password)
        self.students[name] = student
        print("\nRegistration successful!")
        self.save_data()

    def login_student(self):
       self.clear_screen()
       print("\nSTUDENT LOGIN")
       print("=" * get_terminal_width())
       name = input("Enter your name: ")
       password = getpass.getpass("Enter your password: ")

       student = self.students.get(name)
       if student and student.password == password:
           print("\nLogin successful!")
           self.clear_screen()
           while True:
               self.clear_screen() 
               print("\n" + "=" * 50)
               print(f"STUDENT PORTAL: {student.name}".center(50))
               print("=" * get_terminal_width())
               print("1. View Profile")
               print("2. View Available Courses")
               print("3. Register for Course")
               print("4. Drop Course")
               print("5. Change Password")
               print("6. Logout")
               print("=" * get_terminal_width())

               choice = input("\nEnter your choice (1-6): ")
               self.clear_screen()

               if choice == "1":
                   student.view_profile()
               elif choice == "2":
                   self.display_courses()
               elif choice == "3":
                  student.register_course(self)
               elif choice == "4":
                  student.drop_course(self)
               elif choice == "5":
                   student.change_password(self)
               elif choice == "6":
                   print("Logging out...")
                   self.save_data()
                   break
               else:
                   print("Invalid choice!")

               input("\nPress Enter to continue...")
       else:
           print("Invalid name or password!")

    def view_profile(self, student):
       print(f"{'PROFILE':^50}")
       print("=" * get_terminal_width())
       print(f"{'Name':<20} : {student.name}")
       print("-" * 50)
       print(f"{'Registered Courses':<20} :")
       if student.courses:
           print(f"{'Course Name':<30} | {'Status':<10}")
           print("-" * 50)
           for course in student.courses:
               print(f"{course:<30} | {'Enrolled':<10}")
       else:
           print("No courses registered.")
       print("=" * get_terminal_width())


    def admin_login(self):
        print("\nADMIN LOGIN")
        print("=" * get_terminal_width())
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        
        if username == self.admin.name and password == self.admin.password:
            print("\nLogin successful!")
            return self.admin
        else:
            print("\nInvalid credentials!")
            return None
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

class ProjectInfo:
    def __init__(self):
        self.title = "Course Registration System"
        self.developer = ["Moaza"]
    
    def show_intro(self):
        self.clear_screen()
        terminal_width = get_terminal_width()
        print("=" * terminal_width)
        print(center_text(self.title))
        print("\nDeveloped By:")
        for dev in self.developer:
            print(f"- {dev}")
        print("=" * get_terminal_width())
        input("\nPress Enter to continue to main menu...")
    
    def show_main_menu(self, system):
        while True:
            self.clear_screen()
            print("\n" + "=" * 50)
            terminal_width = get_terminal_width()
            print("=" * terminal_width)
            print(center_text("MAIN MENU"))
            print("=" * terminal_width)
            print("1. Admin Login")
            print("2. Student Login")
            print("3. Student Registration")
            print("4. Exit")
            print("=" * get_terminal_width())
            
            choice = input("\nEnter your choice (1-4): ")
            system.clear_screen()
            
            if choice == "1":
                admin = system.admin_login()
                if admin:
                    admin.show_menu(system)
            elif choice == "2":
                student = system.login_student()
                if student:
                    system.clear_screen()
                    print("\n" + "=" * 50)
                    print(f"STUDENT PROFILE: {student.name}".center(50))
                    print("=" * 50)
                    print("{:<20} {}".format("Name", student.name))
                    print("{:<20} {}".format("Registered Courses", ', '.join(student.courses) if student.courses else "None"))
                    print("=" * get_terminal_width())
                    input("\nPress Enter to return to main menu...")
            elif choice == "3":
                system.register_student()
            elif choice == "4":
                print("\nThank you for using the system. Goodbye!")
                system.save_data()
                break
            else:
                print("Invalid choice!")
            
            input("\nPress Enter to continue...")
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

# Main Program
if __name__ == "__main__":
    system = CourseRegistrationSystem()
    project = ProjectInfo()
    
    project.show_intro()

    project.show_main_menu(system)
