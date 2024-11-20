# Inventory Management System

This Python-based Inventory Management System (IMS) helps to automate inventory tracking, improve accuracy, and provide real-time status.

## Features
- Add, update, and delete items with details (name, ID, quantity, supplier, reorder level)
- Real-time inventory tracking
- Low stock alerts
- Inventory search and report generation

## Directory Structure
- `db/`: Database setup and data models
- `gui/`: Tkinter-based GUI for the application
- `reports/`: Report generation scripts
- `utils/`: Utility functions like alerts
- `config.py`: Configuration file for settings

## Requirements
- Python 3.x
- Tkinter
- pandas
- sqlite3

## Setup
1. Install dependencies:
    ```bash
    pip install pandas
    ```
2. Run the application:
    ```bash
    python main.py
    ```
