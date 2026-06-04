# Task 4: Load a CSV into Pandas, select specific columns, and filter rows.
# In this code, we use the Pandas library to read a CSV file named "student.csv" into a DataFrame.
# We then demonstrate how to select specific columns from the DataFrame and apply filters to extract rows based on certain conditions, such as math scores greater than 75 and science scores for students in Mumbai greater than or equal to 75. 
# The results are printed in a clear format for easy analysis.
import pandas as pd
df = pd.read_csv("student.csv")

print("=== Selected columns: name, city, math_score ===")
print(df[["name", "city", "math_score"]])

high_math = df[df["math_score"] > 75][["name", "city", "math_score"]]
print("\n=== Filter: math_score > 75 ===")
print(high_math)

mumbai_science = df[(df["city"] == "Mumbai") & (df["science_score"] >= 75)][
    ["name", "city", "science_score"]
]
print("\n=== Filter: city == 'Mumbai' AND science_score >= 75 ===")
print(mumbai_science)
