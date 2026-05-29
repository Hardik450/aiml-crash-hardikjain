# This code demonstrates basic data manipulation and analysis using the pandas library in Python. 
# It creates a DataFrame with student information, calculates average scores for different subjects, identifies the student with the highest total score, counts the number of students from each city, and lists students with a math score above a certain threshold. 
# Additionally, it shows how to find the top students based on their total scores using the nlargest method for efficient retrieval.

import pandas as pd
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Heidi', 'Ivan', 'Judy'],
    'city': ['New York', 'Los Angeles', 'Chicago', 'Dallas', 'Miami', 'New York', 'Los Angeles', 'Chicago', 'Dallas', 'Miami'],
    'math_score': [85, 92, 70, 60, 55, 78, 88, 90, 82, 95],
    'science_score': [90, 88, 75, 65, 50, 80, 85, 92, 78, 95],
    'english_score': [78, 95, 80, 58, 45, 82, 90, 91, 85, 94]
})

math_avg_score = df['math_score'].mean()
science_avg_score = df['science_score'].mean()
english_avg_score = df['english_score'].mean()
print(f"Average Math Score: {math_avg_score:.2f}")
print(f"Average Science Score: {science_avg_score:.2f}")
print(f"Average English Score: {english_avg_score:.2f}")

total_score = df['math_score'] + df['science_score'] + df['english_score']
print()
print(f"The user with the highest total score across all subjects is: {df.loc[total_score.idxmax(), 'name']}")

students_from_cities = df['city'].value_counts()
print()
print("Number of students from each city:")
for city, count in students_from_cities.items():
    print(f"{city}: {count}")

print()
students_with_math_score_above_75 = df[df['math_score'] > 75]
print("Students with a math score above 75:")
for index, row in students_with_math_score_above_75.iterrows():
    print(f"{row['name']} from {row['city']} with a math score of {row['math_score']}")

# df.sort_values() can be used to sort the DataFrame by a specific column, such as 'math_score', in ascending or descending order.
# df.nlargest() can be used to find the top n rows with the largest values in a specific column, such as 'math_score', which is more efficient than sorting the entire DataFrame when only a few top entries are needed.
# In this case, df.nlargest(1, 'math_score') would return the row with the highest math score directly without sorting the entire DataFrame.

print()
print("Top 3 students with the highest total scores:")
df['total_score'] = total_score
top_total_scores = df.nlargest(3, 'total_score')
for index, row in top_total_scores.iterrows():
    print(f"{row['name']} from {row['city']} with a total score of {row['total_score']}")