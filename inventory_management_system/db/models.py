"""
models.py

This module provides functions for database operations related to the Inventory Management System.
It includes functionalities for managing items, transactions, and user authentication.

Dependencies:
- sqlite3: For database interactions.
- bcrypt: For secure password hashing and verification.
- datetime: For handling timestamps in transactions.
- logging: For recording events and errors.

Functions:
- add_item(item_name, quantity, supplier, reorder_level): Adds a new item to the inventory.
- update_item(item_id, quantity=None, reorder_level=None): Updates the quantity or reorder level of an existing item.
- delete_item(item_id): Deletes an item from the inventory.
- log_transaction(item_id, transaction_type, quantity): Logs a transaction (add, update, delete) for an item.
- fetch_all_items(): Retrieves all items from the inventory.
- create_user(username, password): Creates a new user with a hashed password.
- authenticate_user(username, password): Authenticates a user by verifying their password.
- fetch_low_stock_items(): Retrieves items with quantities below their reorder levels.
"""

from .database import get_connection
import bcrypt
from datetime import datetime
import sqlite3
import logging
from tkinter import messagebox

# Establish a database connection
conn = get_connection()

def add_item(item_name, quantity, supplier, reorder_level):
    """
    Adds a new item to the inventory.

    Args:
        item_name (str): The name of the item.
        quantity (int): The quantity of the item.
        supplier (str): The supplier of the item.
        reorder_level (int): The reorder threshold for the item.

    Raises:
        sqlite3.IntegrityError: If there is a database integrity error.
        sqlite3.Error: If a general database error occurs.
    """
    try:
        c = conn.cursor()
        c.execute(
            "INSERT INTO items (item_name, quantity, supplier, reorder_level) VALUES (?, ?, ?, ?)",
            (item_name, quantity, supplier, reorder_level)
        )
        conn.commit()
        logging.info(f"{quantity} {item_name}'s added successfully.")
    except sqlite3.IntegrityError as e:
        logging.error(f"Integrity error while adding item: {e}")
        raise
    except sqlite3.Error as e:
        logging.error(f"Database error while adding item: {e}")
        raise

def update_item(item_id, quantity=None, reorder_level=None):
    """
    Updates an existing item in the inventory.

    Args:
        item_id (int): The ID of the item to update.
        quantity (int, optional): The new quantity of the item. Defaults to None.
        reorder_level (int, optional): The new reorder level of the item. Defaults to None.
    """
    c = conn.cursor()
    if quantity is not None:
        c.execute("UPDATE items SET quantity = ? WHERE item_id = ?", (quantity, item_id))
        log_transaction(item_id, 'update', quantity)
    if reorder_level is not None:
        c.execute("UPDATE items SET reorder_level = ? WHERE item_id = ?", (reorder_level, item_id))
    conn.commit()

def delete_item(item_id):
    """
    Deletes an item from the inventory.

    Args:
        item_id (int): The ID of the item to delete.
    """
    c = conn.cursor()
    c.execute("DELETE FROM items WHERE item_id = ?", (item_id,))
    conn.commit()

def log_transaction(item_id, transaction_type, quantity):
    """
    Logs a transaction in the database.

    Args:
        item_id (int): The ID of the item involved in the transaction.
        transaction_type (str): The type of transaction ('add', 'update', or 'delete').
        quantity (int): The quantity involved in the transaction.
    """
    c = conn.cursor()
    c.execute(
        "INSERT INTO transactions (item_id, transaction_type, quantity) VALUES (?, ?, ?)",
        (item_id, transaction_type, quantity)
    )
    conn.commit()

def fetch_all_items():
    """
    Retrieves all items from the inventory.

    Returns:
        list: A list of tuples containing item details.
    """
    c = conn.cursor()
    c.execute("SELECT * FROM items")
    return c.fetchall()

def create_user(username, password):
    """
    Creates a new user with a hashed password.

    Args:
        username (str): The username of the new user.
        password (str): The plaintext password of the new user.

    Returns:
        bool: True if the user was created successfully, False otherwise.
    """
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    with get_connection() as conn:
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

def authenticate_user(username, password):
    """
    Authenticates a user by verifying their password.

    Args:
        username (str): The username of the user.
        password (str): The plaintext password provided for authentication.

    Returns:
        bool: True if authentication is successful, False otherwise.
    """
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        result = c.fetchone()
        if result is None:
            return False  # User does not exist
        stored_password_hash = result[0]
        return bcrypt.checkpw(password.encode('utf-8'), stored_password_hash)

def fetch_low_stock_items():
    """
    Retrieves items with quantities below their reorder levels.

    Returns:
        list: A list of tuples containing low-stock item details.
    """
    c = conn.cursor()
    c.execute("SELECT * FROM items WHERE quantity < reorder_level")
    return c.fetchall()


def delete_all_items():
    try:
        with get_connection() as conn:
                c = conn.cursor()
                c.execute("DELETE FROM items")  # Delete all records from the items table
                conn.commit()
                messagebox.showinfo("Success", "All items have been deleted successfully!")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Failed to delete items: {e}")