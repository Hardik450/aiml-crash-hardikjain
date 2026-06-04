import math
import functools

@functools.total_ordering
class Fraction:
    numerator: int
    denominator: int
    def __init__(self, numerator: int, denominator: int):
        if denominator == 0:
            raise ValueError("Denominator cannot be zero.")
        self.numerator = numerator
        self.denominator = denominator
    def __str__(self):
        return f"{self.numerator}/{self.denominator}"
    def __add__(self, other):
        new_numerator = self.numerator * other.denominator + other.numerator * self.denominator
        new_denominator = self.denominator * other.denominator
        gcd = math.gcd(new_numerator, new_denominator)
        return Fraction(new_numerator // gcd, new_denominator // gcd)
    def __eq__(self, other):
        return self.numerator / self.denominator == other.numerator / other.denominator
    def __lt__(self, other):
        return self.numerator / self.denominator < other.numerator / other.denominator

f1 = Fraction(1, 2)
f2 = Fraction(3, 4)
print(f"Fraction 1: {f1}")
print(f"Fraction 2: {f2}")
print(f"Sum of {f1} and {f2}: {f1 + f2}")
print(f"Is {f1} equal to {f2}? {'Yes' if f1 == f2 else 'No'}")
print(f"Is {f1} less than {f2}? {'Yes' if f1 < f2 else 'No'}")

# @functools.total_ordering is a class decorator that fills in missing ordering methods based on the ones that are defined.
# If you define __eq__ and one of the other ordering methods (__lt__, __le__, __gt__, or __ge__), the decorator will automatically generate the rest of the ordering methods for you.
# In the above code, we have defined the __eq__ and __lt__ methods for the Fraction class.
# If we were to use the @functools.total_ordering decorator, we would only need to define one of the ordering methods (e.g., __lt__) and the decorator would automatically generate the other ordering methods (__le__, __gt__, and __ge__) based on the defined __eq__ and __lt__ methods. 
# This can help reduce boilerplate code and make it easier to implement all the necessary comparison operations for a class.

print(f"Is {f1} greater than or equal to {f2}? {'Yes' if f1 >= f2 else 'No'}")  # This will work if we use @functools.total_ordering
