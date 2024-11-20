"""
This module handles database connection and initialization for the Inventory Management System.
It provides functions to establish a connection to the SQLite database and initialize required tables.

Functions:
- get_connection(): Establishes and returns a connection to the database.
- initialize_tables(): Ensures the necessary tables (items, transactions, users) exist in the database.

Dependencies:
- sqlite3: For SQLite database interactions.
- logging: For logging errors and events.

Tables Created:
1. items:
   - Stores inventory items with details like name, quantity, supplier, and reorder level.
2. transactions:
   - Logs transactions (add, update, delete) with timestamps and references to items.
3. users:
   - Stores user authentication data with hashed passwords.
"""

import sqlite3
import logging

def get_connection():
    """
    Establishes a connection to the SQLite database.

    Returns:
        sqlite3.Connection: A connection object to the SQLite database.

    Raises:
        sqlite3.Error: If a database connection cannot be established.
    """
    try:
        conn = sqlite3.connect("data/inventory.db", timeout=10)
        conn.execute("PRAGMA foreign_keys = 1")  # Ensure foreign key constraints are enforced
        return conn
    except sqlite3.Error as e:
        logging.error(f"Error connecting to database: {e}")
        raise

def initialize_tables():
    """
    Ensures that the required tables (items, transactions, users) are created in the database.
    If the tables do not exist, they will be created.
    """
    with get_connection() as conn:
        c = conn.cursor()
        # Create the items table
        c.execute('''CREATE TABLE IF NOT EXISTS items (
                        item_id INTEGER PRIMARY KEY,
                        item_name TEXT NOT NULL,
                        quantity INTEGER DEFAULT 0,
                        supplier TEXT,
                        reorder_level INTEGER DEFAULT 0
                    )''')
        c.execute("DROP TABLE IF EXISTS transactions")
         # Create the users table
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL
                    )''') 
        conn.commit()
