import subprocess
from tkinter import Tk, Button

def open_dept_crud():
    subprocess.Popen(["python", "dept_crud.py"])

def open_emp_crud():
    subprocess.Popen(["python", "emp_crud.py"])

def setup_window():
    window = Tk()
    window.title("Main Menu")

    window_width = 500
    window_height = 400

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    window.config(bg="#333333")  

    return window

def create_button(parent, text, command, bg="#4CAF50"):
    button_font = ("Arial", 12, "bold")
    button_fg = "white" 

    return Button(
        parent,
        text=text,
        command=command,
        font=button_font,
        bg=bg,  
        fg=button_fg,
        padx=10,
        pady=5
    )

def main():
    window = setup_window()

    btn_dept_crud = create_button(window, "Departments CRUD", open_dept_crud)
    btn_emp_crud = create_button(window, "Employees CRUD", open_emp_crud)
    btn_exit = create_button(window, "Exit", window.quit, bg="#FF5733")  

    btn_dept_crud.pack(fill="x", pady=15, padx=50)
    btn_emp_crud.pack(fill="x", pady=15, padx=50)
    btn_exit.pack(fill="x", pady=15, padx=50) 

    window.mainloop()

if __name__ == "__main__":
    main()