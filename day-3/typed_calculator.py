# A simple calculator that performs basic arithmetic operations with type hints for better code clarity and error checking.
# The calculator supports addition, subtraction, multiplication, division, exponentiation, and modulo operations.
# The code includes error handling for division and modulo by zero, as well as invalid input and operation selection. 
# The calculator function serves as the main entry point for user interaction.
from typing import Optional
def add(a: int, b: int) -> int:
    """
    It takes two integers as input and returns their sum.
    :param a: The first number to be added
    :param b: The second number to be added
    :return: The sum of a and b
    """
    return a + b

def subtract(a: int, b: int) -> int:
    """
    It takes two integers as input and returns their difference.
    :param a: The first number
    :param b: The second number
    :return: The difference of a and b
    """
    return a - b

def multiply(a: int, b: int) -> int:
    """It takes two integers as input and returns their product.
    :param a: The first number to be multiplied 
    :param b: The second number to be multiplied
    :return: The product of a and b
    """
    return a * b

def divide(a: float, b: float) -> Optional[float]:
    """
    It takes two floats as input and returns their quotient.
    :param a: The first number
    :param b: The second number
    :return: The quotient of a and b or an error message
    """
    if b == 0:
        return "Error: Division by zero is not allowed."
    return a / b

def power(a: float, b: float) -> float:
    """
    It takes two floats as input and returns the result of raising the first number to the power of the second.
    :param a: The base number
    :param b: The exponent
    :return: The result of a raised to the power of b
    """
    return a ** b

def modulo(a: int, b: int) -> Optional[int]:
    """
    It takes two integers as input and returns the remainder of dividing the first number by the second.
    :param a: The dividend
    :param b: The divisor
    :return: The remainder of a divided by b or an error message
    """
    if b == 0:
        return "Error: Modulo by zero is not allowed."
    return a % b

def calculator():
    print("Welcome to the Simple Calculator!")
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        operation = input("Choose an operation (+, -, *, /, ^, %): ")

        dict_operations = {
            '+': add,
            '-': subtract,
            '*': multiply,
            '/': divide,
            '^': power,
            '%': modulo
        }
        if operation in dict_operations:
            result = dict_operations[operation](num1, num2)
        else:
            return "Invalid operation selected."

        return f"The result of {num1} {operation} {num2} is: {result}"
    except ValueError:
        return "Please enter valid numbers."
    
if __name__ == "__main__":
    print(calculator())