from tkinter import *
import subprocess

def open_dept_crud():
    subprocess.Popen(["python", "dept_crud.py"])

def open_emp_crud():
    subprocess.Popen(["python", "emp_crud.py"])

window = Tk()
window.title("Main Menu")

window_width = 500
window_height = 400

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x_position = (screen_width - window_width) 
y_position = (screen_height - window_height) 

window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

window.config(bg="#333333")  

button_font = ("Arial", 12, "bold")
button_bg = "#4CAF50"      
button_fg = "white"

Button(window, text="Departments CRUD", command=open_dept_crud, font=button_font, bg=button_bg, fg=button_fg).pack(fill=X, pady=10, padx=20)
Button(window, text="Employees CRUD", command=open_emp_crud, font=button_font, bg=button_bg, fg=button_fg).pack(fill=X, pady=10, padx=20)

window.mainloop()