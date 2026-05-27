# This program checks if a number is even or odd and handles invalid input gracefully.
try:
    number = int(input("Enter a number: "))
    if number % 2 == 0:
        print(f"{number} is an even number.")
    elif number % 2 == 1:
        print(f"{number} is an odd number.")
    else:
        print("The zero is neither even nor odd.")
except ValueError:
    print("Please enter a valid integer.")

# When given a string input, the int() function will raise a ValueError, which we catch and print a user-friendly message.