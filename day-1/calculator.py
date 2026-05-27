# Simple Calculator in Python
# This program allows the user to perform basic arithmetic operations: addition, subtraction, multiplication, and division.
# The user is prompted to enter two numbers and select an operation. The program then performs the calculation and displays the result.
# The calculator also handles division by zero and invalid inputs gracefully, providing appropriate error messages.
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Division by zero is not allowed."
    return a / b

def calculator():
    print("Welcome to the Simple Calculator!")
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        operation = input("Choose an operation (+, -, *, /): ")

        if operation == '+':
            result = add(num1, num2)
        elif operation == '-':
            result = subtract(num1, num2)
        elif operation == '*':
            result = multiply(num1, num2)
        elif operation == '/':
            result = divide(num1, num2)
        else:
            return "Invalid operation selected."

        return f"The result of {num1} {operation} {num2} is: {result}"
    except ValueError:
        return "Please enter valid numbers."
    
if __name__ == "__main__":
    print(calculator())


def calculator_new():
    print("Welcome to the Simple Calculator!")
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        operation = input("Choose an operation (+, -, *, /): ")

        dict_operations = {
            '+': add,
            '-': subtract,
            '*': multiply,
            '/': divide
        }
        if operation in dict_operations:
            result = dict_operations[operation](num1, num2)
        else:
            return "Invalid operation selected."

        return f"The result of {num1} {operation} {num2} is: {result}"
    except ValueError:
        return "Please enter valid numbers."
    
if __name__ == "__main__":
    print(calculator_new())