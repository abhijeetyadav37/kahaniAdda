import getpass
import sys

from app import app, db, Admin
from werkzeug.security import generate_password_hash

username = input("Admin username [abhijeet]: ").strip() or "abhijeet"
password = getpass.getpass("Enter new password (minimum 12 characters): ")
confirmation = getpass.getpass("Confirm new password: ")

if len(password) < 12:
    sys.exit("Error: Password must be at least 12 characters.")

if password != confirmation:
    sys.exit("Error: Passwords do not match.")

with app.app_context():
    admin = Admin.query.filter_by(username=username).first()

    if admin is None:
        sys.exit(
            "Admin not found. Check that DATABASE_URL points to Neon."
        )

    admin.password_hash = generate_password_hash(password)
    db.session.commit()

    print("Admin password updated successfully.")
