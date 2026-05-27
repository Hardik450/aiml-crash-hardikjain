# This file contains code to create a simple contact book and search for contacts by name.
# The contacts are stored in a list of dictionaries, where each dictionary represents a contact with their name, phone number, and email address. 
# The find_contact function takes a name as input and searches through the contact list to find a matching contact, returning the contact details if found or a message if not found. 
# The program prompts the user to enter a name to search for and displays the results accordingly.


contacts = [
    {
        "name": "Alice",
        "phone": "123-456-7890",
        "email": "alice@gmail.com"
    },
    {
        "name": "Bob",
        "phone": "987-654-3210",
        "email": "bob@gmail.com"
    },
    {
        "name": "Charlie",
        "phone": "555-555-5555",
        "email": "charlie@gmail.com"
    },
    {
        "name": "David",
        "phone": "111-222-3333",
        "email": "david@gmail.com"
    },
    {   
        "name": "Eve",
        "phone": "444-444-4444",    
        "email": "eve@gmail.com"
    }
]

def find_contact(name):
    for contact in contacts:
        if contact["name"].lower() == name.lower():
            return contact
    return None

name_to_search = input("Enter the name of the contact you want to search for: ")
result = find_contact(name_to_search)
if result:
    print(f"Contact found: Name: {result['name']}, Phone: {result['phone']}, Email: {result['email']}")
else:
    print("Contact not found.")