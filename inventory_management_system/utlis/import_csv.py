import csv
from tkinter import filedialog, messagebox
from ..db.models import add_item, update_item, fetch_all_items

def import_csv_to_inventory(refresh_inventory):
    """
    Allows the user to select a CSV file and updates the inventory based on the file's content.
    """
    # Open a file dialog to select a CSV file
    file_path = filedialog.askopenfilename(
        title="Select Inventory CSV File",
        filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
    )

    if not file_path:
        return  # User canceled the file selection

    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            required_columns = {"item_name", "quantity", "supplier", "reorder_level"}

            # Check if required columns are present
            if not required_columns.issubset(reader.fieldnames):
                messagebox.showerror(
                    "Invalid CSV",
                    f"The CSV file must contain the following columns: {', '.join(required_columns)}"
                )
                return

            # Process each row in the CSV
            for row in reader:
                item_name = row["item_name"]
                quantity = int(row["quantity"])
                supplier = row["supplier"]
                reorder_level = int(row["reorder_level"])

                # Check if the item already exists
                items = fetch_all_items()
                existing_item = next((item for item in items if item[1] == item_name), None)

                if existing_item:
                    # Update the item if it exists
                    update_item(existing_item[0], quantity=quantity, reorder_level=reorder_level)
                else:
                    # Add the item if it doesn't exist
                    add_item(item_name, quantity, supplier, reorder_level)
        refresh_inventory()
        messagebox.showinfo("Success", "Inventory updated successfully from CSV file!")
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found. Please select a valid CSV file.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while importing CSV: {e}")
