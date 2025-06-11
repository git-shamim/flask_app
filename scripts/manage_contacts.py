#!/usr/bin/env python3
"""
scripts/manage_contacts.py

CLI to list and manage Contact entries in the configured database
(either local SQLite when USE_SQLITE=true, or Cloud SQL in GCP).
"""

import os
import sys
import logging

# Add project root to sys.path so we can import index and models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from index import app
from models import db, Contact

# Configure logging
logging.basicConfig(level=logging.INFO)


def list_contacts():
    """Fetch and display all contacts."""
    contacts = Contact.query.all()
    if not contacts:
        print("No contact entries found.")
        return []

    print("\nCurrent Contact Entries:")
    for c in contacts:
        snippet = c.message[:50] + ("..." if len(c.message) > 50 else "")
        print(f"[{c.id}] {c.name} | {c.email} | {snippet}")
    return contacts


def delete_all():
    """Delete all contact entries after confirmation."""
    confirm = input("Are you sure you want to delete ALL contact entries? (yes/no): ").strip().lower()
    if confirm == "yes":
        Contact.query.delete()
        db.session.commit()
        print("All contact entries deleted.")
    else:
        print("Deletion cancelled.")


def delete_by_email_or_id():
    """Delete a single contact by ID or email."""
    choice = input("Delete by (1) ID or (2) Email? Enter 1 or 2: ").strip()

    if choice == "1":
        try:
            id_to_delete = int(input("Enter ID to delete: ").strip())
            contact = Contact.query.get(id_to_delete)
        except ValueError:
            print("Invalid ID.")
            return
    elif choice == "2":
        email = input("Enter Email to delete: ").strip()
        contact = Contact.query.filter_by(email=email).first()
    else:
        print("Invalid choice.")
        return

    if contact:
        print(f"Found: {contact.name} | {contact.email}")
        confirm = input("Delete this contact? (yes/no): ").strip().lower()
        if confirm == "yes":
            db.session.delete(contact)
            db.session.commit()
            print("Contact deleted.")
        else:
            print("Deletion cancelled.")
    else:
        print("Contact not found.")


def main():
    """Entry point: show DB connection and management menu."""
    # Log which database is in use
    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "<none>")
    logging.info(f"Connected to database: {db_uri}\n")

    with app.app_context():
        # Ensure tables exist (SQLite locally or Cloud SQL in GCP)
        db.create_all()

        contacts = list_contacts()
        if not contacts:
            print("Exiting.")
            return

        print("\nOptions:")
        print("1. Delete ALL contacts")
        print("2. Delete a contact by ID or email")
        print("3. Exit")

        option = input("Choose an option (1/2/3): ").strip()
        if option == "1":
            delete_all()
        elif option == "2":
            delete_by_email_or_id()
        else:
            print("Exiting.")


if __name__ == "__main__":
    main()
