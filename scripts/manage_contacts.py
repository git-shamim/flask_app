# scripts/manage_contacts.py

import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from index import app
from models import db, Contact


def list_contacts():
    contacts = Contact.query.all()
    if not contacts:
        print("📭 No contact entries found.")
        return []

    print("\n📋 Current Contact Entries:")
    for c in contacts:
        print(f"[{c.id}] {c.name} | {c.email} | {c.message[:50]}")
    return contacts


def delete_all():
    confirm = input("⚠️  Are you sure you want to delete ALL contact entries? (yes/no): ").strip().lower()
    if confirm == 'yes':
        Contact.query.delete()
        db.session.commit()
        print("✅ All contact entries deleted.")
    else:
        print("❎ Deletion cancelled.")


def delete_by_email_or_id():
    choice = input("Delete by (1) ID or (2) Email? Enter 1 or 2: ").strip()

    if choice == '1':
        try:
            id_to_delete = int(input("Enter ID to delete: ").strip())
            contact = Contact.query.get(id_to_delete)
        except ValueError:
            print("❌ Invalid ID.")
            return
    elif choice == '2':
        email = input("Enter Email to delete: ").strip()
        contact = Contact.query.filter_by(email=email).first()
    else:
        print("❌ Invalid choice.")
        return

    if contact:
        print(f"Found: {contact.name} | {contact.email}")
        confirm = input("Delete this contact? (yes/no): ").strip().lower()
        if confirm == 'yes':
            db.session.delete(contact)
            db.session.commit()
            print("✅ Contact deleted.")
        else:
            print("❎ Deletion cancelled.")
    else:
        print("❌ Contact not found.")


def main():
    with app.app_context():
        contacts = list_contacts()
        if not contacts:
            print("👋 Exiting.")
            return

        print("\nOptions:")
        print("1. Delete ALL contacts")
        print("2. Delete a contact by ID or email")
        print("3. Exit")

        option = input("Choose an option (1/2/3): ").strip()

        if option == '1':
            delete_all()
        elif option == '2':
            delete_by_email_or_id()
        else:
            print("👋 Exiting.")


if __name__ == "__main__":
    main()
