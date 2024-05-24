import customtkinter as ctk
import tkinter as tk
import mysql.connector

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="a12"
)
cursor = db.cursor()

# Create tasks table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task TEXT,
        is_completed BOOLEAN
    )
""")

db.commit()

class ToDoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("To-Do List")
        self.geometry("700x500")  # Wider screen

        self.label = ctk.CTkLabel(self, text="To-Do List")
        self.label.pack(padx=10, pady=10)

        self.entry = ctk.CTkEntry(self, placeholder_text="Enter a task...")
        self.entry.pack(padx=10, pady=10)

        self.add_button = ctk.CTkButton(self, text="Add Task", command=self.add_task)
        self.add_button.pack(padx=10, pady=10)

        self.task_frame = ctk.CTkScrollableFrame(self)
        self.task_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.load_tasks()

    def add_task(self):
        task = self.entry.get()
        if task:
            query = "INSERT INTO tasks (task, is_completed) VALUES (%s, 0)"
            cursor.execute(query, (task,))
            db.commit()
            self.entry.delete(0, 'end')
            self.load_tasks()

    def load_tasks(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()

        for task in tasks:
            task_id, task_text, is_completed = task
            task_frame = ctk.CTkFrame(self.task_frame)
            task_frame.pack(padx=5, pady=5, fill="x")

            progress_var = ctk.DoubleVar(value=100 if is_completed else 0)
            progress_bar = ctk.CTkProgressBar(task_frame, mode="determinate", variable=progress_var)
            progress_bar.pack(side="left", padx=5, pady=5)

            task_textbox = tk.Text(task_frame, height=2, wrap="word")
            task_textbox.insert("1.0", task_text)
            task_textbox.configure(state="disabled")
            task_textbox.pack(side="left", padx=5, pady=5, fill="both", expand=True)

            done_button = ctk.CTkButton(task_frame, text="Done",
                                        command=lambda id=task_id: self.mark_as_done(id, progress_var, task_textbox))
            done_button.pack(side="right", padx=5, pady=5)

            remove_button = ctk.CTkButton(task_frame, text="❌",
                                          command=lambda id=task_id: self.remove_task(id))
            remove_button.pack(side="right", padx=5, pady=5)

            update_button = ctk.CTkButton(task_frame, text="✏️",
                                          command=lambda id=task_id, textbox=task_textbox: self.update_task(id, textbox))
            update_button.pack(side="right", padx=5, pady=5)

    def mark_as_done(self, task_id, progress_var, task_textbox):
        query = "UPDATE tasks SET is_completed = 1 WHERE id = %s"
        cursor.execute(query, (task_id,))
        db.commit()
        progress_var.set(100)
        task_textbox.configure(state="disabled")
        task_textbox.configure(fg="#808080")

    def remove_task(self, task_id):
        query = "DELETE FROM tasks WHERE id = %s"
        cursor.execute(query, (task_id,))
        db.commit()
        self.load_tasks()

    def update_task(self, task_id, task_textbox):
        if task_textbox.cget("state") == "disabled":
            task_textbox.configure(state="normal")
        else:
            task_textbox.configure(state="disabled")
            new_task_text = task_textbox.get("1.0", "end-1c")
            query = "UPDATE tasks SET task = %s WHERE id = %s"
            cursor.execute(query, (new_task_text, task_id))
            db.commit()

if __name__ == "__main__":
    app = ToDoApp()
    app.mainloop()
