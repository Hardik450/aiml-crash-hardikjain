# This file contains code to calculate the tip amount and total bill for different bills and a given tip percentage.
# The calculate_tip function takes the bill amount and tip percentage as input, calculates the tip amount and total amount, and returns them in a dictionary. 
# The program then iterates over a list of bills, calculates the tip and total for each bill, and prints the results formatted to two decimal places.
def calculate_tip(bill, tip_percent):
    tip_amount = bill * (tip_percent / 100)
    total_amount = bill + tip_amount
    return {'tip_amount': tip_amount, 'total_amount': total_amount}

# 3 different bills
bills = [50, 100, 150]
tip_percent = 15
for bill in bills:
    result = calculate_tip(bill, tip_percent)
    print(f"Bill: ${bill:.2f}, Tip: ${result['tip_amount']:.2f}, Total: ${result['total_amount']:.2f}")

# Difference between return and print:
# The calculate_tip function returns a dictionary with the tip amount and total amount, which can be used later in the code.
# The print statements inside the loop display the results immediately, but do not allow for further manipulation of the values. If we wanted to use the tip and total amounts for further calculations, we would need to store them in variables instead of just printing them.
