# Task 1: Build a Student Profile Card using f-strings and type hints.
# In this code, we define a function `build_profile_card` that takes a learner's profile as a dictionary and returns a formatted string representing the profile card. 
# The function uses f-strings for formatting and includes type hints for better code clarity. 
# The `main` function demonstrates how to create a learner profile and print the resulting profile card.

def build_profile_card(profile: dict[str, str | list[str]]) -> str:
    """Accept a learner profile dict and return a formatted 4-line card."""
    skills_line = ", ".join(profile["skills"])
    card = (
        f"┌─────────────────────────────────────┐\n"
        f"  Name    : {profile['name']}\n"
        f"  Role    : {profile['role']}\n"
        f"  City    : {profile['city']}\n"
        f"  Skills  : {skills_line}\n"
        f"└─────────────────────────────────────┘"
    )
    return card


def main() -> None:
    learner: dict[str, str | list[str]] = {
        "name": "Alex Johnson",
        "role": "AI/ML Intern",
        "city": "Mumbai",
        "skills": ["Python", "Pandas", "NumPy", "Git"],
    }
    print(build_profile_card(learner))


if __name__ == "__main__":
    main()
