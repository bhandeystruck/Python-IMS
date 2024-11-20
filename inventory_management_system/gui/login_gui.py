import tkinter as tk
from tkinter import messagebox
from ..db.models import create_user, authenticate_user

def login_gui(root, on_login_success):
    """
    Displays the Login GUI to authenticate users.

    Args:
        root: The parent Tkinter window.
        on_login_success: A callback function to proceed to the main application upon successful login.
    """
    def attempt_login():
        """
        Handles the login attempt.
        - Retrieves username and password from the input fields.
        - Calls `authenticate_user` to verify credentials.
        - Displays a success message and proceeds to the main app on success.
        - Displays an error message on failure.
        """
        username = entry_username.get()
        password = entry_password.get()

        if authenticate_user(username, password):
            messagebox.showinfo("Login Success", f"Welcome, {username}!")
            on_login_success()  # Proceed to the main app
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def open_signup():
        """
        Opens the Signup GUI for user registration.
        """
        signup_gui(root)

    # Clear the existing widgets (if returning to login screen)
    for widget in root.winfo_children():
        widget.destroy()

    # Create and display the Login form
    tk.Label(root, text="Login", font=("Arial", 16, "bold")).pack(pady=10)

    # Username input field
    tk.Label(root, text="Username").pack()
    entry_username = tk.Entry(root)
    entry_username.pack()

    # Password input field
    tk.Label(root, text="Password").pack()
    entry_password = tk.Entry(root, show="*")
    entry_password.pack()

    # Login and Sign Up buttons
    tk.Button(root, text="Login", command=attempt_login).pack(pady=10)
    tk.Button(root, text="Sign Up", command=open_signup).pack()


def signup_gui(root):
    """
    Displays the Signup GUI to register new users.

    Args:
        root: The parent Tkinter window.
    """
    def attempt_signup():
        """
        Handles the signup attempt.
        - Retrieves username, password, and confirmation password from the input fields.
        - Validates password and confirmation match.
        - Calls `create_user` to register the new user.
        - Displays success message on successful registration.
        - Displays error message if username exists or validation fails.
        """
        username = entry_username.get()
        password = entry_password.get()
        confirm_password = entry_confirm_password.get()

        if password != confirm_password:
            # Display an error if passwords do not match
            messagebox.showerror("Signup Failed", "Passwords do not match.")
            return

        if create_user(username, password):
            # Display success message and close the signup window
            messagebox.showinfo("Signup Success", "Account created successfully! Please log in.")
            signup_window.destroy()
        else:
            # Display an error if the username already exists
            messagebox.showerror("Signup Failed", "Username already exists.")

    # Create a new window for the Signup form
    signup_window = tk.Toplevel(root)
    signup_window.title("Sign Up")

    # Username input field
    tk.Label(signup_window, text="Username").pack()
    entry_username = tk.Entry(signup_window)
    entry_username.pack()

    # Password input field
    tk.Label(signup_window, text="Password").pack()
    entry_password = tk.Entry(signup_window, show="*")
    entry_password.pack()

    # Confirm Password input field
    tk.Label(signup_window, text="Confirm Password").pack()
    entry_confirm_password = tk.Entry(signup_window, show="*")
    entry_confirm_password.pack()

    # Sign Up button
    tk.Button(signup_window, text="Sign Up", command=attempt_signup).pack(pady=10)
