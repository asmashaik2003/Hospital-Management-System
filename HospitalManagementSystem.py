"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# --------------------- DATABASE SETUP ---------------------
conn = sqlite3.connect('hospital.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tablet_name TEXT,
        reference_no TEXT,
        dose TEXT,
        no_of_tablets TEXT,
        lot TEXT,
        issue_date TEXT,
        exp_date TEXT,
        daily_dose TEXT,
        side_effect TEXT,
        blood_pressure TEXT,
        storage_advice TEXT,
        medication TEXT,
        patient_id TEXT,
        nhs_number TEXT,
        patient_name TEXT,
        dob TEXT,
        address TEXT
    )
''')
conn.commit()

# --------------------- FUNCTIONS ---------------------
def insert_data():
    data = (
        tablet_name.get(), ref_no.get(), dose.get(), num_tablets.get(), lot.get(),
        issue_date.get(), exp_date.get(), daily_dose.get(), side_effect.get(),
        bp.get(), storage.get(), medication.get(), patient_id.get(), nhs_no.get(),
        patient_name.get(), dob.get(), address.get()
    )
    cursor.execute('''
        INSERT INTO patients (
            tablet_name, reference_no, dose, no_of_tablets, lot,
            issue_date, exp_date, daily_dose, side_effect,
            blood_pressure, storage_advice, medication, patient_id,
            nhs_number, patient_name, dob, address
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    fetch_data()
    clear_fields()

def fetch_data():
    tree.delete(*tree.get_children())
    cursor.execute("SELECT * FROM patients")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

def clear_fields():
    for var in entry_vars:
        var.set("")
    prescription_box.delete("1.0", tk.END)

def delete_data():
    selected = tree.selection()
    if selected:
        row = tree.item(selected[0])['values']
        cursor.execute("DELETE FROM patients WHERE id=?", (row[0],))
        conn.commit()
        fetch_data()
        clear_fields()
    else:
        messagebox.showwarning("Delete", "Please select a record to delete")

def update_data():
    selected = tree.selection()
    if selected:
        row = tree.item(selected[0])['values']
        data = (
            tablet_name.get(), ref_no.get(), dose.get(), num_tablets.get(), lot.get(),
            issue_date.get(), exp_date.get(), daily_dose.get(), side_effect.get(),
            bp.get(), storage.get(), medication.get(), patient_id.get(), nhs_no.get(),
            patient_name.get(), dob.get(), address.get(), row[0]
        )
        cursor.execute('''
            UPDATE patients SET
                tablet_name=?, reference_no=?, dose=?, no_of_tablets=?, lot=?,
                issue_date=?, exp_date=?, daily_dose=?, side_effect=?,
                blood_pressure=?, storage_advice=?, medication=?, patient_id=?,
                nhs_number=?, patient_name=?, dob=?, address=?
            WHERE id=?
        ''', data)
        conn.commit()
        fetch_data()
        clear_fields()
    else:
        messagebox.showwarning("Update", "Please select a record to update")

def generate_prescription():
    prescription_box.delete("1.0", tk.END)
    prescription = (
        f"Patient Name: {patient_name.get()}\n"
        f"Patient ID: {patient_id.get()}\n"
        f"NHS Number: {nhs_no.get()}\n"
        f"DOB: {dob.get()}\n"
        f"Address: {address.get()}\n\n"
        f"Tablet Name: {tablet_name.get()}\n"
        f"Reference No: {ref_no.get()}\n"
        f"Dose: {dose.get()}\n"
        f"Number of Tablets: {num_tablets.get()}\n"
        f"Lot: {lot.get()}\n"
        f"Issue Date: {issue_date.get()}\n"
        f"Expiry Date: {exp_date.get()}\n"
        f"Daily Dose: {daily_dose.get()}\n"
        f"Side Effects: {side_effect.get()}\n"
        f"Blood Pressure: {bp.get()}\n"
        f"Storage Advice: {storage.get()}\n"
        f"Medication: {medication.get()}\n"
    )
    prescription_box.insert(tk.END, prescription)

def on_row_select(event):
    selected = tree.focus()
    if selected:
        row = tree.item(selected)['values']
        for i, var in enumerate(entry_vars):
            var.set(row[i + 1])  # skip ID which is at index 0
        generate_prescription()

# --------------------- GUI SETUP ---------------------
root = tk.Tk()
root.title("Hospital Management System")
root.geometry("1400x750")

tk.Label(root, text="HOSPITAL MANAGEMENT SYSTEM", font=("Arial", 30, "bold"), fg="red").pack(fill=tk.X)

# Form Frame
form_frame = tk.Frame(root, padx=10, pady=10)
form_frame.pack(side=tk.TOP, fill=tk.X)

labels = [
    "Name Of Tablets", "Reference No", "Dose", "No Of Tablets", "Lot",
    "Issue Date", "Exp Date", "Daily Dose", "Side Effect", "Blood Pressure",
    "Storage Advice", "Medication", "Patient Id", "NHS Number", "Patient Name",
    "Date Of Birth", "Patient Address"
]

entry_vars = [tk.StringVar() for _ in labels]
(
    tablet_name, ref_no, dose, num_tablets, lot, issue_date, exp_date,
    daily_dose, side_effect, bp, storage, medication, patient_id, nhs_no,
    patient_name, dob, address
) = entry_vars

for i, label in enumerate(labels):
    row = i % 9
    col = i // 9
    tk.Label(form_frame, text=label).grid(row=row, column=col*2, sticky=tk.W, padx=5, pady=2)
    tk.Entry(form_frame, textvariable=entry_vars[i], width=30).grid(row=row, column=col*2+1, padx=5, pady=2)

# Prescription Frame
prescription_frame = tk.Frame(root)
prescription_frame.pack(pady=10)
tk.Label(prescription_frame, text="Prescription", font=('Arial', 12, 'bold')).pack(anchor='w')
prescription_box = tk.Text(prescription_frame, height=10, width=100)
prescription_box.pack()

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Record", width=15, bg="green", fg="white", command=insert_data).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Show Data", width=15, bg="green", fg="white", command=fetch_data).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Update", width=15, bg="green", fg="white", command=update_data).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Delete", width=15, bg="green", fg="white", command=delete_data).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Reset", width=15, bg="green", fg="white", command=clear_fields).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Prescription", width=15, bg="green", fg="white", command=generate_prescription).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Exit", width=15, bg="green", fg="white", command=root.quit).pack(side=tk.LEFT, padx=5)

