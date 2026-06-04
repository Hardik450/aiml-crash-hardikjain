# Task 3: A class representing a learner project in an intern workflow.
# In this code, we define a `Project` class that encapsulates the details of a learner's project, including the title, tech stack, and status.
# The class includes an initializer to set these attributes and a method `summary` that returns a formatted string summarizing the project details. 
# We then create two instances of the `Project` class to demonstrate how it can be used to represent different projects and print their summaries.

class Project:
    """Represents a learner's project with a title, tech stack, and status."""

    def __init__(self, title: str, tech_stack: list[str], status: str) -> None:
        self.title = title
        self.tech_stack = tech_stack
        self.status = status

    def summary(self) -> str:
        """Return a formatted one-line project summary."""
        techs = ", ".join(self.tech_stack)
        return (
            f"Project  : {self.title}\n"
            f"Stack    : {techs}\n"
            f"Status   : {self.status}"
        )

p1 = Project("Student Grade Analyser", ["Python", "Pandas"], "In Progress")
p2 = Project("Chatbot Prototype", ["Python", "OpenAI API", "Flask"], "Completed")

print(p1.summary())
print()
print(p2.summary())
