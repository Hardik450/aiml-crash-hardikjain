# This file contains code for a simple number guessing game where the user has to guess a randomly generated number between 1 and 100 within a limited number of attempts.
# The program uses the random module to generate a random number and handles user input with error checking to ensure that only valid integers are accepted as guesses.

import random
number = random.randint(1, 100)
attempts = 7
print("Welcome to the Number Guessing Game!")
print(f"I'm thinking of a number between 1 and 100. You have {attempts} attempts to guess it.")
for attempt in range(1, attempts + 1):
    try:
        guess = int(input(f"Attempt {attempt}: Enter your guess: "))
        if guess < number:
            print("Too low! Try again.")
        elif guess > number:
            print("Too high! Try again.")
        else:
            print(f"Congratulations! You've guessed the number {number} in {attempt} attempts!")
            break
    except ValueError:
        print("Please enter a valid integer.")