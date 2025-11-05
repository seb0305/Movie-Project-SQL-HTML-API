"""
User management for Movie Project.
Handles creation, listing, and selection of active user profiles.
"""

from sqlalchemy import create_engine, text

DB_URL = "sqlite:///data/movies.db"
engine = create_engine(DB_URL, echo=False)

def list_users():
    """
    Retrieve all users.

    Returns:
        list of (id, username) tuples.
    """
    with engine.connect() as connection:
        result = connection.execute(text("SELECT id, username FROM users ORDER BY username"))
        return result.fetchall()

def add_user(username):
    """
    Create a new user.

    Args:
        username (str): Desired unique username.
    Returns:
        bool: True if added successfully, False if username exists or error.
    """
    with engine.connect() as connection:
        try:
            connection.execute(
                text("INSERT INTO users (username) VALUES (:username)"),
                {"username": username}
            )
            connection.commit()
            return True
        except Exception:
            return False

def select_user():
    """
    Present user selection menu for choosing or creating a user.

    Returns:
        (user_id, username) tuple of selected or created user.
    """
    users = list_users()
    print("Select a user:")
    for idx, (uid, name) in enumerate(users, 1):
        print(f"{idx}. {name}")
    print(f"{len(users)+1}. Create new user")

    while True:
        choice = input("Enter choice: ").strip()
        if choice.isdigit():
            choice_i = int(choice)
            if 1 <= choice_i <= len(users):
                return users[choice_i - 1]
            elif choice_i == len(users) + 1:
                username = input("Enter new username: ").strip()
                if username:
                    if add_user(username):
                        print(f"User '{username}' created.")
                        return select_user()
                    else:
                        print("Username already exists or error occurred.")
                else:
                    print("Username cannot be empty.")
            else:
                print("Invalid choice, try again.")
        else:
            print("Please enter a number.")
