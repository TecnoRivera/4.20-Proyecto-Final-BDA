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

def show_employees():
    try:
        for row in emp_table.get_children():
            emp_table.delete(row)

        query = """
        MATCH (e:Employee)-[:BELONGS_TO]->(d:Department)
        OPTIONAL MATCH (e)-[:MANAGES]->(mgr:Employee)
        RETURN e.empno AS empno, e.ename AS ename, e.job AS job,
               d.dname AS department, mgr.ename AS manager
        """
        result = execute_query(query)

        for record in result:
            empno = record["empno"]
            ename = record["ename"]
            job = record["job"]
            department = record["department"] or "None"
            manager = record["manager"] or "None"
            emp_table.insert("", "end", text=empno, values=(empno, ename, job, department, manager))
    except Exception as e:
        messagebox.showerror("Error", str(e))

def create_employee():
    try:
        empno = empno_entry.get()
        ename = ename_entry.get()
        job = job_entry.get()
        deptno = deptno_entry.get()
        mgr_empno = mgr_entry.get()

        if empno and ename and job and deptno:
            query = "CREATE (e:Employee {empno: $empno, ename: $ename, job: $job})"
            execute_query(query, {"empno": empno, "ename": ename, "job": job})

            query = """
            MATCH (e:Employee {empno: $empno}), (d:Department {deptno: $deptno})
            CREATE (e)-[:BELONGS_TO]->(d)
            """
            execute_query(query, {"empno": empno, "deptno": deptno})

            if mgr_empno:
                query = """
                MATCH (e:Employee {empno: $empno}), (mgr:Employee {empno: $mgr_empno})
                CREATE (mgr)-[:MANAGES]->(e)
                """
                execute_query(query, {"empno": empno, "mgr_empno": mgr_empno})

            empno_entry.delete(0, END)
            ename_entry.delete(0, END)
            job_entry.delete(0, END)
            deptno_entry.delete(0, END)
            mgr_entry.delete(0, END)
            show_employees()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios excepto el manager")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def update_employee(event=None):
    try:
        selected_item = emp_table.focus()
        if not selected_item:
            messagebox.showerror("Error", "Selecciona un empleado para actualizar")
            return

        empno = emp_table.item(selected_item, "text")
        ename = emp_table.item(selected_item, "values")[1]
        job = emp_table.item(selected_item, "values")[2]
        department = emp_table.item(selected_item, "values")[3]
        manager = emp_table.item(selected_item, "values")[4]

        empno_entry.delete(0, END)
        empno_entry.insert(0, empno)
        ename_entry.delete(0, END)
        ename_entry.insert(0, ename)
        job_entry.delete(0, END)
        job_entry.insert(0, job)
        deptno_entry.delete(0, END)
        deptno_entry.insert(0, department if department != "None" else "")
        mgr_entry.delete(0, END)
        mgr_entry.insert(0, manager if manager != "None" else "")

        update_btn.config(command=lambda: update_employee_from_ui(empno))
    except Exception as e:
        messagebox.showerror("Error", str(e))

def update_employee_from_ui(empno):
    try:
        ename = ename_entry.get()
        job = job_entry.get()
        deptno = deptno_entry.get()
        mgr_empno = mgr_entry.get()

        if ename and job and deptno:
            query = """
            MATCH (e:Employee {empno: $empno})
            SET e.ename = $ename, e.job = $job
            """
            execute_query(query, {"empno": empno, "ename": ename, "job": job})

            query = """
            MATCH (e:Employee {empno: $empno})-[r:BELONGS_TO]->(:Department)
            DELETE r
            """
            execute_query(query, {"empno": empno})
            query = """
            MATCH (e:Employee {empno: $empno}), (d:Department {deptno: $deptno})
            CREATE (e)-[:BELONGS_TO]->(d)
            """
            execute_query(query, {"empno": empno, "deptno": deptno})

            query = """
            MATCH (e:Employee {empno: $empno})<-[r:MANAGES]-(:Employee)
            DELETE r
            """
            execute_query(query, {"empno": empno})
            if mgr_empno:
                query = """
                MATCH (e:Employee {empno: $empno}), (mgr:Employee {empno: $mgr_empno})
                CREATE (mgr)-[:MANAGES]->(e)
                """
                execute_query(query, {"empno": empno, "mgr_empno": mgr_empno})

            show_employees()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios excepto el manager")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_employee(event=None):
    try:
        selected_item = emp_table.focus()
        if not selected_item:
            messagebox.showerror("Error", "Selecciona un empleado para eliminar")
            return
        empno = emp_table.item(selected_item, "text")
        query = """
        MATCH (e:Employee {empno: $empno}) 
        DETACH DELETE e
        """
        execute_query(query, {"empno": empno})
        show_employees()
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = Tk()
root.title("Employees CRUD")
root.geometry("900x650")
root.config(bg="#f4f4f9")

form_frame = Frame(root, bg="#f4f4f9", padx=20, pady=10)
form_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

Label(form_frame, text="Employee No", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=5)
empno_entry = Entry(form_frame, font=("Arial", 10), bd=2)
empno_entry.grid(row=0, column=1, padx=10, pady=5)

Label(form_frame, text="Name", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=5)
ename_entry = Entry(form_frame, font=("Arial", 10), bd=2)
ename_entry.grid(row=1, column=1, padx=10, pady=5)

Label(form_frame, text="Job", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=5)
job_entry = Entry(form_frame, font=("Arial", 10), bd=2)
job_entry.grid(row=2, column=1, padx=10, pady=5)

Label(form_frame, text="Department No", font=("Arial", 10)).grid(row=3, column=0, padx=10, pady=5)
deptno_entry = Entry(form_frame, font=("Arial", 10), bd=2)
deptno_entry.grid(row=3, column=1, padx=10, pady=5)

Label(form_frame, text="Manager Emp No", font=("Arial", 10)).grid(row=4, column=0, padx=10, pady=5)
mgr_entry = Entry(form_frame, font=("Arial", 10), bd=2)
mgr_entry.grid(row=4, column=1, padx=10, pady=5)

button_frame = Frame(root, bg="#f4f4f9", pady=10)
button_frame.grid(row=1, column=0, columnspan=2, padx=10)

Button(button_frame, text="Add Employee", font=("Arial", 10), bg="#4CAF50", fg="white", command=create_employee).grid(row=0, column=0, padx=10, pady=5)
update_btn = Button(button_frame, text="Update Employee", font=("Arial", 10), bg="#2196F3", fg="white", command=update_employee)
update_btn.grid(row=0, column=1, padx=10, pady=5)
Button(button_frame, text="Delete Employee", font=("Arial", 10), bg="#F44336", fg="white", command=delete_employee).grid(row=0, column=2, padx=10, pady=5)

emp_table = ttk.Treeview(root, columns=("empno", "ename", "job", "dept", "manager"), show="headings", height=8)
emp_table.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

emp_table.heading("empno", text="Emp No", anchor=CENTER)
emp_table.heading("ename", text="Name", anchor=CENTER)
emp_table.heading("job", text="Job", anchor=CENTER)
emp_table.heading("dept", text="Department", anchor=CENTER)
emp_table.heading("manager", text="Manager", anchor=CENTER)

emp_table.tag_configure("evenrow", background="#f9f9f9")
emp_table.tag_configure("oddrow", background="#ffffff")

emp_table.bind("<Double-1>", update_employee)
emp_table.bind("<Double-3>", delete_employee)

show_employees()

root.mainloop()
close_connection()
