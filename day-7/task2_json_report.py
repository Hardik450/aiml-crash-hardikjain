# Task 2: Load a JSON file and print a short formatted report using f-strings
# and a list comprehension for compact transformation.
# In this code, we define a function `print_report` that reads a learner's profile from a JSON file and prints a concise report. 
# The function uses f-strings for formatting the output and a list comprehension to transform the skills into uppercase for better visibility. 
# The `main` block demonstrates how to call the `print_report` function with a sample JSON file named "learner.json".

import json


def print_report(filepath: str) -> None:
    """Read a learner JSON file and print a concise report."""
    with open(filepath, "r") as f:
        data: dict = json.load(f)

    skills_display: list[str] = [skill.upper() for skill in data["skills"]]

    print(f"--- Learner Report ---")
    print(f"Name     : {data['name']}")
    print(f"Role     : {data['role']}")
    print(f"Cohort   : {data['cohort']}")
    print(f"Projects : {data['projects_completed']} completed")
    print(f"Skills   : {', '.join(skills_display)}")


if __name__ == "__main__":
    print_report("learner.json")
