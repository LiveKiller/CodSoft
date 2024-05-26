import customtkinter as ctk
import tkinter as tk
import mysql.connector
from tkinter import messagebox
from functools import partial

class ToDoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("To-Do List")
        self.geometry("1500x500")

        self.label = ctk.CTkLabel(self, text="To-Do List")
        self.label.pack(padx=10, pady=10)

        self.entry = ctk.CTkEntry(self, placeholder_text="Enter a task...")
        self.entry.pack(padx=10, pady=10)

        self.add_button = ctk.CTkButton(self, text="Add Task", command=self.add_task)
        self.add_button.pack(padx=10, pady=10)

        self.task_frame = ctk.CTkScrollableFrame(self)
        self.task_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.db = self.connect_db()
        self.create_table()
        self.load_tasks()

    def connect_db(self):
        try:
            return mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="a12"
            )
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            self.destroy()

    def create_table(self):
        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                task TEXT,
                is_completed BOOLEAN
            )
        """)
        self.db.commit()

    def add_task(self):
        task = self.entry.get().strip()
        if not task:
            messagebox.showwarning("Input Error", "Task cannot be empty!")
            return
        cursor = self.db.cursor()
        query = "INSERT INTO tasks (task, is_completed) VALUES (%s, 0)"
        cursor.execute(query, (task,))
        self.db.commit()
        self.entry.delete(0, 'end')
        self.resequence_ids()
        self.load_tasks()

    def load_tasks(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()

        for task in tasks:
            task_id, task_text, is_completed = task
            task_frame = ctk.CTkFrame(self.task_frame)
            task_frame.pack(padx=5, pady=5, fill="x")

            progress_var = ctk.DoubleVar(value=100 if is_completed else 0)
            progress_bar = ctk.CTkProgressBar(task_frame, mode="determinate", variable=progress_var)
            progress_bar.pack(side="left", padx=5, pady=5)
            if is_completed:
                progress_bar.configure(progress_color="green")

            task_textbox = tk.Text(task_frame, height=2, wrap="word")
            task_textbox.insert("1.0", task_text)
            task_textbox.configure(state="disabled")
            if is_completed:
                task_textbox.configure(fg="#808080", bg="#d3d3d3")
            task_textbox.pack(side="left", padx=5, pady=5, fill="both", expand=True)

            done_button = ctk.CTkButton(task_frame, text="Done",
                                        command=partial(self.mark_as_done, task_id, progress_var, progress_bar, task_textbox))
            done_button.pack(side="right", padx=5, pady=5)

            remove_button = ctk.CTkButton(task_frame, text="❌",
                                          command=partial(self.remove_task, task_id))
            remove_button.pack(side="right", padx=5, pady=5)

            update_button = ctk.CTkButton(task_frame, text="✏️",
                                          command=partial(self.update_task, task_id, task_textbox))
            update_button.pack(side="right", padx=5, pady=5)

    def mark_as_done(self, task_id, progress_var, progress_bar, task_textbox):
        cursor = self.db.cursor()
        query = "UPDATE tasks SET is_completed = 1 WHERE id = %s"
        cursor.execute(query, (task_id,))
        self.db.commit()
        progress_var.set(100)
        progress_bar.configure(progress_color="green")
        task_textbox.configure(fg="#808080", bg="#d3d3d3")

    def remove_task(self, task_id):
        cursor = self.db.cursor()
        query = "DELETE FROM tasks WHERE id = %s"
        cursor.execute(query, (task_id,))
        self.db.commit()
        self.resequence_ids()
        self.load_tasks()

    def update_task(self, task_id, task_textbox):
        if task_textbox.cget("state") == "disabled":
            task_textbox.configure(state="normal")
        else:
            task_textbox.configure(state="disabled")
            new_task_text = task_textbox.get("1.0", "end-1c").strip()
            if not new_task_text:
                messagebox.showwarning("Input Error", "Task cannot be empty!")
                task_textbox.configure(state="normal")
                return
            cursor = self.db.cursor()
            query = "UPDATE tasks SET task = %s WHERE id = %s"
            cursor.execute(query, (new_task_text, task_id))
            self.db.commit()

    def resequence_ids(self):
        cursor = self.db.cursor()
        cursor.execute("SET @count = 0;")
        cursor.execute("UPDATE tasks SET id = @count:= @count + 1;")
        cursor.execute("ALTER TABLE tasks AUTO_INCREMENT = 1;")
        self.db.commit()

if __name__ == "__main__":
    app = ToDoApp()
    app.mainloop()
