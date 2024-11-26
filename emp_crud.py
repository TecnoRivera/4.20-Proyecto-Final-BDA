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
        OPTIONAL MATCH (e)-[:MANAGES]->(m:Employee)
        RETURN e, d.dname AS dept_name, m.ename AS manager_name
        """
        result = execute_query(query)  
        
        for record in result:
            emp = record["e"]
            dept = record["dept_name"] or "None"
            mgr = record["manager_name"] or "None"
            emp_table.insert("", "end", text=emp["empno"], values=(emp["ename"], emp["job"], dept, mgr))
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
            # Crear empleado
            query = """
            CREATE (e:Employee {empno: $empno, ename: $ename, job: $job})
            """
            execute_query(query, {"empno": empno, "ename": ename, "job": job})

            # Establecer relación con departamento
            query = """
            MATCH (e:Employee {empno: $empno}), (d:Department {deptno: $deptno})
            CREATE (e)-[:BELONGS_TO]->(d)
            """
            execute_query(query, {"empno": empno, "deptno": deptno})

            # Establecer relación con manager, si existe
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

def update_employee():
    try:
        selected_item = emp_table.focus()
        if not selected_item:
            messagebox.showerror("Error", "Selecciona un empleado para actualizar")
            return
        empno = emp_table.item(selected_item, "text")
        ename = ename_entry.get()
        job = job_entry.get()
        deptno = deptno_entry.get()
        mgr_empno = mgr_entry.get()

        if ename and job and deptno:
            # Actualizar empleado
            query = """
            MATCH (e:Employee {empno: $empno})
            SET e.ename = $ename, e.job = $job
            """
            execute_query(query, {"empno": empno, "ename": ename, "job": job})

            # Actualizar relación con departamento
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

            # Actualizar relación con manager
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

def delete_employee():
    try:
        selected_item = emp_table.focus()
        if not selected_item:
            messagebox.showerror("Error", "Selecciona un empleado para eliminar")
            return
        empno = emp_table.item(selected_item, "text")
        query = "MATCH (e:Employee {empno: $empno}) DETACH DELETE e"
        execute_query(query, {"empno": empno})
        show_employees()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Interfaz gráfica
root = Tk()
root.title("Employees CRUD")
root.geometry("800x500")

Label(root, text="Emp No").grid(row=0, column=0, padx=10, pady=5)
empno_entry = Entry(root)
empno_entry.grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Name").grid(row=1, column=0, padx=10, pady=5)
ename_entry = Entry(root)
ename_entry.grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Job").grid(row=2, column=0, padx=10, pady=5)
job_entry = Entry(root)
job_entry.grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Dept No").grid(row=3, column=0, padx=10, pady=5)
deptno_entry = Entry(root)
deptno_entry.grid(row=3, column=1, padx=10, pady=5)

Label(root, text="Manager Emp No").grid(row=4, column=0, padx=10, pady=5)
mgr_entry = Entry(root)
mgr_entry.grid(row=4, column=1, padx=10, pady=5)

Button(root, text="Add Employee", command=create_employee).grid(row=5, column=0, padx=10, pady=5)
Button(root, text="Update Employee", command=update_employee).grid(row=5, column=1, padx=10, pady=5)
Button(root, text="Delete Employee", command=delete_employee).grid(row=6, column=0, padx=10, pady=5)

emp_table = ttk.Treeview(root, columns=("ename", "job", "dept", "manager"), show="headings")
emp_table.grid(row=7, column=0, columnspan=2, padx=10, pady=5)
emp_table.heading("ename", text="Name")
emp_table.heading("job", text="Job")
emp_table.heading("dept", text="Department")
emp_table.heading("manager", text="Manager")

show_employees()

root.mainloop()
close_connection()
