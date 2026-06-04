# Task 7: Produce quick insights using describe() on numeric columns and value_counts() on a categorical column.
# In this code, we use the `describe()` method to generate a summary of the numeric columns (math_score, science_score, english_score) in the DataFrame, which includes count, mean, standard deviation, min, max, and quartiles.
# We also use the `value_counts()` method to count the number of students from each city, which is a categorical column. 
# Finally, we provide observations based on the outputs of both methods to highlight key insights about the students' performance and distribution across cities. 
import pandas as pd

df = pd.read_csv("student.csv")

print("=== describe() — numeric summary ===")
print(df[["math_score", "science_score", "english_score"]].describe().round(1))
print("""
Observation: math_score has the widest spread (std ≈ 19.6) and the lowest
minimum (40), meaning student performance varies most in Math compared to
Science and English.
""")

print("=== value_counts() — students per city ===")
print(df["city"].value_counts())
print("""
Observation: Mumbai has the most students (4), followed by Delhi and
Bangalore (3 each) — useful for knowing where cohort support is most needed.
""")
