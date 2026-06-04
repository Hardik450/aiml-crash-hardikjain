# Task 6: Identify missing values, then handle them with dropna() and fillna().
# In this code, we create a DataFrame with some missing values (NaN) in the "city", "math_score", "science_score", and "english_score" columns.
# We first print the original DataFrame and count the missing values in each column using `isnull().sum()`.
# Next, we demonstrate how to use `dropna()` to remove rows that have missing values in the "city" column, and then we use `fillna()` to replace missing numeric scores with the mean of their respective columns. 
# Finally, we print the modified DataFrames to show the results of both operations.
import pandas as pd
import numpy as np

data = {
    "name":          ["Alice", "Bob",  "Carol", "David", "Eva",  "Frank"],
    "city":          ["Mumbai", None,  "Delhi", "Mumbai", None,  "Bangalore"],
    "math_score":    [88,       55,    np.nan,  45,       78,    63],
    "science_score": [76,       60,    89,      np.nan,   82,    71],
    "english_score": [91,       np.nan, 85,     55,       88,    69],
}

df = pd.DataFrame(data)

print("=== Original DataFrame ===")
print(df)

print("\n=== Missing value count per column ===")
print(df.isnull().sum())

df_dropped = df.dropna(subset=["city"])
print("\n=== After dropna(subset=['city']) — rows with no city removed ===")
print(df_dropped)

df_filled = df.copy()
for col in ["math_score", "science_score", "english_score"]:
    df_filled[col] = df_filled[col].fillna(round(df_filled[col].mean(), 1))

print("\n=== After fillna(mean) — missing scores replaced with column average ===")
print(df_filled)
