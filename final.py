from tkinter import *
from tkinter import messagebox, ttk
import csv
import os


# File name for storing user data
FILE_NAME = "users.csv"


# Initialize CSV file with headers if it doesn't exist
def initialize_csv():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["unique_id", "name", "address", "designation"])


# Get the next unique ID
def get_next_id():
    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            rows = list(reader)
            if len(rows) > 1:  # If there are rows after the header
                last_id = int(rows[-1][0])#get the id from last row
                return last_id + 1
            return 1
    except Exception as e:
        messagebox.showerror(title="Error", message=f"Error reading file: {e}")
        return 1


# Add a new user
def add_user():
    name = textbox_name.get()
    address = textbox_address.get()
    designation = textbox_designation.get()

    if not name or not address or not designation:
        messagebox.showinfo(title="Validation Error", message="All fields must be filled.")
        return

    try:
        # Check for duplicate names
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            if any(row[1].lower() == name.lower() for row in reader if row):
                messagebox.showinfo(title="Duplicate Error", message="User with this name already exists.")
                return

        # Write user data
        unique_id = get_next_id()
        with open(FILE_NAME, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([unique_id, name, address, designation])

        # Clear input fields
        textbox_name.delete(0, END)
        textbox_address.delete(0, END)
        textbox_designation.delete(0, END)

        messagebox.showinfo(title="Success", message="User added successfully!")
    except Exception as e:
        messagebox.showerror(title="Error", message=f"Error saving user: {e}")


# View user details
def view_user():
    user_id = textbox_view_id.get()
    if not user_id.isdigit():
        messagebox.showinfo(title="Validation Error", message="Please enter a valid numeric ID.")
        return

    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == user_id:
                    messagebox.showinfo(title="User Details", message=f"ID: {row[0]}\nName: {row[1]}\nAddress: {row[2]}\nDesignation: {row[3]}")
                    return
            messagebox.showinfo(title="Not Found", message="No user found with the given ID.")
    except Exception as e:
        messagebox.showerror(title="Error", message=f"Error reading user details: {e}")


# List all users
def list_users():
    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            rows = list(reader)
            if len(rows) <= 1:
                messagebox.showinfo(title="No Data", message="No users found.")
                return

            # Display all users in a new window
            list_window = Toplevel(tk)
            list_window.title("All Users")
            list_window.geometry("600x400")

            # Create treeview for displaying users
            tree = ttk.Treeview(list_window, columns=("ID", "Name", "Address", "Designation"), show="headings")
            tree.heading("ID", text="ID")
            tree.heading("Name", text="Name")
            tree.heading("Address", text="Address")
            tree.heading("Designation", text="Designation")
            tree.column("ID", width=50)
            tree.column("Name", width=150)
            tree.column("Address", width=200)
            tree.column("Designation", width=150)
            tree.pack(fill=BOTH, expand=True)

            # Add rows to treeview
            for row in rows[1:]:  # Skip the header
                tree.insert("", END, values=row)
    except Exception as e:
        messagebox.showerror(title="Error", message=f"Error listing users: {e}")


# Update user details
def update_user():
    user_id = textbox_update_id.get()
    name = textbox_update_name.get()
    address = textbox_update_address.get()
    designation = textbox_update_designation.get()

    if not user_id.isdigit():
        messagebox.showinfo(title="Validation Error", message="Please enter a valid numeric ID.")
        return

    updated = False
    try:
        with open(FILE_NAME, "r") as file:
            rows = list(csv.reader(file))

        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            for row in rows:
                if row[0] == user_id:
                    if name:
                        row[1] = name
                    if address:
                        row[2] = address
                    if designation:
                        row[3] = designation
                    updated = True
                writer.writerow(row)

        if updated:
            messagebox.showinfo(title="Success", message="User updated successfully!")
        else:
            messagebox.showinfo(title="Not Found", message="No user found with the given ID.")
    except Exception as e:
        messagebox.showerror(title="Error", message=f"Error updating user: {e}")


# Initialize CSV file
initialize_csv()

# UI Setup
tk = Tk()
tk.title("User Information Management System")
tk.config(padx=20, pady=20)

# Add User Section
Label(text="Add User").grid(column=0, row=0, columnspan=2, pady=10)
Label(text="Name:").grid(column=0, row=1, sticky="E")
textbox_name = Entry(width=30)
textbox_name.grid(column=1, row=1)

Label(text="Address:").grid(column=0, row=2, sticky="E")
textbox_address = Entry(width=30)
textbox_address.grid(column=1, row=2)

Label(text="Designation:").grid(column=0, row=3, sticky="E")
textbox_designation = Entry(width=30)
textbox_designation.grid(column=1, row=3)

Button(text="Add User", command=add_user).grid(column=1, row=4, pady=10)

# View User Section
Label(text="View User").grid(column=0, row=5, columnspan=2, pady=10)
Label(text="User ID:").grid(column=0, row=6, sticky="E")
textbox_view_id = Entry(width=30)
textbox_view_id.grid(column=1, row=6)

Button(text="View User", command=view_user).grid(column=1, row=7, pady=10)

# Update User Section
Label(text="Update User").grid(column=0, row=8, columnspan=2, pady=10)
Label(text="User ID:").grid(column=0, row=9, sticky="E")
textbox_update_id = Entry(width=30)
textbox_update_id.grid(column=1, row=9)

Label(text="Name:").grid(column=0, row=10, sticky="E")
textbox_update_name = Entry(width=30)
textbox_update_name.grid(column=1, row=10)

Label(text="Address:").grid(column=0, row=11, sticky="E")
textbox_update_address = Entry(width=30)
textbox_update_address.grid(column=1, row=11)

Label(text="Designation:").grid(column=0, row=12, sticky="E")
textbox_update_designation = Entry(width=30)
textbox_update_designation.grid(column=1, row=12)

Button(text="Update User", command=update_user).grid(column=1, row=13, pady=10)

# List All Users Section
Button(text="List All Users", command=list_users).grid(column=1, row=14, pady=10)

tk.mainloop()
