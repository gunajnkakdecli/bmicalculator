import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt 

# ==========================
# DATABASE SETUP
# ==========================

conn = sqlite3.connect("bmi_data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bmi_records(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    weight REAL,
    height REAL,
    bmi REAL,
    category TEXT,
    date TEXT
)
""")

conn.commit()

# ==========================
# BMI FUNCTIONS
# ==========================

def calculate_bmi():
    try:
        name = name_var.get().strip()

        if not name:
            messagebox.showerror("Error", "Please enter your name.")
            return

        weight = float(weight_var.get())
        height_cm = float(height_var.get())

        if weight <= 0 or weight > 500:
            messagebox.showerror(
                "Error",
                "Weight must be between 1 and 500 kg."
            )
            return

        if height_cm <= 0 or height_cm > 300:
            messagebox.showerror(
                "Error",
                "Height must be between 1 and 300 cm."
            )
            return

        # Convert cm to meters
        height_m = height_cm / 100

        bmi = weight / (height_m ** 2)

        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"

        result_label.config(
            text=f"BMI = {bmi:.2f}\nCategory = {category}",
            fg="blue"
        )

        save_record(
            name,
            weight,
            height_cm,
            bmi,
            category
        )

        load_records()

    except ValueError:
        messagebox.showerror(
            "Input Error",
            "Please enter valid numbers."
        )

# ==========================
# SAVE DATA
# ==========================

def save_record(name, weight, height, bmi, category):

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO bmi_records
    (name, weight, height, bmi, category, date)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (name, weight, height, bmi, category, date))

    conn.commit()

# ==========================
# LOAD RECORDS
# ==========================

def load_records():

    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("""
    SELECT * FROM bmi_records
    ORDER BY id DESC
    """)

    records = cursor.fetchall()

    for record in records:
        tree.insert("", tk.END, values=record)

# ==========================
# DELETE RECORD
# ==========================

def delete_record():

    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Select a record first."
        )
        return

    item = tree.item(selected[0])
    record_id = item["values"][0]

    cursor.execute(
        "DELETE FROM bmi_records WHERE id=?",
        (record_id,)
    )

    conn.commit()

    load_records()

    messagebox.showinfo(
        "Success",
        "Record deleted successfully."
    )

# ==========================
# CLEAR ALL RECORDS
# ==========================

def clear_all():

    confirm = messagebox.askyesno(
        "Confirm",
        "Delete ALL BMI records?"
    )

    if confirm:
        cursor.execute(
            "DELETE FROM bmi_records"
        )

        conn.commit()

        load_records()

        messagebox.showinfo(
            "Success",
            "All records deleted."
        )

# ==========================
# SHOW GRAPH
# ==========================

def show_graph():

    cursor.execute("""
    SELECT bmi, date
    FROM bmi_records
    ORDER BY id
    """)

    data = cursor.fetchall()

    if not data:
        messagebox.showwarning(
            "No Data",
            "No BMI records available."
        )
        return

    bmi_values = [row[0] for row in data]
    dates = [row[1][:10] for row in data]

    plt.figure(figsize=(10, 5))
    plt.plot(
        dates,
        bmi_values,
        marker="o"
    )

    plt.title("BMI Trend Analysis")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# ==========================
# SHOW STATISTICS
# ==========================

def show_statistics():

    cursor.execute(
        "SELECT bmi FROM bmi_records"
    )

    data = cursor.fetchall()

    if not data:
        messagebox.showwarning(
            "No Data",
            "No records available."
        )
        return

    bmi_values = [x[0] for x in data]

    avg_bmi = sum(bmi_values) / len(bmi_values)
    max_bmi = max(bmi_values)
    min_bmi = min(bmi_values)

    stats = (
        f"Total Records: {len(bmi_values)}\n\n"
        f"Average BMI: {avg_bmi:.2f}\n"
        f"Highest BMI: {max_bmi:.2f}\n"
        f"Lowest BMI: {min_bmi:.2f}"
    )

    messagebox.showinfo(
        "BMI Statistics",
        stats
    )

# ==========================
# GUI
# ==========================

root = tk.Tk()
root.title("Advanced BMI Calculator")
root.geometry("1000x650")
root.configure(bg="#F0F8FF")

# Variables

name_var = tk.StringVar()
weight_var = tk.StringVar()
height_var = tk.StringVar()

# Title

title = tk.Label(
    root,
    text="Advanced BMI Calculator",
    font=("Arial", 20, "bold"),
    bg="#F0F8FF",
    fg="darkblue"
)

title.pack(pady=10)

# Input Frame

input_frame = tk.Frame(
    root,
    bg="#F0F8FF"
)

input_frame.pack(pady=10)

# Name

tk.Label(
    input_frame,
    text="Name:",
    font=("Arial", 12),
    bg="#F0F8FF"
).grid(row=0, column=0, padx=10, pady=5)

tk.Entry(
    input_frame,
    textvariable=name_var,
    width=25
).grid(row=0, column=1)

# Weight

tk.Label(
    input_frame,
    text="Weight (kg):",
    font=("Arial", 12),
    bg="#F0F8FF"
).grid(row=1, column=0, padx=10, pady=5)

tk.Entry(
    input_frame,
    textvariable=weight_var,
    width=25
).grid(row=1, column=1)

# Height

tk.Label(
    input_frame,
    text="Height (cm):",
    font=("Arial", 12),
    bg="#F0F8FF"
).grid(row=2, column=0, padx=10, pady=5)

tk.Entry(
    input_frame,
    textvariable=height_var,
    width=25
).grid(row=2, column=1)

# Buttons

button_frame = tk.Frame(
    root,
    bg="#F0F8FF"
)

button_frame.pack(pady=10)

tk.Button(
    button_frame,
    text="Calculate BMI",
    command=calculate_bmi,
    bg="green",
    fg="white",
    width=15
).grid(row=0, column=0, padx=5)

tk.Button(
    button_frame,
    text="Statistics",
    command=show_statistics,
    bg="orange",
    fg="white",
    width=15
).grid(row=0, column=1, padx=5)

tk.Button(
    button_frame,
    text="Show Graph",
    command=show_graph,
    bg="blue",
    fg="white",
    width=15
).grid(row=0, column=2, padx=5)

tk.Button(
    button_frame,
    text="Delete Record",
    command=delete_record,
    bg="red",
    fg="white",
    width=15
).grid(row=0, column=3, padx=5)

tk.Button(
    button_frame,
    text="Clear All",
    command=clear_all,
    bg="darkred",
    fg="white",
    width=15
).grid(row=0, column=4, padx=5)

# Result Label

result_label = tk.Label(
    root,
    text="Enter details and click Calculate BMI",
    font=("Arial", 14, "bold"),
    bg="#F0F8FF"
)

result_label.pack(pady=10)

# Table

columns = (
    "ID",
    "Name",
    "Weight",
    "Height",
    "BMI",
    "Category",
    "Date"
)

tree = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=15
)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

# Load Data

load_records()

# Run App

root.mainloop()

# Close Database

conn.close()