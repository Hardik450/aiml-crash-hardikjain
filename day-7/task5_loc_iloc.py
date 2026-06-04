# Task 5: Demonstrate .loc (label-based) vs .iloc (position-based) on the same DataFrame.
# In this code, we read a CSV file into a Pandas DataFrame and then show how to use the `.loc` method for label-based indexing to select rows where the city is "Mumbai" and specific columns.
# We also demonstrate the `.iloc` method for position-based indexing to select the first three rows and the first three columns of the DataFrame. 
# Finally, we provide a plain language explanation of the differences between `.loc` and `.iloc` to clarify when to use each method based on whether you are working with labels or numeric positions.
import pandas as pd

df = pd.read_csv("student.csv")

print("=== .loc — rows where city == 'Mumbai', columns: name & math_score ===")
print(df.loc[df["city"] == "Mumbai", ["name", "math_score"]])

print("\n=== .iloc — first 3 rows, first 3 columns (by position) ===")
print(df.iloc[0:3, 0:3])

print("""
Difference in plain language:
  .loc  -> uses LABELS (column names, index labels, or boolean conditions).
           Example: df.loc[df['city'] == 'Mumbai', ['name', 'math_score']]
  .iloc -> uses INTEGER POSITIONS (row number, column number — zero-based).
           Example: df.iloc[0:3, 0:3]
Use .loc when you know the name of what you want.
Use .iloc when you want a specific numeric slice of the table.
""")
