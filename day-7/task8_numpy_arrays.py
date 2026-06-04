# Task 8: Create NumPy arrays, inspect their properties, and slice them.
# In this code, we demonstrate how to create different types of NumPy arrays, such as a 1-D array using `np.array()`, a range of values using `np.arange()`, a 2-D array of zeros using `np.zeros()`, and a linearly spaced array using `np.linspace()`.
# We then print the values, shape, data type, and number of dimensions for each array to understand their properties. 
# Finally, we show how to slice both a 1-D array and a 2-D array to extract specific elements, rows, columns, and subarrays, demonstrating the powerful indexing capabilities of NumPy arrays.

import numpy as np

a = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
b = np.arange(0, 50, 5)           
c = np.zeros((3, 4))              
d = np.linspace(0.0, 1.0, 6)      

print("=== Array a (np.array) ===")
print(f"  values : {a}")
print(f"  shape  : {a.shape}  |  dtype : {a.dtype}  |  ndim : {a.ndim}")

print("\n=== Array b (np.arange) ===")
print(f"  values : {b}")
print(f"  shape  : {b.shape}  |  dtype : {b.dtype}  |  ndim : {b.ndim}")

print("\n=== Array c (np.zeros, 2-D) ===")
print(c)
print(f"  shape  : {c.shape}  |  dtype : {c.dtype}  |  ndim : {c.ndim}")

print("\n=== Array d (np.linspace) ===")
print(f"  values : {d}")
print(f"  shape  : {d.shape}  |  dtype : {d.dtype}  |  ndim : {d.ndim}")

print("\n=== Slicing array a ===")
print(f"  a[0]       = {a[0]}       (first element)")
print(f"  a[-1]      = {a[-1]}      (last element — negative index)")
print(f"  a[2:6]     = {a[2:6]}  (subarray: index 2 to 5 inclusive)")
print(f"  a[::2]     = {a[::2]}  (every other element)")

print("\n=== Slicing 2-D array c ===")
print(f"  c[0, :]    = {c[0, :]}   (entire first row)")
print(f"  c[:, 1]    = {c[:, 1]}          (entire second column)")
print(f"  c[1:3, 1:3] =\n{c[1:3, 1:3]}   (2x2 subarray from rows 1-2, cols 1-2)")
