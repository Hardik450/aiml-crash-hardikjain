# This code demonstrates how to create, read, and manipulate CSV files using the csv module in Python.
# It includes functions to create a CSV file with student records, read the records from the file, calculate average scores, and create a report with average scores and grades.
# The code also explains the difference between csv.writer() and csv.DictWriter() for writing data to CSV files.
# The data used in this example consists of student names and their scores in Math, Science, and English. The results are saved in 'students.csv' and 'results.csv' files.

import csv

def create_csv_file(filename, data):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Math', 'Science', 'English'])
        writer.writerows(data)

def read_csv_file(filename):
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        return list(reader)
    
def calculate_avg(records):
    avg_records = []
    for record in records[1:]:
        name = record[0]
        scores = list(map(float, record[1:]))
        avg_score = sum(scores) / len(scores)
        avg_records.append((name, avg_score))
    return avg_records

def create_report(records):
    report = []
    for name, avg in records:
        if avg >= 90:
            grade = 'A'
        elif avg >= 80:
            grade = 'B'
        elif avg >= 70:
            grade = 'C'
        elif avg >= 60:
            grade = 'D'
        else:
            grade = 'F'
        report.append((name, avg, grade))
    with open('results.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Average Score', 'Grade'])
        writer.writerows(report)

data = [
    ['Alice', 85, 90, 78],
    ['Bob', 92, 88, 95],
    ['Charlie', 70, 75, 80],
    ['David', 60, 65, 58],
    ['Eve', 55, 50, 45]
]
create_csv_file('students.csv', data)
print("CSV file 'students.csv' created with student records.")
records = read_csv_file('students.csv')
print("Student records read from 'students.csv':")
for record in records:
    print(record)
avg_records = calculate_avg(records)
print("Average scores calculated for each student:")
for name, avg in avg_records:
    print(f"{name}: {avg:.2f}")
create_report(avg_records)
print("Report created in 'results.csv' with average scores and grades.")

# Difference between csv.writer() and csv.DictWriter():
# csv.writer() is used to write data to a CSV file in a simple list format, where each row is a list of values.
# csv.DictWriter() is used to write data to a CSV file in a dictionary format, where each row is a dictionary with keys corresponding to the column headers. 
# This allows for more flexibility and readability when writing data to CSV files.

data_dict = [
    {'Name': 'Alice', 'Math': 85, 'Science': 90, 'English': 78},
    {'Name': 'Bob', 'Math': 92, 'Science': 88, 'English': 95},
    {'Name': 'Charlie', 'Math': 70, 'Science': 75, 'English': 80},
    {'Name': 'David', 'Math': 60, 'Science': 65, 'English': 58},
    {'Name': 'Eve', 'Math': 55, 'Science': 50, 'English': 45}
]
def create_csv_file_dict(filename, data):
    with open(filename, mode='w', newline='') as file:
        fieldnames = ['Name', 'Math', 'Science', 'English']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

create_csv_file_dict('students_dict.csv', data_dict)
print("CSV file 'students_dict.csv' created with student records in dictionary format.")