# Data Table
tree_frame = tk.Frame(root)
tree_frame.pack(fill=tk.BOTH, expand=True)

cols = [
    "ID", "Tablet Name", "Ref No", "Dose", "No of Tablets", "Lot", "Issue Date", "Exp Date",
    "Daily Dose", "Side Effect", "BP", "Storage", "Medication", "Patient ID", "NHS No",
    "Name", "DOB", "Address"
]

tree = ttk.Treeview(tree_frame, columns=cols, show="headings")
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor=tk.CENTER)
tree.pack(fill=tk.BOTH, expand=True)
tree.bind("<<TreeviewSelect>>", on_row_select)

# Initial data load
fetch_data()

# Run app
root.mainloop()"""
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# --------------------- DATABASE SETUP ---------------------
conn = sqlite3.connect('hospital.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tablet_name TEXT,
        reference_no TEXT,
        dose TEXT,
        no_of_tablets TEXT,
        lot TEXT,
        issue_date TEXT,
        exp_date TEXT,
        daily_dose TEXT,
        side_effect TEXT,
        blood_pressure TEXT,
        storage_advice TEXT,
        medication TEXT,
        patient_id TEXT,
        nhs_number TEXT,
        patient_name TEXT,
        dob TEXT,
        address TEXT
    )
''')
conn.commit()

# --------------------- FUNCTIONS ---------------------
def insert_data():
    data = (
        tablet_name.get(), ref_no.get(), dose.get(), num_tablets.get(), lot.get(),
        issue_date.get(), exp_date.get(), daily_dose.get(), side_effect.get(),
        bp.get(), storage.get(), medication.get(), patient_id.get(), nhs_no.get(),
        patient_name.get(), dob.get(), address.get()
    )
    cursor.execute('''
        INSERT INTO patients (
            tablet_name, reference_no, dose, no_of_tablets, lot,
            issue_date, exp_date, daily_dose, side_effect,
            blood_pressure, storage_advice, medication, patient_id,
            nhs_number, patient_name, dob, address
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    fetch_data()
    generate_prescription()

def fetch_data(search_term=None):
    for item in tree.get_children():
        tree.delete(item)
    if search_term:
        cursor.execute("SELECT * FROM patients WHERE patient_name LIKE ?", ('%' + search_term + '%',))
    else:
        cursor.execute("SELECT * FROM patients")
    rows = cursor.fetchall()
    for row in rows:
        display_row = (
            row[1], row[2], row[3], row[4], row[5], row[6],
            row[7], row[8], row[11], row[14], row[15], row[16], row[17]
        )
        tree.insert("", tk.END, values=display_row)

def clear_fields():
    for var in entry_vars:
        var.set("")
    prescription_box.delete("1.0", tk.END)

def delete_data():
    selected = tree.selection()
    if selected:
        item = tree.item(selected[0])['values']
        cursor.execute("DELETE FROM patients WHERE reference_no=? AND patient_name=?", (item[1], item[10]))
        conn.commit()
        fetch_data()
    else:
        messagebox.showwarning("Delete", "Please select a record to delete")

def update_data():
    selected = tree.selection()
    if selected:
        item = tree.item(selected[0])['values']
        data = (
            tablet_name.get(), ref_no.get(), dose.get(), num_tablets.get(), lot.get(),
            issue_date.get(), exp_date.get(), daily_dose.get(), side_effect.get(),
            bp.get(), storage.get(), medication.get(), patient_id.get(), nhs_no.get(),
            patient_name.get(), dob.get(), address.get(), item[1], item[10]
        )
        cursor.execute('''
            UPDATE patients SET
                tablet_name=?, reference_no=?, dose=?, no_of_tablets=?, lot=?,
                issue_date=?, exp_date=?, daily_dose=?, side_effect=?,
                blood_pressure=?, storage_advice=?, medication=?, patient_id=?,
                nhs_number=?, patient_name=?, dob=?, address=?
            WHERE reference_no=? AND patient_name=?
        ''', data)
        conn.commit()
        fetch_data()
    else:
        messagebox.showwarning("Update", "Please select a record to update")

def generate_prescription():
    prescription_box.delete("1.0", tk.END)
    prescription = (
        f"Patient Name: {patient_name.get()}\n"
        f"Patient ID: {patient_id.get()}\n"
        f"NHS Number: {nhs_no.get()}\n"
        f"DOB: {dob.get()}\n"
        f"Address: {address.get()}\n\n"
        f"Tablet Name: {tablet_name.get()}\n"
        f"Reference No: {ref_no.get()}\n"
        f"Dose: {dose.get()}\n"
        f"Number of Tablets: {num_tablets.get()}\n"
        f"Lot: {lot.get()}\n"
        f"Issue Date: {issue_date.get()}\n"
        f"Expiry Date: {exp_date.get()}\n"
        f"Daily Dose: {daily_dose.get()}\n"
        f"Storage Advice: {storage.get()}\n"
    )
    prescription_box.insert(tk.END, prescription)

def search_patient():
    search_term = search_var.get()
    fetch_data(search_term)

# --------------------- GUI SETUP ---------------------
root = tk.Tk()
root.title("Hospital Management System")
root.geometry("1400x750")

tk.Label(root, text="HOSPITAL MANAGEMENT SYSTEM", font=("Arial", 30, "bold"), fg="red").pack(fill=tk.X)

# Form Frame
form_frame = tk.Frame(root, padx=10, pady=10)
form_frame.pack(side=tk.TOP, fill=tk.X)

labels = [
    "Name Of Tablets", "Reference No", "Dose", "No Of Tablets", "Lot",
    "Issue Date", "Exp Date", "Daily Dose", "Side Effect", "Blood Pressure",
    "Storage Advice", "Medication", "Patient Id", "NHS Number", "Patient Name",
    "Date Of Birth", "Patient Address"
]

entry_vars = [tk.StringVar() for _ in labels]
(
    tablet_name, ref_no, dose, num_tablets, lot, issue_date, exp_date,
    daily_dose, side_effect, bp, storage, medication, patient_id, nhs_no,
    patient_name, dob, address
) = entry_vars

for i, label in enumerate(labels):
    row = i % 9
    col = i // 9
    tk.Label(form_frame, text=label).grid(row=row, column=col*2, sticky=tk.W, padx=5, pady=2)
    tk.Entry(form_frame, textvariable=entry_vars[i], width=30).grid(row=row, column=col*2+1, padx=5, pady=2)

# Prescription Block
prescription_frame = tk.Frame(root)
prescription_frame.pack(pady=10)
tk.Label(prescription_frame, text="Prescription", font=('Arial', 12, 'bold')).pack(anchor='w')
prescription_box = tk.Text(prescription_frame, height=8, width=100)
prescription_box.pack()

# Search Bar
search_frame = tk.Frame(root)
search_frame.pack(pady=5)
search_var = tk.StringVar()
tk.Label(search_frame, text="Search Patient Name:").pack(side=tk.LEFT)
tk.Entry(search_frame, textvariable=search_var, width=30).pack(side=tk.LEFT, padx=5)
tk.Button(search_frame, text="Search", command=search_patient, bg="blue", fg="white").pack(side=tk.LEFT)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)
tk.Button(button_frame, text="Add Record", width=15, bg="green", fg="white", command=insert_data).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Update", width=15, bg="green", fg="white", command=update_data).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Delete", width=15, bg="green", fg="white", command=delete_data).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Reset", width=15, bg="green", fg="white", command=clear_fields).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Exit", width=15, bg="green", fg="white", command=root.quit).pack(side=tk.LEFT, padx=5)

# Table Frame
tree_frame = tk.Frame(root)
tree_frame.pack(fill=tk.BOTH, expand=True)

tree_scroll_y = tk.Scrollbar(tree_frame)
tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

tree_scroll_x = tk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

displayed_cols = [
    "Tablet Name", "Ref No", "Dose", "No of Tablets", "Lot",
    "Issue Date", "Exp Date", "Daily Dose", "Storage", "NHS No",
    "Name", "DOB", "Address"
]

tree = ttk.Treeview(tree_frame, columns=displayed_cols, show="headings",
                    yscrollcommand=tree_scroll_y.set,
                    xscrollcommand=tree_scroll_x.set)

for col in displayed_cols:
    tree.heading(col, text=col)
    tree.column(col, width=120, anchor=tk.CENTER)

tree_scroll_y.config(command=tree.yview)
tree_scroll_x.config(command=tree.xview)

tree.pack(fill=tk.BOTH, expand=True)
tree.configure(height=4)  # Show 4 rows

# Initial Load
fetch_data()

root.mainloop()


