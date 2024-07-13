from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkcalendar import Calendar

# Creating the Window for the application
root = Tk()
root.geometry("600x400") # dimensions of the window
root.title("to-do list") # title of the window

# tkinter strings to store task titles
title_var = tk.StringVar()
edit_title_var = tk.StringVar()

id = 0

# ID generator
def generate_id():
    global id
    id += 1
    return id

# All tasks go into this dictionary
To_do = {}

# Dictionary to store checkbox states
checkbox_states = {}


def load_screen():
    for widget in root.winfo_children():
        widget.destroy()
    Title = tk.Label(root, text='Title:', font=('calibre', 10, 'bold'))
    Title.grid(row=0, column=0)
    title_entry = tk.Entry(root, textvariable=title_var, font=('calibre', 10, 'normal'))
    title_entry.grid(row=0, column=1)

    # date
    global cal
    Date_label = tk.Label(root, text='Date:', font=('calibre', 10, 'bold'))
    Date_label.grid(row=1, column=0)
    cal = Calendar(root, selectmode='day')
    cal.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    # button
    sub_btn = tk.Button(root, text='Submit', command=submit)
    sub_btn.grid(row=4, column=0)

    display_task_details(root, To_do)


def display_task_details(parent, To_do, row=6, column=0):
    for key, value in To_do.items():
        if isinstance(value, dict):
            tasks = tk.Label(parent, text="TASKS")
            label = tk.Label(parent, text=key)
            tasks.grid(row=5, column=0)
            label.grid(row=row, column=column, sticky="w", padx=5, pady=2)

            # adding delete button
            delete_btn = tk.Button(parent, text="Delete", command=lambda key=key: delete_task(key))
            delete_btn.grid(row=row + 2, column=column + 5, padx=5, pady=2)
      
            # adding edit button
            edit_btn = tk.Button(parent, text="Edit", command=lambda key=key: edit_task(key))
            edit_btn.grid(row=row + 2, column=column + 6, padx=5, pady=2)

            # Add checkbox for marking as complete
            complete_var = tk.BooleanVar(value=checkbox_states.get(key, False))  # Retrieve checkbox state from dictionary
            complete_checkbox = tk.Checkbutton( 
                parent, text="Mark as Complete", variable=complete_var,
                command=lambda key=key, var=complete_var: mark_as_complete(key, var.get())
            )
            complete_checkbox.grid(row=row, column=column + 1, padx=5, pady=2)
            row += 2
            
            # Display the task metadata(name, date, status)
            row = display_task_details(parent, value, row, column + 1) 
        
        else:
            label_key = tk.Label(parent, text=key)
            label_key.grid(row=row, column=column, sticky="w", padx=5, pady=2)
            label_value = tk.Label(parent, text=value)
            label_value.grid(row=row, column=column + 1, sticky="w", padx=5, pady=2)
            row += 1
    
    return row


def edit_task(key):
    edit_window = tk.Toplevel(root)
    edit_window.geometry("500x400")
    edit_window.title("Edit Task")

    def save_changes():
        new_title = edit_title_var.get()
        new_date = cal.get_date()
        if new_title:
            To_do[key]['Task:'] = new_title
        To_do[key]['Date:'] = new_date
        edit_window.destroy()
        load_screen()
    
    task_label = tk.Label(edit_window, text="New Title:")
    task_label.grid(row=0, column=0, padx=5, pady=5)
    edit_title_entry = tk.Entry(edit_window, textvariable=edit_title_var)
    edit_title_entry.grid(row=0, column=1, padx=5, pady=5)

    Date_label = tk.Label(edit_window, text="New Date:")
    Date_label.grid(row=1, column=0, padx=5, pady=5)
    cal = Calendar(edit_window, selectmode='day')
    cal.grid(row=1, column=1, padx=5, pady=5)

    save_btn = tk.Button(edit_window, text="Save Changes", command=save_changes)
    save_btn.grid(row=2, columnspan=2, padx=5, pady=5)
    edit_title_var.set("")


def delete_task(key):
    global id
    del To_do[key]
    load_screen()
    id -= 1


def submit():
    id = generate_id()
    name = title_var.get()
    global cal
    date_selected = cal.get_date()

    to_do_temp = {
        'Task:': name,
        'Date:': date_selected,
       
    }
  
    To_do.update({id: to_do_temp})     
    title_var.set("")
    display_task_details(root, To_do)

#function to mark task as completed
def mark_as_complete(key, is_complete):
    checkbox_states[key] = is_complete  # Store checkbox state in dictionary
 

load_screen()
root.mainloop()