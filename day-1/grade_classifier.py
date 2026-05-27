# This file contains code to classify students' scores into grades and print the results.  
# The classify_grade function takes a score as input and returns the corresponding grade based on the defined thresholds. 
# The program iterates over a list of students, classifies their scores into grades, and prints the results in a formatted manner.
students = [
    {"name": "Alice", "score": 85},
    {"name": "Bob", "score": 72},     
    {"name": "Charlie", "score": 90},
    {"name": "David", "score": 65},
    {"name": "Eve", "score": 78}
]
def classify_grade(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'
    
for student in sorted(students, key = lambda x: x['score'], reverse=True):
    grade = classify_grade(student['score'])
    print(f"{student['name']} received grade: {grade}")