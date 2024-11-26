from tkinter import *
from tkinter import messagebox, ttk
from neo4j import GraphDatabase

uri = "neo4j://localhost:7687"
user = "neo4j"
password = "Emiliano"
driver = GraphDatabase.driver(uri, auth=(user, password))

def close_connection():
    driver.close()


def execute_query(query, parameters=None):
    with driver.session() as session:
        result = session.run(query, parameters)
        return list(result)

def show_departments():
    try:
        for row in dept_table.get_children():
            dept_table.delete(row)

        query = "MATCH (d:Department) RETURN d"
        result = execute_query(query)

        for record in result:
            dept = record["d"]
            deptno = dept.get("deptno", "Unknown")
            dname = dept.get("dname", "Unknown")
            location = dept.get("location", "Unknown")
            dept_table.insert("", "end", text=deptno, values=(dname, location))
    except Exception as e:
        messagebox.showerror("Error", str(e))


def create_department():
    try:
        deptno = deptno_entry.get()
        dname = dname_entry.get()
        location = location_entry.get()

        if not all([deptno, dname, location]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        query = """
        CREATE (d:Department {deptno: $deptno, dname: $dname, location: $location})
        """
        execute_query(query, {"deptno": deptno, "dname": dname, "location": location})

        clear_inputs()
        show_departments()
    except Exception as e:
        messagebox.showerror("Error", str(e))


def update_department():
    try:
        selected_item = dept_table.focus()
        if not selected_item:
            messagebox.showerror("Error", "Selecciona un departamento para actualizar")
            return

        deptno = dept_table.item(selected_item, "text")
        dname = dname_entry.get()
        location = location_entry.get()

        if not all([dname, location]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        query = """
        MATCH (d:Department {deptno: $deptno})
        SET d.dname = $dname, d.location = $location
        """
        execute_query(query, {"deptno": deptno, "dname": dname, "location": location})

        clear_inputs()
        show_departments()
    except Exception as e:
        messagebox.showerror("Error", str(e))


def delete_department():
    try:
        selected_item = dept_table.focus()
        if not selected_item:
            messagebox.showerror("Error", "Selecciona un departamento para eliminar")
            return

        deptno = dept_table.item(selected_item, "text")
        query = """
        MATCH (d:Department {deptno: $deptno})
        OPTIONAL MATCH (d)<-[:BELONGS_TO]-(e:Employee)
        DELETE d, e
        """
        execute_query(query, {"deptno": deptno})

        show_departments()
    except Exception as e:
        messagebox.showerror("Error", str(e))


def clear_inputs():
    deptno_entry.delete(0, END)
    dname_entry.delete(0, END)
    location_entry.delete(0, END)


root = Tk()
root.title("Departments CRUD")
root.geometry("800x500")
root.configure(bg="#f4f4f4")

style = ttk.Style()
style.configure("Treeview", font=("Arial", 10), rowheight=25)
style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

frame_inputs = Frame(root, bg="#f4f4f4")
frame_inputs.pack(pady=20)

Label(frame_inputs, text="Dept No", bg="#f4f4f4").grid(row=0, column=0, padx=10, pady=5)
deptno_entry = Entry(frame_inputs, width=30)
deptno_entry.grid(row=0, column=1, padx=10, pady=5)

Label(frame_inputs, text="Name", bg="#f4f4f4").grid(row=1, column=0, padx=10, pady=5)
dname_entry = Entry(frame_inputs, width=30)
dname_entry.grid(row=1, column=1, padx=10, pady=5)

Label(frame_inputs, text="Location", bg="#f4f4f4").grid(row=2, column=0, padx=10, pady=5)
location_entry = Entry(frame_inputs, width=30)
location_entry.grid(row=2, column=1, padx=10, pady=5)

frame_buttons = Frame(root, bg="#f4f4f4")
frame_buttons.pack(pady=10)

Button(frame_buttons, text="Add Department", command=create_department, bg="#4CAF50", fg="white", width=15).pack(side=LEFT, padx=10)
Button(frame_buttons, text="Update Department", command=update_department, bg="#FFC107", fg="black", width=15).pack(side=LEFT, padx=10)
Button(frame_buttons, text="Delete Department", command=delete_department, bg="#FF5733", fg="white", width=15).pack(side=LEFT, padx=10)

dept_table = ttk.Treeview(root, columns=("dname", "location"), show="headings")
dept_table.pack(fill=BOTH, expand=True, pady=20, padx=20)
dept_table.heading("dname", text="Name")
dept_table.heading("location", text="Location")

show_departments()

root.mainloop()
close_connection()
