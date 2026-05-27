# intro.py — Collects personal info from the user and prints a formatted introduction.

# --- Collect input from the user ---
name           = input("Enter your name: ")
age            = input("Enter your age: ")
city           = input("Enter your city: ")
favourite_subject = input("Enter your favourite subject: ")
target_role       = input("Enter your target role: ")


# --- Store everything in a single dict ---
student = {
    "name":             name,
    "age":              age,
    "city":             city,
    "favourite_subject": favourite_subject,
    "target_role":       target_role
}

# --- Print a 4-line introduction using f-strings ---
print()
print(f"Hi! My name is {student['name'].title()} and I am {student['age']} years old.")
print(f"I'm from {student['city'].title()}.")
print(f"My favourite subject is {student['favourite_subject'].title()}.")
print(f"My target role is {student['target_role'].title()}.")

print("\nNice to meet you!".upper())
print("Let's have a great learning experience together!".lower())
