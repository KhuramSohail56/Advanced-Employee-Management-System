import tkinter as tk
from tkinter import ttk, messagebox
import oracledb
import csv

class EmployeeSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Employee Management System")
        self.root.geometry("1100x760")
        self.root.minsize(980, 680)
        self.root.configure(bg="#eef2f7")
        self.current_user = None
        self.current_role = None
        self.labels = ["Employee ID", "Name", "Gender", "Department", "Salary", "Contact"]
        self.sort_column = None
        self.sort_reverse = False
        self.selected_record_values = None
        self.setup_styles()
        
        try:
            self.conn = oracledb.connect(user="system", password="Kh$074571", dsn="localhost:1521/orcl")
            self.cursor = self.conn.cursor()
            self.contact_column = self.find_employee_column(
                ["CONTACT", "CONTACTNO", "CONTACT_NO", "PHONE", "PHONE_NO", "MOBILE", "MOBILE_NO"]
            )
            self.employee_select_columns = f"EmpID, Name, Gender, Department, Salary, {self.contact_column}"
        except Exception as e:
            messagebox.showerror("Database Error", f"Connection failed: {e}")
            self.root.destroy()

        self.login_window()

    def find_employee_column(self, possible_names):
        self.cursor.execute("SELECT COLUMN_NAME FROM USER_TAB_COLUMNS WHERE TABLE_NAME = 'EMPLOYEES'")
        db_columns = {str(row[0]).upper(): str(row[0]) for row in self.cursor.fetchall()}
        for name in possible_names:
            if name in db_columns:
                return db_columns[name]
        return "Contact"

    def setup_styles(self):
        self.colors = {
            "bg": "#e8eef8",
            "login_bg": "#dbeafe",
            "panel": "#ffffff",
            "primary": "#1d4ed8",
            "primary_dark": "#1d4ed8",
            "navy": "#0f172a",
            "accent": "#14b8a6",
            "success": "#16a34a",
            "warning": "#f59e0b",
            "danger": "#dc2626",
            "text": "#0f172a",
            "muted": "#64748b",
            "line": "#dbe4f0",
            "table": "#f8fafc",
        }

        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.style.configure("App.TFrame", background=self.colors["bg"])
        self.style.configure("Panel.TFrame", background=self.colors["panel"])
        self.style.configure("Header.TFrame", background=self.colors["primary"])
        self.style.configure("Title.TLabel", background=self.colors["primary"], foreground="white", font=("Segoe UI", 20, "bold"))
        self.style.configure("Subtitle.TLabel", background=self.colors["primary"], foreground="#dbeafe", font=("Segoe UI", 10))
        self.style.configure("PanelTitle.TLabel", background=self.colors["panel"], foreground=self.colors["text"], font=("Segoe UI", 12, "bold"))
        self.style.configure("Muted.TLabel", background=self.colors["panel"], foreground=self.colors["muted"], font=("Segoe UI", 9))
        self.style.configure("Stat.TLabel", background=self.colors["panel"], foreground=self.colors["primary"], font=("Segoe UI", 11, "bold"))
        self.style.configure("TLabel", background=self.colors["panel"], foreground=self.colors["text"], font=("Segoe UI", 10))
        self.style.configure("TEntry", fieldbackground="white", bordercolor=self.colors["line"], lightcolor=self.colors["line"], padding=6)
        self.style.map("TEntry", bordercolor=[("focus", self.colors["primary"])])
        self.style.configure("TCombobox", fieldbackground="white", bordercolor=self.colors["line"], lightcolor=self.colors["line"], padding=6)
        self.style.configure("Treeview", background="white", fieldbackground="white", foreground=self.colors["text"], rowheight=30, borderwidth=0, font=("Segoe UI", 10))
        self.style.configure("Treeview.Heading", background="#e2e8f0", foreground=self.colors["text"], relief="flat", font=("Segoe UI", 10, "bold"))
        self.style.map("Treeview.Heading", background=[("active", "#cbd5e1")])
        self.style.map("Treeview", background=[("selected", "#bfdbfe")], foreground=[("selected", self.colors["text"])])

    def login_window(self):
        self.login_frame = ttk.Frame(self.root, style="App.TFrame")
        self.login_frame.pack(fill="both", expand=True)
        self.root.configure(bg=self.colors["login_bg"])

        login_bg = tk.Frame(self.login_frame, bg=self.colors["login_bg"])
        login_bg.pack(fill="both", expand=True, padx=34, pady=34)

        shell = tk.Frame(login_bg, bg=self.colors["panel"], highlightthickness=1,
                         highlightbackground="#cbd5e1")
        shell.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.88, relheight=0.82)

        brand = tk.Frame(shell, bg=self.colors["navy"])
        brand.place(relx=0, rely=0, relwidth=0.48, relheight=1)

        tk.Label(brand, text="EMS", bg=self.colors["accent"], fg="white",
                 font=("Segoe UI", 15, "bold"), width=5, height=2).place(x=42, y=42)
        tk.Label(brand, text="Employee\nManagement\nSystem", bg=self.colors["navy"], fg="white",
                 justify="left", font=("Segoe UI", 32, "bold")).place(x=42, y=125)
        tk.Label(brand, text="Oracle database dashboard for employee records", bg=self.colors["navy"],
                 fg="#cbd5e1", justify="left", font=("Segoe UI", 11)).place(x=46, y=318)

        stat_strip = tk.Frame(brand, bg="#111c33", highlightthickness=1, highlightbackground="#24324a")
        stat_strip.place(x=42, y=385, width=330, height=88)
        tk.Label(stat_strip, text="Secure Login", bg="#111c33", fg="#5eead4",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=18, pady=(14, 2))
        tk.Label(stat_strip, text="Role based access for admin and user accounts", bg="#111c33",
                 fg="#dbeafe", font=("Segoe UI", 10)).pack(anchor="w", padx=18)

        card = tk.Frame(shell, bg=self.colors["panel"])
        card.place(relx=0.57, rely=0.5, anchor="w", relwidth=0.35, height=380)

        tk.Label(card, text="Welcome Back", bg=self.colors["panel"], fg=self.colors["text"],
                 font=("Segoe UI", 25, "bold")).pack(anchor="w", pady=(8, 5))
        tk.Label(card, text="Sign in with your employee system account", bg=self.colors["panel"], fg=self.colors["muted"],
                 font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 30))

        form = tk.Frame(card, bg=self.colors["panel"])
        form.pack(fill="x")

        user_box = tk.Frame(form, bg="#f8fafc", highlightthickness=1, highlightbackground=self.colors["line"])
        user_box.pack(fill="x", pady=(0, 16))
        tk.Label(user_box, text="USERNAME", bg="#f8fafc", fg=self.colors["muted"],
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=12, pady=(9, 2))
        self.ent_user = ttk.Entry(user_box, font=("Segoe UI", 11))
        self.ent_user.pack(fill="x", padx=10, pady=(0, 10), ipady=5)

        pass_box = tk.Frame(form, bg="#f8fafc", highlightthickness=1, highlightbackground=self.colors["line"])
        pass_box.pack(fill="x", pady=(0, 22))
        tk.Label(pass_box, text="PASSWORD", bg="#f8fafc", fg=self.colors["muted"],
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=12, pady=(9, 2))
        self.ent_pass = ttk.Entry(pass_box, show="*", font=("Segoe UI", 11))
        self.ent_pass.pack(fill="x", padx=10, pady=(0, 10), ipady=5)
        self.ent_pass.bind("<Return>", lambda _: self.authenticate())

        self.make_button(card, "Login", self.authenticate, self.colors["primary"]).pack(fill="x", ipady=7)
        tk.Label(card, text="Advanced Database System Assignment", bg=self.colors["panel"],
                 fg=self.colors["muted"], font=("Segoe UI", 9)).pack(anchor="center", pady=(22, 0))
        self.ent_user.focus_set()

    def authenticate(self):
        u = self.ent_user.get()
        p = self.ent_pass.get()
        self.cursor.execute("SELECT Role FROM USERS WHERE Username = :1 AND Password = :2", (u, p))
        row = self.cursor.fetchone()
        
        if row:
            self.current_user = u
            self.current_role = row[0]
            self.login_frame.destroy()
            self.main_dashboard()
        else:
            messagebox.showerror("Error", "Invalid Credentials")

    def main_dashboard(self):
        self.root.configure(bg=self.colors["bg"])
        top_frame = tk.Frame(self.root, bg=self.colors["primary"], height=82)
        top_frame.pack(side="top", fill="x")
        top_frame.pack_propagate(False)
        tk.Label(top_frame, text="Employee Management System", bg=self.colors["primary"], fg="white",
                 font=("Segoe UI", 22, "bold")).pack(side="left", padx=26)
        tk.Label(top_frame, text=f"{self.current_user}  |  {self.current_role}", bg=self.colors["primary"], fg="#dbeafe",
                 font=("Segoe UI", 11, "bold")).pack(side="right", padx=26)

        content = tk.Frame(self.root, bg=self.colors["bg"])
        content.pack(fill="both", expand=True, padx=24, pady=20)

        form_frame = tk.Frame(content, bg=self.colors["panel"], highlightthickness=1, highlightbackground=self.colors["line"])
        form_frame.pack(fill="x")
        tk.Label(form_frame, text="Employee Details", bg=self.colors["panel"], fg=self.colors["text"],
                 font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=3, sticky="w", padx=18, pady=(16, 2))
        tk.Label(form_frame, text="Oracle employee record workspace", bg=self.colors["panel"], fg=self.colors["muted"],
                 font=("Segoe UI", 9)).grid(row=1, column=0, columnspan=3, sticky="w", padx=18, pady=(0, 12))

        labels = self.labels
        self.entries = {}
        for i, text in enumerate(labels):
            row = (i // 3) + 2
            col = i % 3
            field_box = tk.Frame(form_frame, bg="#f8fafc", highlightthickness=1, highlightbackground=self.colors["line"])
            field_box.grid(row=row, column=col, padx=(18 if col == 0 else 8, 18 if col == 2 else 8), pady=8, sticky="ew")

            tk.Label(field_box, text=text.upper(), bg="#f8fafc", fg=self.colors["muted"],
                     font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=12, pady=(8, 2))
            if text == "Gender":
                ent = ttk.Combobox(field_box, values=["Male", "Female", "Other"], font=("Segoe UI", 10))
            else:
                ent = ttk.Entry(field_box, font=("Segoe UI", 10))
            ent.pack(fill="x", padx=10, pady=(0, 10), ipady=4)
            self.entries[text] = ent

        self.entries["Name"].bind("<KeyRelease>", self.live_search)
        self.entries["Department"].bind("<KeyRelease>", self.live_search)

        for col in (0, 1, 2):
            form_frame.grid_columnconfigure(col, weight=1)

        search_box = tk.Frame(form_frame, bg="#f1f5f9", highlightthickness=1, highlightbackground=self.colors["line"])
        search_box.grid(row=4, column=0, columnspan=3, padx=18, pady=(10, 8), sticky="ew")
        search_box.grid_columnconfigure(1, weight=1)
        search_box.grid_columnconfigure(3, weight=1)

        tk.Label(search_box, text="Min Salary", bg="#f1f5f9", fg=self.colors["muted"],
                 font=("Segoe UI", 9, "bold")).grid(row=0, column=0, padx=(14, 6), pady=12, sticky="w")
        self.ent_min_sal = ttk.Entry(search_box, font=("Segoe UI", 10))
        self.ent_min_sal.grid(row=0, column=1, padx=(0, 18), pady=12, sticky="ew", ipady=4)
        self.ent_min_sal.bind("<KeyRelease>", self.live_search)
        tk.Label(search_box, text="Max Salary", bg="#f1f5f9", fg=self.colors["muted"],
                 font=("Segoe UI", 9, "bold")).grid(row=0, column=2, padx=(14, 6), pady=12, sticky="w")
        self.ent_max_sal = ttk.Entry(search_box, font=("Segoe UI", 10))
        self.ent_max_sal.grid(row=0, column=3, padx=(0, 14), pady=12, sticky="ew", ipady=4)
        self.ent_max_sal.bind("<KeyRelease>", self.live_search)

        btn_frame = tk.Frame(form_frame, bg=self.colors["panel"])
        btn_frame.grid(row=5, column=0, columnspan=3, sticky="w", padx=18, pady=(6, 18))

        self.btn_insert = self.make_button(btn_frame, "Insert", self.insert_data, self.colors["success"])
        self.btn_update = self.make_button(btn_frame, "Update", self.update_data, self.colors["warning"])
        self.btn_delete = self.make_button(btn_frame, "Delete", self.delete_data, self.colors["danger"])
        btn_search = self.make_button(btn_frame, "Smart Search", self.smart_search, self.colors["primary"])
        btn_show = self.make_button(btn_frame, "Show All", self.show_all, "#475569")
        self.btn_export = self.make_button(btn_frame, "Export CSV", self.export_data, "#0891b2")
        self.btn_txt = self.make_button(btn_frame, "Export TXT", self.export_txt, "#7c3aed")

        btns = [self.btn_insert, self.btn_update, self.btn_delete, btn_search, btn_show, self.btn_export, self.btn_txt]
        for i, b in enumerate(btns):
            b.grid(row=0, column=i, padx=(0, 10), ipady=4)

        if self.current_role == "USER":
            self.btn_insert.config(state="disabled")
            self.btn_update.config(state="disabled")
            self.btn_delete.config(state="disabled")
            self.btn_export.config(state="disabled")
            self.btn_txt.config(state="disabled")

        table_panel = tk.Frame(content, bg=self.colors["panel"], highlightthickness=1, highlightbackground=self.colors["line"])
        table_panel.pack(fill="both", expand=True)
        tk.Label(table_panel, text="Employee Records", bg=self.colors["panel"], fg=self.colors["text"],
                 font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=18, pady=(14, 8))

        tree_frame = tk.Frame(table_panel, bg=self.colors["panel"])
        tree_frame.pack(padx=18, pady=(0, 12), fill="both", expand=True)
        
        self.tree = ttk.Treeview(tree_frame, columns=labels, show="headings")
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        
        for col in labels:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))
            self.tree.column(col, width=130, anchor="center")
        
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self.auto_fill)

        self.stats_label = tk.Label(table_panel, text="", bg=self.colors["panel"], fg=self.colors["primary"],
                                    font=("Segoe UI", 10, "bold"), justify="left", wraplength=1050)
        self.stats_label.pack(anchor="w", padx=18, pady=(0, 14))
        self.show_all()

    def make_button(self, parent, text, command, color):
        return tk.Button(parent, text=text, command=command, width=13, bg=color, fg="white",
                         activebackground=color, activeforeground="white", relief="flat",
                         bd=0, cursor="hand2", font=("Segoe UI", 10, "bold"),
                         disabledforeground="#cbd5e1")

    def validate(self):
        try:
            if not self.entries["Employee ID"].get().isdigit():
                raise ValueError("ID must be numeric")
            if not all(x.isalpha() or x.isspace() for x in self.entries["Name"].get().strip()):
                raise ValueError("Name alphabets only")
            if not self.entries["Name"].get().strip():
                raise ValueError("Name is required")
            if not self.entries["Department"].get().strip():
                raise ValueError("Department is required")
            if not all(x.isalpha() or x.isspace() for x in self.entries["Department"].get().strip()):
                raise ValueError("Department alphabets only")
            if float(self.entries["Salary"].get()) < 0:
                raise ValueError("Salary non-negative")
            contact = self.entries["Contact"].get().strip()
            if not contact.isdigit():
                raise ValueError("Contact number must be numeric")
            if len(contact) < 7 or len(contact) > 15:
                raise ValueError("Contact number length must be 7 to 15 digits")
            return True
        except Exception as e:
            messagebox.showerror("Validation Error", str(e))
            return False

    def get_form_values(self):
        return tuple(self.entries[label].get().strip() for label in self.labels)

    def fetch_employee_by_id(self, emp_id):
        self.cursor.execute(f"SELECT {self.employee_select_columns} FROM Employees WHERE EmpID = :1", (emp_id,))
        row = self.cursor.fetchone()
        return tuple(str(value) for value in row) if row else None

    def contact_exists(self, contact, exclude_emp_id=None):
        if exclude_emp_id:
            self.cursor.execute(f"SELECT COUNT(*) FROM Employees WHERE {self.contact_column} = :1 AND EmpID <> :2",
                                (contact, exclude_emp_id))
        else:
            self.cursor.execute(f"SELECT COUNT(*) FROM Employees WHERE {self.contact_column} = :1", (contact,))
        return self.cursor.fetchone()[0] > 0

    def insert_data(self):
        if self.validate():
            try:
                data = {l: self.entries[l].get() for l in self.entries}
                if self.contact_exists(data["Contact"]):
                    messagebox.showerror("Error", "Duplicate Contact Number")
                    return
                self.cursor.execute(f"INSERT INTO Employees (EmpID, Name, Gender, Department, Salary, {self.contact_column}) VALUES (:1, :2, :3, :4, :5, :6)", 
                                   (data["Employee ID"], data["Name"], data["Gender"], data["Department"], data["Salary"], data["Contact"]))
                self.conn.commit()
                messagebox.showinfo("Success", "Employee Inserted Successfully")
                self.show_all()
                self.selected_record_values = self.get_form_values()
            except oracledb.IntegrityError:
                messagebox.showerror("Error", "Duplicate Employee ID")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def update_data(self):
        if self.validate():
            try:
                current_values = self.get_form_values()
                emp_id = current_values[0]
                original_values = self.selected_record_values

                if not original_values or original_values[0] != emp_id:
                    original_values = self.fetch_employee_by_id(emp_id)

                if original_values and tuple(str(value) for value in original_values) == current_values:
                    messagebox.showinfo("No changes", "No changes detected")
                    return

                if self.contact_exists(current_values[5], exclude_emp_id=emp_id):
                    messagebox.showerror("Error", "Duplicate Contact Number")
                    return

                query = f"UPDATE Employees SET Name=:1, Gender=:2, Department=:3, Salary=:4, {self.contact_column}=:5 WHERE EmpID=:6"
                params = (self.entries["Name"].get(), self.entries["Gender"].get(), self.entries["Department"].get(), 
                          self.entries["Salary"].get(), self.entries["Contact"].get(), self.entries["Employee ID"].get())
                self.cursor.execute(query, params)
                self.conn.commit()
                messagebox.showinfo("Success", "Employee Updated Successfully")
                self.show_all()
                self.selected_record_values = current_values
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def delete_data(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this record?"):
            self.cursor.execute("DELETE FROM Employees WHERE EmpID = :1", (self.entries["Employee ID"].get(),))
            self.conn.commit()
            self.selected_record_values = None
            self.show_all()

    def live_search(self, _=None):
        self.smart_search(ignore_id=True)

    def smart_search(self, ignore_id=False):
        eid, name, dept = self.entries["Employee ID"].get(), self.entries["Name"].get(), self.entries["Department"].get()
        min_s, max_s = self.ent_min_sal.get(), self.ent_max_sal.get()
        
        query = f"SELECT {self.employee_select_columns} FROM Employees WHERE 1=1"
        params = {}
        
        if eid and not ignore_id:
            query += " AND EmpID = :eid"
            params["eid"] = eid
        else:
            if name:
                query += " AND UPPER(Name) LIKE :name"
                params["name"] = f"%{name.upper()}%"
            if dept:
                query += " AND UPPER(Department) LIKE :dept"
                params["dept"] = f"%{dept.upper()}%"
            if min_s:
                query += " AND Salary >= :min_salary"
                params["min_salary"] = min_s
            if max_s:
                query += " AND Salary <= :max_salary"
                params["max_salary"] = max_s

        self.cursor.execute(query, params)
        self.update_tree(self.cursor.fetchall())

    def update_tree(self, rows):
        self.tree.delete(*self.tree.get_children())
        rows = [tuple(r) for r in rows]
        if self.sort_column:
            rows = self.sort_rows(rows)

        for i, r in enumerate(rows):
            tag = self.salary_tag(r, i)
            self.tree.insert("", "end", values=r, tags=(tag,))
        self.tree.tag_configure("high_salary", background="#dcfce7")
        self.tree.tag_configure("mid_salary", background="white")
        self.tree.tag_configure("low_salary", background="#fef3c7")
        self.tree.tag_configure("normal_even", background="white")
        self.tree.tag_configure("normal_odd", background=self.colors["table"])
        self.update_stats()

    def salary_tag(self, row, index):
        try:
            salary = float(row[4])
        except (ValueError, TypeError):
            return "normal_even" if index % 2 == 0 else "normal_odd"
        if salary > 1000:
            return "high_salary"
        if salary < 500:
            return "low_salary"
        return "mid_salary"

    def update_stats(self):
        self.cursor.execute("SELECT AVG(Salary), MAX(Salary), MIN(Salary), SUM(Salary) FROM Employees")
        res = self.cursor.fetchone()
        self.cursor.execute("SELECT Department, COUNT(*) FROM Employees GROUP BY Department ORDER BY Department")
        dept_counts = self.cursor.fetchall()
        dept_text = " | ".join(f"{dept}: {count}" for dept, count in dept_counts)
        if res[0]:
            self.stats_label.config(
                text=f"Avg: {res[0]:.2f} | Max: {res[1]} | Min: {res[2]} | Total Expense: {res[3]}\nDepartment Count: {dept_text}"
            )
        else:
            self.stats_label.config(text="No records found")

    def show_all(self):
        self.cursor.execute(f"SELECT {self.employee_select_columns} FROM Employees")
        self.update_tree(self.cursor.fetchall())

    def auto_fill(self, _):
        if not self.tree.selection(): return
        item = self.tree.selection()[0]
        vals = self.tree.item(item, "values")
        for i, label in enumerate(self.entries):
            self.entries[label].delete(0, "end")
            self.entries[label].insert(0, vals[i])
        self.selected_record_values = tuple(str(value) for value in vals)

    def export_data(self):
        with open("employees.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name", "Gender", "Dept", "Salary", "Contact"])
            for item in self.tree.get_children():
                writer.writerow(self.tree.item(item, "values"))
        messagebox.showinfo("Exported", "Data saved to employees.csv")

    def export_txt(self):
        with open("employees.txt", "w") as f:
            f.write("ID\tName\tGender\tDept\tSalary\tContact\n")
            for item in self.tree.get_children():
                f.write("\t".join(str(value) for value in self.tree.item(item, "values")) + "\n")
        messagebox.showinfo("Exported", "Data saved to employees.txt")

    def sort_treeview(self, col):
        rows = [self.tree.item(k)["values"] for k in self.tree.get_children()]
        if self.sort_column == col:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = col
            self.sort_reverse = False
        self.refresh_tree_headings()
        self.update_tree(rows)

    def sort_rows(self, rows):
        index = self.labels.index(self.sort_column)
        return sorted(rows, key=lambda row: self.sort_key(row[index], self.sort_column), reverse=self.sort_reverse)

    def sort_key(self, value, column):
        if column in ("Employee ID", "Salary", "Contact"):
            try:
                return float(value)
            except (ValueError, TypeError):
                return 0
        return str(value).lower()

    def refresh_tree_headings(self):
        for col in self.labels:
            arrow = ""
            if col == self.sort_column:
                arrow = " ↓" if self.sort_reverse else " ↑"
            self.tree.heading(col, text=f"{col}{arrow}", command=lambda c=col: self.sort_treeview(c))

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeSystem(root)
    root.mainloop()
