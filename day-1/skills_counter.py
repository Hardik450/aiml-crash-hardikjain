# This file contains code to count the number of skills in a list and print them with their respective numbers.
skills = ['Python', 'Data Science', 'Machine Learning', 'Deep Learning', 'NLP']
for i, skill in enumerate(skills, start=1):
    print(f"{i}. {skill}")
print(f"\nTotal number of skills: {len(skills)}")