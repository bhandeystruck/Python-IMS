"""
inventory_gui.py

This module provides GUI functionalities for managing inventory items in a Tkinter-based application.
The following operations are supported:
1. Adding a new item to the inventory.
2. Viewing all items in the inventory.
3. Updating an existing item in the inventory.
4. Deleting an item from the inventory.

Each operation opens a dedicated GUI window to interact with the user, enabling easy management of inventory data.

Dependencies:
- tkinter: For GUI components and user interaction.
- tkinter.messagebox: For displaying alerts and messages.
- inventory_management_system.db.models: Contains database interaction functions, including:
    - add_item: Adds a new item to the inventory.
    - update_item: Updates an existing item in the inventory.
    - delete_item: Deletes an item from the inventory.
    - fetch_all_items: Fetches all items from the inventory.

Functions:
- add_item_gui(root, refresh_inventory): Opens a window to add a new inventory item.
- view_inventory_gui(root): Opens a window to display all inventory items.
- update_item_gui(root, refresh_inventory): Opens a window to update an inventory item.
- delete_item_gui(root, refresh_inventory): Opens a window to delete an inventory item.
"""
import tkinter as tk
from tkinter import messagebox
from inventory_management_system.db.models import add_item, update_item, delete_item, fetch_all_items

def add_item_gui(root, refresh_inventory):
    """
    Opens a GUI window to add a new item to the inventory.

    Args:
        root: The parent Tkinter window.
        refresh_inventory: A function to refresh the inventory display after adding an item.
    """
    def submit():
        """
        Handles the submission of the new item.
        - Retrieves input values from the GUI fields.
        - Calls the `add_item` function to add the item to the database.
        - Displays a success message.
        - Refreshes the inventory display.
        - Closes the Add Item window.
        """
        # Retrieve values from the input fields
        name = entry_name.get()
        quantity = int(entry_quantity.get())
        supplier = entry_supplier.get()
        reorder_level = int(entry_reorder_level.get())

        # Add the new item to the inventory
        add_item(name, quantity, supplier, reorder_level)
        # Show success message
        messagebox.showinfo("Success", "Item added successfully")
        # Refresh the inventory table in the main GUI
        refresh_inventory()
        # Close the Add Item window  
        window.destroy()

    # Create a new window for adding an item
    window = tk.Toplevel(root)
    window.title("Add Item")
    # Create and pack the label and entry for the Item Name field
    tk.Label(window, text="Item Name").pack()
    entry_name = tk.Entry(window)
    entry_name.pack()
    # Create and pack the label and entry for the Quantity field
    tk.Label(window, text="Quantity").pack()
    entry_quantity = tk.Entry(window)
    entry_quantity.pack()
    # Create and pack the label and entry for the Supplier field
    tk.Label(window, text="Supplier").pack()
    entry_supplier = tk.Entry(window)
    entry_supplier.pack()
    # Create and pack the label and entry for the Reorder Level field
    tk.Label(window, text="Reorder Level").pack()
    entry_reorder_level = tk.Entry(window)
    entry_reorder_level.pack()
    # Create and pack the Submit button
    # When clicked, it triggers the `submit` function
    tk.Button(window, text="Submit", command=submit).pack()

def view_inventory_gui(root):
    """
    Opens a GUI window to display all items in the inventory.

    Args:
        root: The parent Tkinter window.
    """
    # Create a new window to display the inventory
    inventory_window = tk.Toplevel(root)
    # Set the title of the window
    inventory_window.title("Inventory")
    # Fetch all inventory items from the database   
    items = fetch_all_items()
    # Loop through each item and display its details in the window
    for item in items:
        # Each item is displayed as a label with its details: ID, Name, Quantity, Supplier, and Reorder Level
        tk.Label(inventory_window, text=f"ID: {item[0]}, Name: {item[1]}, Quantity: {item[2]}, Supplier: {item[3]}, Reorder Level: {item[4]}").pack()

def update_item_gui(root,refresh_inventory):
    """
    Opens a GUI window to update an existing item in the inventory.

    Args:
        root: The parent Tkinter window.
        refresh_inventory: A function to refresh the inventory display after updating an item.
    """
    def submit():
        """
        Handles the submission of the updated item details.
        - Retrieves input values from the GUI fields.
        - Calls the `update_item` function to update the item in the database.
        - Displays a success message.
        - Refreshes the inventory display.
        - Closes the Update Item window.
        """
         # Get the item ID from the input field
        item_id = int(entry_id.get())

        # Retrieve new quantity if provided, otherwise set to None
        quantity = int(entry_quantity.get()) if entry_quantity.get() else None

        # Retrieve new reorder level if provided, otherwise set to None
        reorder_level = int(entry_reorder_level.get()) if entry_reorder_level.get() else None

        # Update the item in the database with the new values
        update_item(item_id, quantity, reorder_level)

        # Show a success message to the user
        messagebox.showinfo("Success", "Item updated successfully")

        # Refresh the inventory table in the main GUI
        refresh_inventory()

        # Close the Update Item window
        window.destroy()

    # Create a new window for updating an item
    window = tk.Toplevel(root)
    window.title("Update Item")

    # Create and pack the label and entry for the Item ID field
    tk.Label(window, text="Item ID").pack()
    entry_id = tk.Entry(window)
    entry_id.pack()

    # Create and pack the label and entry for the New Quantity field
    tk.Label(window, text="New Quantity (Leave blank to skip)").pack()
    entry_quantity = tk.Entry(window)
    entry_quantity.pack()

    # Create and pack the label and entry for the New Reorder Level field
    tk.Label(window, text="New Reorder Level (Leave blank to skip)").pack()
    entry_reorder_level = tk.Entry(window)
    entry_reorder_level.pack()

    # Create and pack the Submit button
    # When clicked, it triggers the `submit` function
    tk.Button(window, text="Submit", command=submit).pack()

def delete_item_gui(root, refresh_inventory):
    """
    Opens a GUI window to delete an item from the inventory.

    Args:
        root: The parent Tkinter window.
        refresh_inventory: A function to refresh the inventory display after deleting an item.
    """
    def submit():
        """
        Handles the submission of the delete operation.
        - Retrieves the item ID from the input field.
        - Calls the `delete_item` function to remove the item from the database.
        - Displays a success message.
        - Refreshes the inventory display.
        - Closes the Delete Item window.
        """
        # Get the item ID from the input field
        item_id = int(entry_id.get())

        # Delete the specified item from the database
        delete_item(item_id)

        # Show a success message to confirm deletion
        messagebox.showinfo("Success", "Item deleted successfully")

        # Refresh the inventory table in the main GUI
        refresh_inventory()

        # Close the Delete Item window
        window.destroy()

    # Create a new window for deleting an item
    window = tk.Toplevel(root)
    window.title("Delete Item")  # Set the window title

    # Create and pack the label and entry for the Item ID field
    tk.Label(window, text="Item ID").pack()
    entry_id = tk.Entry(window)
    entry_id.pack()

    # Create and pack the Delete button
    # When clicked, it triggers the `submit` function
    tk.Button(window, text="Delete", command=submit).pack()
