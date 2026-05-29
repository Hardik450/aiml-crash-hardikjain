# Comprehension Drills
# This script demonstrates the use of list comprehensions, dictionary comprehensions, and set comprehensions to filter and transform data in various ways.
# The code includes examples of filtering integers, transforming words, converting temperatures, flattening nested lists, and extracting data from dictionaries and sets.


int_list = [22, 35, 27, 42, 19, 50, 31, 28, 40, 26, 33, 24, 38, 29, 41, 30, 36, 25, 27, 34]
word_list = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew", "kiwi", "lemon", "plum", "berry", "peach", "mango", "nectarine", "orange", "papaya", "quince", "raspberry", "strawberry"]
temperature_list = [72, 85, 78, 90, 68, 80, 82, 75, 88, 70, 77, 83, 79, 91, 74, 81, 76, 89, 73]

filtered_ints = [num for num in int_list if num % 3 == 0]
filtered_words = [word.title() for word in word_list if len(word) > 4]
filtered_temperatures = [(temp*9/5) + 32 for temp in temperature_list]

nested_list = [[1, 2], [3, 4], [5, 6], [7, 8]]
flattened_list = [num for sublist in nested_list for num in sublist]

print("Filtered Integers (divisible by 3):", filtered_ints)
print("Filtered Words (length > 4, title case):", filtered_words)
print("Filtered Temperatures (Celsius to Fahrenheit):", filtered_temperatures)
print("Flattened List:", flattened_list)

dict_list = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}, {"name": "Charlie", "age": 35}]
names = [d["name"] for d in dict_list]
ages = [d["age"] for d in dict_list]

set_list = [{"name": "Alice"}, {"name": "Bob"}, {"name": "Charlie"}, {"name": "Alice"}]
set_of_names = {d["name"] for d in set_list}
print("Names:", names)
print("Ages:", ages)
print("Set of Names:", set_of_names)
