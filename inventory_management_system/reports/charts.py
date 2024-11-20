import tkinter as tk
from tkinter import Toplevel
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ..db.models import fetch_all_items

def show_inventory_chart(root):
    """
    Displays a bar chart of inventory item quantities in a new window with a Refresh Chart button.

    Args:
        root: The parent Tkinter window.
    """
    def refresh_chart():
        """
        Refreshes the chart with the latest inventory data.
        """
        # Clear the current chart
        ax.clear()

        # Fetch updated inventory data
        updated_items = fetch_all_items()
        item_names = [item[1] for item in updated_items]
        quantities = [item[2] for item in updated_items]
        reorder_levels = [item[4] for item in updated_items]

        # Redraw the bar chart with updated data
        bars = ax.bar(item_names, quantities, color="skyblue", label="Current Quantity")

        # Add reorder level lines and annotations
        for idx, reorder_level in enumerate(reorder_levels):
            ax.axhline(y=reorder_level, color='red', linestyle='--', alpha=0.5, xmax=(idx + 0.5) / len(item_names))
            ax.text(
                idx, reorder_level + 1, f"Reorder: {reorder_level}",
                color="red", fontsize=9, ha="center", va="bottom"
            )

        # Add data labels on top of bars
        for bar, quantity in zip(bars, quantities):
            ax.text(
                bar.get_x() + bar.get_width() / 2, bar.get_height(),
                str(quantity), ha='center', va='bottom', fontsize=10, color="black"
            )

        # Annotate low-stock items
        for idx, (quantity, reorder_level) in enumerate(zip(quantities, reorder_levels)):
            if quantity < reorder_level:
                ax.text(
                    idx, quantity + 1, "Low Stock!", color="orange",
                    fontsize=10, ha="center", va="bottom", fontweight="bold"
                )

        # Enhance chart appearance
        ax.set_title("Inventory Quantities", fontsize=18, fontweight='bold', pad=15)
        ax.set_xlabel("Items", fontsize=14, labelpad=10)
        ax.set_ylabel("Quantity", fontsize=14, labelpad=10)
        ax.tick_params(axis="x", rotation=45)
        ax.legend(loc="upper right", fontsize=12)

        # Redraw the canvas
        canvas.draw()

    # Fetch initial inventory data
    items = fetch_all_items()
    item_names = [item[1] for item in items]
    quantities = [item[2] for item in items]
    reorder_levels = [item[4] for item in items]

    # Create a new window for the chart
    chart_window = Toplevel(root)
    chart_window.title("Inventory Chart")
    chart_window.geometry("900x700")

    # Create a Matplotlib figure
    fig = Figure(figsize=(9, 7), dpi=100)
    ax = fig.add_subplot(111)

    # Draw the initial chart
    bars = ax.bar(item_names, quantities, color="skyblue", label="Current Quantity")

    # Add reorder level lines and annotations
    for idx, reorder_level in enumerate(reorder_levels):
        ax.axhline(y=reorder_level, color='red', linestyle='--', alpha=0.5, xmax=(idx + 0.5) / len(item_names))
        ax.text(
            idx, reorder_level + 1, f"Reorder: {reorder_level}",
            color="red", fontsize=9, ha="center", va="bottom"
        )

    # Add data labels on top of bars
    for bar, quantity in zip(bars, quantities):
        ax.text(
            bar.get_x() + bar.get_width() / 2, bar.get_height(),
            str(quantity), ha='center', va='bottom', fontsize=10, color="black"
        )

    # Annotate low-stock items
    for idx, (quantity, reorder_level) in enumerate(zip(quantities, reorder_levels)):
        if quantity < reorder_level:
            ax.text(
                idx, quantity + 1, "Low Stock!", color="orange",
                fontsize=10, ha="center", va="bottom", fontweight="bold"
            )

    # Enhance chart appearance
    ax.set_title("Inventory Quantities", fontsize=18, fontweight='bold', pad=15)
    ax.set_xlabel("Items", fontsize=14, labelpad=10)
    ax.set_ylabel("Quantity", fontsize=14, labelpad=10)
    ax.tick_params(axis="x", rotation=45)
    ax.legend(loc="upper right", fontsize=12)

    # Embed the Matplotlib figure in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Add a Refresh Chart button
    tk.Button(chart_window, text="Refresh Chart", command=refresh_chart).pack(pady=10)


def show_pie_chart(root):
    """
    Displays a pie chart of inventory item quantities with a Refresh Chart button.

    Args:
        root: The parent Tkinter window.
    """
    def refresh_chart():
        """
        Refreshes the pie chart with the latest inventory data.
        """
        # Clear the current chart
        ax.clear()

        # Fetch updated inventory data
        updated_items = fetch_all_items()
        item_names = [item[1] for item in updated_items]
        quantities = [item[2] for item in updated_items]

        # Redraw the pie chart with updated data
        ax.pie(quantities, labels=item_names, autopct='%1.1f%%', startangle=90)
        ax.set_title("Inventory Distribution", fontsize=16)

        # Redraw the canvas
        canvas.draw()

    # Fetch initial inventory data
    items = fetch_all_items()
    item_names = [item[1] for item in items]
    quantities = [item[2] for item in items]

    # Create a new window for the pie chart
    chart_window = Toplevel(root)
    chart_window.title("Inventory Pie Chart")
    chart_window.geometry("800x600")

    # Create a Matplotlib figure
    fig = Figure(figsize=(8, 6), dpi=100)
    ax = fig.add_subplot(111)

    # Draw the initial pie chart
    ax.pie(quantities, labels=item_names, autopct='%1.1f%%', startangle=90)
    ax.set_title("Inventory Distribution", fontsize=16)

    # Embed the Matplotlib figure in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Add a Refresh Chart button
    tk.Button(chart_window, text="Refresh Chart", command=refresh_chart).pack(pady=10)
