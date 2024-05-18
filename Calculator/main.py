import customtkinter as ctk

class Calculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculator")
        self.geometry("470x250")
        self.configure(fg_color="#181b1f")

        self.evwidth = 400
        self.bwidth1 = self.evwidth / 4 - 20

        self.values = ctk.CTkEntry(master=self, width=self.evwidth)
        self.values.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        self.obc = "#fb2f64"
        self.obch = "#cc2753"
        self.nbc = "#181b1f"
        self.nbch = "#14161a"

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]

        row_val = 1
        col_val = 0

        for button in buttons:
            if button == '=':
                btn = ctk.CTkButton(master=self, text=button, command=self.evaluate, width=self.bwidth1)
            elif button in ['+', '-', '*', '/']:
                btn = ctk.CTkButton(master=self, text=button, command=lambda button=button: self.operate(button), width=self.bwidth1, fg_color=self.obc, hover_color=self.obch)
            else:
                btn = ctk.CTkButton(master=self, text=button, command=lambda button=button: self.g_num(button), width=self.bwidth1, fg_color=self.nbc, hover_color=self.nbch)
            btn.grid(row=row_val, column=col_val, pady=5, padx=10)
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

        self.clear = ctk.CTkButton(master=self, text="Clear", command=self.all_clear, width=self.bwidth1)
        self.clear.grid(row=row_val, column=0, columnspan=4, pady=5, padx=10)

    def g_num(self, n):
        current_text = self.values.get()
        new_text = current_text + n
        self.values.delete(0, ctk.END)
        self.values.insert(0, new_text)

    def all_clear(self):
        self.values.delete(0, ctk.END)

    def operate(self, o):
        self.f_num = float(self.values.get())
        self.op = o
        self.values.delete(0, ctk.END)

    def evaluate(self, event=None):
        s_num = self.values.get()
        if s_num:
            s_num = float(s_num)
            result = None
            if self.op == "+":
                result = self.f_num + s_num
            elif self.op == "-":
                result = self.f_num - s_num
            elif self.op == "*":
                result = self.f_num * s_num
            elif self.op == "/":

                if s_num != 0:
                    result = self.f_num / s_num
                else:
                    result = "Error"
            self.values.delete(0, ctk.END)
            self.values.insert(0, result)
        else:
            self.values.insert(0, "Error")

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
