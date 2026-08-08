import tkinter as tk
from tkinter import ttk, messagebox
from Patient_Management import PatientManagement
from priority import priority_Management
from surgery_management import surgery_mangment
class HospitalDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Surgery Management System")
        self.root.geometry("1200x720")
        self.root.minsize(1000, 650)

        self.bg = "#f4f7fb"
        self.sidebar = "#172033"
        self.primary = "#2563eb"
        self.text = "#172033"
        self.muted = "#64748b"
        self.card_color = "#ffffff"
        self.danger = "#dc2626"
        self.success = "#16a34a"
        self.warning = "#d97706"

        self.root.configure(bg=self.bg)

        self.patient_manager = PatientManagement()
        self.priority_manager = priority_Management()
        self.surgery_manager = surgery_mangment()

        self.setup_style()
        self.build_layout()
        self.show_dashboard()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="white",
            fieldbackground="white",
            foreground=self.text,
            rowheight=38,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Treeview.Heading",
            background="#eef2f7",
            foreground=self.text,
            font=("Segoe UI Semibold", 10),
            padding=8,
        )
        style.map("Treeview", background=[("selected", "#dbeafe")])

        style.configure(
            "TEntry",
            padding=9,
            font=("Segoe UI", 10),
        )

        style.configure(
            "TCombobox",
            padding=8,
            font=("Segoe UI", 10),
        )

    def build_layout(self):
        self.sidebar_frame = tk.Frame(self.root, bg=self.sidebar, width=230)
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False)

        brand = tk.Frame(self.sidebar_frame, bg=self.sidebar)
        brand.pack(fill="x", padx=20, pady=(28, 35))

        tk.Label(
            brand, text="✚", bg=self.sidebar, fg="#60a5fa",
            font=("Segoe UI", 28, "bold")
        ).pack(side="left")

        title_box = tk.Frame(brand, bg=self.sidebar)
        title_box.pack(side="left", padx=10)

        tk.Label(
            title_box, text="SURGERY", bg=self.sidebar, fg="white",
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w")
        tk.Label(
            title_box, text="MANAGEMENT", bg=self.sidebar, fg="#94a3b8",
            font=("Segoe UI", 8)
        ).pack(anchor="w")

        self.nav_buttons = {}
        nav_items = [
            ("Dashboard", self.show_dashboard),
            ("Patients", self.show_patients),
            ("Surgeries", self.show_surgeries),
            ("Priority Queue", self.show_priority),
            ("Rooms", self.show_rooms),
        ]

        for name, command in nav_items:
            btn = tk.Button(
                self.sidebar_frame,
                text="  " + name,
                command=command,
                anchor="w",
                bd=0,
                relief="flat",
                bg=self.sidebar,
                fg="#cbd5e1",
                activebackground="#263653",
                activeforeground="white",
                font=("Segoe UI", 10, "bold"),
                padx=20,
                pady=13,
                cursor="hand2",
            )
            btn.pack(fill="x", padx=10, pady=2)
            self.nav_buttons[name] = btn

        tk.Label(
            self.sidebar_frame,
            text="Hospital Operations",
            bg=self.sidebar,
            fg="#64748b",
            font=("Segoe UI", 8),
        ).pack(side="bottom", pady=20)

        self.main = tk.Frame(self.root, bg=self.bg)
        self.main.pack(side="left", fill="both", expand=True)

        self.header = tk.Frame(self.main, bg="white", height=72)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        self.page_title = tk.Label(
            self.header, text="Dashboard",
            bg="white", fg=self.text,
            font=("Segoe UI", 20, "bold")
        )
        self.page_title.pack(side="left", padx=28, pady=20)

        self.content = tk.Frame(self.main, bg=self.bg)
        self.content.pack(fill="both", expand=True, padx=28, pady=24)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def set_active(self, name):
        for key, btn in self.nav_buttons.items():
            btn.configure(
                bg="#263653" if key == name else self.sidebar,
                fg="white" if key == name else "#cbd5e1"
            )

    def page_header(self, title, subtitle):
        self.page_title.config(text=title)
        tk.Label(
            self.content, text=subtitle,
            bg=self.bg, fg=self.muted,
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(0, 18))

    def card(self, parent):
        return tk.Frame(parent, bg=self.card_color, bd=0, highlightthickness=1,
                        highlightbackground="#e5e7eb")

    def get_patients(self):
        try:
            return self.patient_manager.show_patients()
        except Exception:
            return getattr(self.patient_manager, "patients", [])

    def get_surgeries(self):
        try:
            return self.surgery_manager.surgeries
        except Exception:
            return []

    def show_dashboard(self):
        self.set_active("Dashboard")
        self.clear_content()
        self.page_header(
            "Dashboard",
            "Overview of patients, scheduled surgeries and operating rooms."
        )

        patients = self.get_patients()
        surgeries = self.get_surgeries()
        scheduled = [s for s in surgeries if s.get("status") == "Scheduled"]
        completed = [s for s in surgeries if s.get("status") == "Completed"]

        try:
            free_rooms = len(self.surgery_manager.a_rooms())
        except Exception:
            free_rooms = 0

        critical = len([
            p for p in patients
            if str(p.get("urgency_level", "")).lower() in
            ("critical", "high", "4", "5")
        ])

        stats = [
            ("Total Patients", len(patients), "Registered patients"),
            ("Scheduled Surgeries", len(scheduled), "Upcoming operations"),
            ("Completed", len(completed), "Finished surgeries"),
            ("Available Rooms", free_rooms, "Currently free"),
        ]

        cards = tk.Frame(self.content, bg=self.bg)
        cards.pack(fill="x")

        for title, value, sub in stats:
            c = self.card(cards)
            c.pack(side="left", fill="both", expand=True, padx=(0, 14))
            tk.Label(c, text=title, bg="white", fg=self.muted,
                     font=("Segoe UI", 10)).pack(anchor="w", padx=18, pady=(17, 4))
            tk.Label(c, text=str(value), bg="white", fg=self.text,
                     font=("Segoe UI", 25, "bold")).pack(anchor="w", padx=18)
            tk.Label(c, text=sub, bg="white", fg="#94a3b8",
                     font=("Segoe UI", 9)).pack(anchor="w", padx=18, pady=(2, 17))

        bottom = tk.Frame(self.content, bg=self.bg)
        bottom.pack(fill="both", expand=True, pady=20)

        left = self.card(bottom)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(left, text="Recent Surgeries", bg="white", fg=self.text,
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=18, pady=18)

        recent = ttk.Treeview(
            left,
            columns=("patient", "doctor", "type", "date", "status"),
            show="headings",
            height=9
        )
        for col, heading, width in [
            ("patient", "Patient", 150),
            ("doctor", "Doctor", 140),
            ("type", "Surgery", 140),
            ("date", "Date", 110),
            ("status", "Status", 100),
        ]:
            recent.heading(col, text=heading)
            recent.column(col, width=width, anchor="w")
        recent.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        for s in surgeries[-10:]:
            recent.insert(
                "", "end",
                values=(
                    s.get("patient_name", ""),
                    s.get("doctor", ""),
                    s.get("surgery_type", ""),
                    s.get("date", ""),
                    s.get("status", ""),
                )
            )

        right = self.card(bottom)
        right.pack(side="left", fill="both", padx=(10, 0))

        tk.Label(right, text="System Snapshot", bg="white", fg=self.text,
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=18, pady=18)

        items = [
            ("Patients", len(patients)),
            ("Critical / High Priority", critical),
            ("Scheduled", len(scheduled)),
            ("Free Rooms", free_rooms),
        ]

        for label, value in items:
            row = tk.Frame(right, bg="white")
            row.pack(fill="x", padx=18, pady=8)
            tk.Label(row, text=label, bg="white", fg=self.muted,
                     font=("Segoe UI", 10)).pack(side="left")
            tk.Label(row, text=str(value), bg="white", fg=self.primary,
                     font=("Segoe UI", 11, "bold")).pack(side="right")

    def show_patients(self):
        self.set_active("Patients")
        self.clear_content()
        self.page_header("Patients", "Manage patient records.")

        actions = tk.Frame(self.content, bg=self.bg)
        actions.pack(fill="x", pady=(0, 15))

        tk.Button(
            actions, text="+ Add Patient", command=self.add_patient_window,
            bg=self.primary, fg="white", bd=0, padx=18, pady=9,
            font=("Segoe UI", 10, "bold"), cursor="hand2"
        ).pack(side="left")

        search_var = tk.StringVar()
        search = ttk.Entry(actions, textvariable=search_var, width=35)
        search.pack(side="right", ipady=2)
        search.insert(0, "")

        table_card = self.card(self.content)
        table_card.pack(fill="both", expand=True)

        tree = ttk.Treeview(
            table_card,
            columns=("id", "name", "age", "diagnosis", "urgency"),
            show="headings"
        )
        headings = [
            ("id", "Patient ID", 130),
            ("name", "Name", 180),
            ("age", "Age", 70),
            ("diagnosis", "Diagnosis", 250),
            ("urgency", "Urgency", 120),
        ]
        for col, heading, width in headings:
            tree.heading(col, text=heading)
            tree.column(col, width=width, anchor="w")
        tree.pack(fill="both", expand=True, padx=15, pady=15)

        def refresh():
            for item in tree.get_children():
                tree.delete(item)
            query = search_var.get().strip().lower()
            data = self.get_patients()
            if query:
                data = [
                    p for p in data
                    if query in str(p.get("patient_id", "")).lower()
                    or query in str(p.get("name", "")).lower()
                ]
            for p in data:
                tree.insert(
                    "", "end",
                    values=(
                        p.get("patient_id", ""),
                        p.get("name", ""),
                        p.get("age", ""),
                        p.get("diagnosis", ""),
                        p.get("urgency_level", ""),
                    )
                )

        search_var.trace_add("write", lambda *_: refresh())
        refresh()

        buttons = tk.Frame(self.content, bg=self.bg)
        buttons.pack(fill="x", pady=(12, 0))

        def selected_patient():
            item = tree.focus()
            if not item:
                messagebox.showwarning("Select Patient", "Please select a patient first.")
                return None
            values = tree.item(item, "values")
            return values

        tk.Button(
            buttons, text="Edit", command=lambda: self.edit_patient_window(selected_patient()),
            bg="#e2e8f0", fg=self.text, bd=0, padx=18, pady=8,
            font=("Segoe UI", 9, "bold")
        ).pack(side="left", padx=(0, 8))

        def delete():
            values = selected_patient()
            if not values:
                return
            if messagebox.askyesno("Delete Patient", "Delete this patient?"):
                result = self.patient_manager.delete_patient(values[0])
                messagebox.showinfo("Result", result)
                refresh()

        tk.Button(
            buttons, text="Delete", command=delete,
            bg="#fee2e2", fg=self.danger, bd=0, padx=18, pady=8,
            font=("Segoe UI", 9, "bold")
        ).pack(side="left")

    def patient_form(self, title, values=None, update=False):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("470x500")
        win.resizable(False, False)
        win.configure(bg="white")

        tk.Label(win, text=title, bg="white", fg=self.text,
                 font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=28, pady=(25, 5))

        form = tk.Frame(win, bg="white")
        form.pack(fill="both", expand=True, padx=28, pady=15)

        fields = [
            ("Patient ID", "id"),
            ("Name", "name"),
            ("Age", "age"),
            ("Diagnosis", "diagnosis"),
            ("Urgency Level", "urgency"),
        ]

        entries = {}
        for label, key in fields:
            tk.Label(form, text=label, bg="white", fg=self.muted,
                     font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(8, 4))
            e = ttk.Entry(form)
            e.pack(fill="x")
            entries[key] = e

        if values:
            for key, value in zip(["id", "name", "age", "diagnosis", "urgency"], values):
                entries[key].insert(0, value)
            entries["id"].configure(state="disabled")

        def save():
            try:
                if update:
                    result = self.patient_manager.update_patient(
                        values[0],
                        entries["name"].get().strip(),
                        int(entries["age"].get()),
                        entries["diagnosis"].get().strip(),
                        entries["urgency"].get().strip()
                    )
                else:
                    result = self.patient_manager.add_patient(
                        entries["id"].get().strip().upper(),
                        entries["name"].get().strip(),
                        int(entries["age"].get()),
                        entries["diagnosis"].get().strip(),
                        entries["urgency"].get().strip()
                    )
                messagebox.showinfo("Success", result)
                win.destroy()
                self.show_patients()
            except ValueError:
                messagebox.showerror("Invalid Data", "Age must be a number.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(
            win, text="Save Patient", command=save,
            bg=self.primary, fg="white", bd=0, padx=20, pady=10,
            font=("Segoe UI", 10, "bold"), cursor="hand2"
        ).pack(fill="x", padx=28, pady=20)

    def add_patient_window(self):
        self.patient_form("Add New Patient")

    def edit_patient_window(self, values):
        if values:
            self.patient_form("Edit Patient", values, True)

    def show_surgeries(self):
        self.set_active("Surgeries")
        self.clear_content()
        self.page_header("Surgeries", "Schedule and monitor surgical operations.")

        top = tk.Frame(self.content, bg=self.bg)
        top.pack(fill="x", pady=(0, 15))

        tk.Button(
            top, text="+ Schedule Surgery", command=self.add_surgery_window,
            bg=self.primary, fg="white", bd=0, padx=18, pady=9,
            font=("Segoe UI", 10, "bold"), cursor="hand2"
        ).pack(side="left")

        card = self.card(self.content)
        card.pack(fill="both", expand=True)

        tree = ttk.Treeview(
            card,
            columns=("patient", "diagnosis", "doctor", "type", "date", "room", "status"),
            show="headings"
        )
        for col, heading, width in [
            ("patient", "Patient", 140),
            ("diagnosis", "Diagnosis", 160),
            ("doctor", "Doctor", 140),
            ("type", "Surgery Type", 130),
            ("date", "Date", 110),
            ("room", "Room", 70),
            ("status", "Status", 100),
        ]:
            tree.heading(col, text=heading)
            tree.column(col, width=width, anchor="w")
        tree.pack(fill="both", expand=True, padx=15, pady=15)

        for s in self.get_surgeries():
            tree.insert("", "end", values=(
                s.get("patient_name", ""),
                s.get("diagnosis", ""),
                s.get("doctor", ""),
                s.get("surgery_type", ""),
                s.get("date", ""),
                s.get("room", ""),
                s.get("status", ""),
            ))

        buttons = tk.Frame(self.content, bg=self.bg)
        buttons.pack(fill="x", pady=(12, 0))

        def get_selected():
            item = tree.focus()
            if not item:
                messagebox.showwarning("Select Surgery", "Please select a surgery.")
                return None
            return tree.item(item, "values")

        def complete():
            v = get_selected()
            if not v:
                return
            result = self.surgery_manager.complete_surgery_by_id(v[0]) \
                if hasattr(self.surgery_manager, "complete_surgery_by_id") \
                else self.complete_by_patient_id(v[0])
            messagebox.showinfo("Result", result)
            self.show_surgeries()

        def delete():
            v = get_selected()
            if not v:
                return
            if messagebox.askyesno("Delete Surgery", "Delete this surgery?"):
                result = self.delete_by_patient_id(v[0])
                messagebox.showinfo("Result", result)
                self.show_surgeries()

        tk.Button(
            buttons, text="Mark Completed", command=complete,
            bg="#dcfce7", fg=self.success, bd=0, padx=18, pady=8,
            font=("Segoe UI", 9, "bold")
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            buttons, text="Delete", command=delete,
            bg="#fee2e2", fg=self.danger, bd=0, padx=18, pady=8,
            font=("Segoe UI", 9, "bold")
        ).pack(side="left")

    def add_surgery_window(self):
        win = tk.Toplevel(self.root)
        win.title("Schedule Surgery")
        win.geometry("500x520")
        win.resizable(False, False)
        win.configure(bg="white")

        tk.Label(win, text="Schedule Surgery", bg="white", fg=self.text,
                 font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=28, pady=(25, 5))

        form = tk.Frame(win, bg="white")
        form.pack(fill="both", expand=True, padx=28)

        labels = ["Patient ID", "Surgery Type", "Doctor", "Date"]
        entries = []

        for label in labels:
            tk.Label(form, text=label, bg="white", fg=self.muted,
                     font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10, 4))
            e = ttk.Entry(form)
            e.pack(fill="x")
            entries.append(e)

        def save():
            patient_id, surgery_type, doctor, date = [e.get().strip() for e in entries]

            patients = self.get_patients()
            patient = next(
                (p for p in patients if str(p.get("patient_id", "")).strip().upper()
                 == patient_id.upper()), None
            )

            if not patient:
                messagebox.showerror("Patient Not Found", "No patient with this ID exists.")
                return

            try:
                rooms = self.surgery_manager.a_rooms()
            except Exception:
                rooms = []

            if not rooms:
                messagebox.showerror("No Rooms", "No available operation rooms.")
                return

            surgery = {
                "patient_id": patient["patient_id"],
                "patient_name": patient["name"],
                "diagnosis": patient["diagnosis"],
                "urgency_level": patient["urgency_level"],
                "doctor": doctor,
                "surgery_type": surgery_type,
                "date": date,
                "room": rooms[0],
                "status": "Scheduled",
            }

            self.surgery_manager.surgeries.append(surgery)
            self.surgery_manager.save_data()

            messagebox.showinfo(
                "Success",
                f"Surgery scheduled successfully.\nAssigned Room: {rooms[0]}"
            )
            win.destroy()
            self.show_surgeries()

        tk.Button(
            win, text="Schedule Surgery", command=save,
            bg=self.primary, fg="white", bd=0, padx=20, pady=10,
            font=("Segoe UI", 10, "bold"), cursor="hand2"
        ).pack(fill="x", padx=28, pady=22)

    def complete_by_patient_id(self, patient_id):
        for surgery in self.surgery_manager.surgeries:
            if surgery.get("patient_id") == patient_id:
                surgery["status"] = "Completed"
                self.surgery_manager.save_data()
                return "Surgery completed successfully"
        return "Surgery not found"

    def delete_by_patient_id(self, patient_id):
        for surgery in self.surgery_manager.surgeries:
            if surgery.get("patient_id") == patient_id:
                self.surgery_manager.surgeries.remove(surgery)
                self.surgery_manager.save_data()
                return "Surgery deleted successfully"
        return "Surgery not found"

    def show_priority(self):
        self.set_active("Priority Queue")
        self.clear_content()
        self.page_header(
            "Priority Queue",
            "Patients sorted by urgency level."
        )

        try:
            self.priority_manager.load_patients()
            patients = self.priority_manager.sort_patients()
        except Exception:
            patients = sorted(
                self.get_patients(),
                key=lambda p: p.get("urgency_level", ""),
                reverse=True
            )

        card = self.card(self.content)
        card.pack(fill="both", expand=True)

        tree = ttk.Treeview(
            card,
            columns=("rank", "id", "name", "diagnosis", "urgency"),
            show="headings"
        )
        for col, heading, width in [
            ("rank", "#", 60),
            ("id", "Patient ID", 150),
            ("name", "Name", 190),
            ("diagnosis", "Diagnosis", 260),
            ("urgency", "Urgency", 130),
        ]:
            tree.heading(col, text=heading)
            tree.column(col, width=width, anchor="w")
        tree.pack(fill="both", expand=True, padx=15, pady=15)

        for index, p in enumerate(patients, 1):
            tree.insert("", "end", values=(
                index,
                p.get("patient_id", ""),
                p.get("name", ""),
                p.get("diagnosis", ""),
                p.get("urgency_level", ""),
            ))

        tk.Button(
            self.content,
            text="Refresh Priority Queue",
            command=self.show_priority,
            bg=self.primary, fg="white", bd=0, padx=18, pady=9,
            font=("Segoe UI", 10, "bold"), cursor="hand2"
        ).pack(anchor="w", pady=(12, 0))

    def show_rooms(self):
        self.set_active("Rooms")
        self.clear_content()
        self.page_header(
            "Operating Rooms",
            "Current room availability and scheduled operations."
        )

        try:
            free = self.surgery_manager.a_rooms()
        except Exception:
            free = []

        surgeries = self.get_surgeries()
        busy = {
            s.get("room"): s
            for s in surgeries
            if s.get("status") == "Scheduled"
        }

        try:
            total = self.surgery_manager.total_r
        except Exception:
            total = 5

        grid = tk.Frame(self.content, bg=self.bg)
        grid.pack(fill="both", expand=True)

        for room in range(1, total + 1):
            is_free = room in free
            s = busy.get(room)

            c = self.card(grid)
            c.grid(
                row=(room - 1) // 3,
                column=(room - 1) % 3,
                sticky="nsew",
                padx=8, pady=8
            )

            status = "AVAILABLE" if is_free else "OCCUPIED"
            status_color = self.success if is_free else self.warning

            tk.Label(
                c, text=f"ROOM {room}", bg="white", fg=self.text,
                font=("Segoe UI", 15, "bold")
            ).pack(anchor="w", padx=18, pady=(18, 5))

            tk.Label(
                c, text=status, bg="white", fg=status_color,
                font=("Segoe UI", 9, "bold")
            ).pack(anchor="w", padx=18)

            if s:
                tk.Label(
                    c, text=f"Patient: {s.get('patient_name', '')}",
                    bg="white", fg=self.muted,
                    font=("Segoe UI", 9)
                ).pack(anchor="w", padx=18, pady=(18, 3))
                tk.Label(
                    c, text=f"Doctor: {s.get('doctor', '')}",
                    bg="white", fg=self.muted,
                    font=("Segoe UI", 9)
                ).pack(anchor="w", padx=18, pady=3)
            else:
                tk.Label(
                    c, text="Ready for scheduling",
                    bg="white", fg="#94a3b8",
                    font=("Segoe UI", 9)
                ).pack(anchor="w", padx=18, pady=(18, 3))

        for col in range(3):
            grid.columnconfigure(col, weight=1)


if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalDashboard(root)
    root.mainloop()
