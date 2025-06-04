import sys
import json
from textual.app import App
from textual.widgets import DataTable
from rich.text import Text

# Load from JSON file
def load_contacts():
    try:
        with open("contacts.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save to JSON file
def save_contacts(contacts):
    with open("contacts.json", "w") as file:
        json.dump(contacts, file, indent=4)

# Add contact
def add_contact(contact_str):
    contacts = load_contacts()
    fields = contact_str.split(",")
    if len(fields) < 4:
        fields.extend([""] * (4 - len(fields)))  # empty strings for missing fields
    name, birthday, email, phone = fields[:4]
    contacts.append({
        "name": name.strip(),
        "birthday": birthday.strip(),
        "email": email.strip(),
        "phone": phone.strip()
    })
    save_contacts(contacts)
    print("Contact added successfully.")

# Delete contact
def delete_contact(search_term):
    contacts = load_contacts()
    matches = [c for c in contacts if search_term.lower() in json.dumps(c).lower()]
    if not matches:
        print("No matching contacts found.")
        return

    print("Matching contacts:")
    for i, contact in enumerate(matches, start=1):
        print(f"{i}: {contact}")

    try:
        to_delete = int(input("Enter the number of the contact to delete (or enter 0 to abort): ")) - 1
        if 0 <= to_delete < len(matches):
            contacts.remove(matches[to_delete])
            save_contacts(contacts)
            print("Contact deleted successfully.")
        else:
            if to_delete < 0:
                print("Aborting delete operation")
            else:
                print("Invalid selection.")
    except ValueError:
        print("Invalid input.")

# Edit contact
def edit_contact(search_term):
    contacts = load_contacts()
    matches = [c for c in contacts if search_term.lower() in json.dumps(c).lower()]
    if not matches:
        print("No matching contacts found.")
        return

    print("Matching contacts:")
    for i, contact in enumerate(matches, start=1):
        print(f"\n{i}:\n" + "\n".join([f"\033[1;97m{key}\033[0m: {value}" for key, value in contact.items()]))


    try:
        to_edit = int(input("Enter the number of the contact to edit (or enter 0 to abort): ")) - 1
        if 0 <= to_edit < len(matches):
            print("Enter updated contact details in the format: Name, Birthday, Email, Phone. \nLeaving a value blank will keep it unchanged, but include all commas.")
            updated_str = input("Updated contact: ").strip()
            fields = updated_str.split(",")
            if len(fields) < 4:
                fields.extend([""] * (4 - len(fields)))
            name, birthday, email, phone = fields[:4]

            # Only update fields that are not blank
            if name.strip():
                matches[to_edit]["name"] = name.strip()
            if birthday.strip():
                matches[to_edit]["birthday"] = birthday.strip()
            if email.strip():
                matches[to_edit]["email"] = email.strip()
            if phone.strip():
                matches[to_edit]["phone"] = phone.strip()

            # Find the index in the original contact list and update it
            original_index = contacts.index(matches[to_edit])
            contacts[original_index] = matches[to_edit]
            save_contacts(contacts)
            print("Contact updated successfully.")
        else:
            if to_edit < 0:
                print("Aborting edit operation")
            else:
                print("Invalid selection.")
    except ValueError:
        print("Invalid input.")

# All contacts viewing
class ContactViewer(App):
    def compose(self):
        self.table = DataTable(zebra_stripes=True)
        self.table.add_columns("Name", "Birthday", "Email", "Phone")
        contacts = load_contacts()
        for contact in contacts:
            self.table.add_row(contact["name"], contact["birthday"], contact["email"], contact["phone"])
        yield self.table

# Searched contacts viewer
class SearchApp(App):
    def __init__(self, search_term):
        super().__init__()
        self.search_term = search_term

    def compose(self):
        contacts = load_contacts()
        results = [contact for contact in contacts if self.search_term.lower() in contact["name"].lower() or \
                   self.search_term.lower() in contact["email"].lower() or \
                   self.search_term.lower() in contact["phone"].lower()]
        table = DataTable(zebra_stripes=True)
        table.add_columns("Name", "Birthday", "Email", "Phone")

        for contact in results:
            table.add_row(contact["name"], contact["birthday"], contact["email"], contact["phone"])

        yield table

# Search contacts
def search(query):
    SearchApp(query).run()

def main():
    if len(sys.argv) < 2:
        print("Usage: main.py <add|delete|edit|view|help|search> [arguments]")
        return

    command = sys.argv[1].lower()

    if command == "add":
        if len(sys.argv) < 3:
            print("Usage: main.py add 'name,birthday,email,phone'")
            return
        add_contact(sys.argv[2])
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Usage: main.py delete '<search_term>'")
            return
        delete_contact(sys.argv[2])
    elif command == "edit":
        if len(sys.argv) < 3:
            print("Usage: main.py edit '<search_term>'")
            return
        edit_contact(sys.argv[2])
    elif command == "view":
        ContactViewer().run()
    elif command == "search":
        if len(sys.argv) < 3:
            print("Usage: main.py search '<search_term>'")
            return
        search(sys.argv[2])
    elif command == "help":
        print("\033[1;97mContacts App\033[0m")
        print("Usage: main.py <add|delete|edit|view|help|search> [arguments]")
        print("\n\033[1;97madd\033[0m: Add a contact. \n    \033[1;97mArgument\033[0m: comma-separated list of values like so: \"Name, Birthday, Email, Phone\". \n    Any item can be left blank but include all commas. Ex: \"John, ,650-123-4567,\"")
        print("\n\033[1;97mdelete\033[0m: Delete a contact. \n    \033[1;97mArgument\033[0m: String containing characters to search. A list of matching contacts will be shown. \n    Follow on-screen prompts to select one for deletion.")
        print("\n\033[1;97medit\033[0m: Edit a contact. \n    \033[1;97mArgument\033[0m: String containing characters to search. A list of matching contacts will be shown. \n    Follow on-screen prompts to edit the selected contact.")
        print("\n\033[1;97mview\033[0m: View a list of all contacts. \n    \033[1;97mArgument\033[0m: N/A")
        print("\n\033[1;97msearch\033[0m: Search for contacts. \n    \033[1;97mArgument\033[0m: A search term to filter contacts.\n    If you're only searching for one term, no need to use quotes.")
        print("\n\033[1;97mhelp\033[0m: View this message. \n    \033[1;97mArgument\033[0m: N/A")
    else:
        print("Unknown command. Use add, delete, edit, view, search, or help.")

if __name__ == "__main__":
    main()
