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

        if deptno and dname and location:
            query = """
            CREATE (d:Department {deptno: $deptno, dname: $dname, location: $location})
            """
            execute_query(query, {"deptno": deptno, "dname": dname, "location": location})

            deptno_entry.delete(0, END)
            dname_entry.delete(0, END)
            location_entry.delete(0, END)
            show_departments()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
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

        if dname and location:
            query = """
            MATCH (d:Department {deptno: $deptno})
            SET d.dname = $dname, d.location = $location
            """
            execute_query(query, {"deptno": deptno, "dname": dname, "location": location})
            show_departments()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
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

# Interfaz gráfica
root = Tk()
root.title("Departments CRUD")
root.geometry("600x400")

Label(root, text="Dept No").grid(row=0, column=0, padx=10, pady=5)
deptno_entry = Entry(root)
deptno_entry.grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Name").grid(row=1, column=0, padx=10, pady=5)
dname_entry = Entry(root)
dname_entry.grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Location").grid(row=2, column=0, padx=10, pady=5)
location_entry = Entry(root)
location_entry.grid(row=2, column=1, padx=10, pady=5)

Button(root, text="Add Department", command=create_department).grid(row=3, column=0, padx=10, pady=5)
Button(root, text="Update Department", command=update_department).grid(row=3, column=1, padx=10, pady=5)
Button(root, text="Delete Department", command=delete_department).grid(row=4, column=0, padx=10, pady=5)

dept_table = ttk.Treeview(root, columns=("dname", "location"), show="headings")
dept_table.grid(row=5, column=0, columnspan=2, padx=10, pady=5)
dept_table.heading("dname", text="Name")
dept_table.heading("location", text="Location")

show_departments()

root.mainloop()
close_connection()
