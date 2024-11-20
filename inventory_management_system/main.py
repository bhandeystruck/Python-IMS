import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from inventory_management_system.db.database import initialize_tables
from inventory_management_system.db.models import fetch_all_items, fetch_low_stock_items, delete_all_items
from inventory_management_system.reports.charts import show_inventory_chart,show_pie_chart
from inventory_management_system.gui.inventory_gui import (
    add_item_gui,
    update_item_gui,
    delete_item_gui,
)
from inventory_management_system.gui.login_gui import login_gui
from inventory_management_system.utlis.import_csv import import_csv_to_inventory 

def main():
    # Initialize the database tables
    initialize_tables()

    def start_main_app():
        """Launch the main application interface after login."""
        # Destroy the login window and create the main application window
        root.destroy()

        # Create a new window for the main application
        main_app = tk.Tk()
        main_app.title("Inventory Management System")
        main_app.geometry("800x600")

        """--------------------FUNCTIONS-START--------------------"""

        def logout():
            """Logout and return to the login screen."""
            main_app.destroy()  # Destroy the main application window
            main()  # Reopen the login screen

        def refresh_inventory():
            """Fetch and display inventory data."""
            for row in tree.get_children():
                tree.delete(row)  # Clear the existing data in the table

            # Fetch all items from the database
            inventory_items = fetch_all_items()
            for item in inventory_items:
                item_id, item_name, quantity, supplier, reorder_level = item
                if quantity < reorder_level:
                    # Highlight low-stock items in yellow
                    tree.insert("", "end", values=(item_id, item_name, quantity, supplier, reorder_level), tags=("low_stock",))
                else:
                    tree.insert("", "end", values=(item_id, item_name, quantity, supplier, reorder_level))

        def show_low_stock_alerts():
            """Display low stock alerts."""
            low_stock_items = fetch_low_stock_items()
            if low_stock_items:
                alert_message = "Low Stock Items:\n\n"
                for item in low_stock_items:
                    alert_message += f"- {item[0]}: {item[1]} units (Reorder Level: {item[2]})\n"
                messagebox.showwarning("Low Stock Alert", alert_message)
            else:
                messagebox.showinfo("Low Stock Alert", "All items are sufficiently stocked.")

        def delete_all():
            confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete all items? This action cannot be undone.")
            if confirm:
                delete_all_items()
                refresh_inventory()
        """--------------------FUNCTIONS-END--------------------"""
        
        """--------------------LAYOUT-START--------------------"""

        # Add a Logout button
        tk.Button(main_app, text="Logout", command=logout).pack(anchor="ne", padx=10, pady=10)
        # Add Low Stock Alert button
        tk.Button(main_app, text="Check Low Stock", command=show_low_stock_alerts).pack(pady=20)
        # Button to show the inventory chart
        tk.Button(main_app, text="Show Inventory Chart", command=lambda: show_inventory_chart(main_app)).pack(pady=20)
        # Button to show pie chart
        tk.Button(main_app, text="Show Pie Chart", command=lambda: show_pie_chart(main_app)).pack(pady=20)
        # Main app interface buttons
        button_frame = tk.Frame(main_app)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Add Item", command=lambda: add_item_gui(main_app, refresh_inventory)).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Update Item", command=lambda: update_item_gui(main_app, refresh_inventory)).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Delete Item", command=lambda: delete_item_gui(main_app, refresh_inventory)).grid(row=0, column=2, padx=5)
        tk.Button(button_frame,text="Refresh Inventory", command=refresh_inventory).grid(row=0, column=3, padx=5)
        tk.Button(button_frame, text="Import CSV to Inventory", command=lambda:import_csv_to_inventory(refresh_inventory), bg="green", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=4, padx=5)
        tk.Button(button_frame, text="Delete All Items", command=delete_all, bg="red", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=5, padx=5)

        # Create a Treeview widget to display inventory data
        columns = ("Item ID", "Item Name", "Quantity", "Supplier", "Reorder Level")
        tree = ttk.Treeview(main_app, columns=columns, show="headings", height=15)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Define column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Add tag for low-stock styling
        tree.tag_configure("low_stock", background="yellow")
        """--------------------LAYOUT-END--------------------"""

        # Initial refresh to display current inventory data
        refresh_inventory()

        main_app.mainloop()

    # Create the root login window
    root = tk.Tk()
    root.title("Login Screen")
    root.geometry("400x300")

    # Start with the login screen
    login_gui(root, start_main_app)

    root.mainloop()

if __name__ == "__main__":
    main()
