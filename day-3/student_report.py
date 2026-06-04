# This code defines a Student class that represents a student with their name, roll number, and marks. 
# It includes methods to calculate the average marks and determine the grade based on the average. 
# The __str__ method provides a formatted string representation of the student's information.


class Student:
    school_name = "ABC High School"
    def __init__(self, name, rollno, marks):
        self.name = name
        self.rollno = rollno
        self.marks = marks
    def average(self):
        return sum(self.marks) / len(self.marks)
    def grade(self):
        avg = self.average()
        if avg >= 90:
            return 'A'
        elif avg >= 80:
            return 'B'
        elif avg >= 70:
            return 'C'
        elif avg >= 60:
            return 'D'
        else:
            return 'F'
    def __str__(self):
        return f"Name: {self.name}\nRoll No: {self.rollno}\nMarks: {self.marks}\nAverage: {self.average():.2f}\nGrade: {self.grade()}\nSchool: {self.school_name}"
    
s1 = Student("Alice", 1, [85, 90, 78])
s2 = Student("Bob", 2, [92, 88, 95])
print(s1)
print(s2)

# Difference between class variable and instance variable:
# A class variable is shared among all instances of a class, while an instance variable is unique to each instance.
# In the above code, 'school_name' is a class variable because it is defined at the class level and is shared by all instances of the Student class.
# The instance variables are 'name', 'rollno', and 'marks' because they are defined within the __init__ method and are unique to each student instance.
