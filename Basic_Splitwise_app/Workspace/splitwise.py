import tkinter as tk
from tkinter import messagebox

class SplitwiseApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Splitwise App")

        self.amount_label = tk.Label(window, text="Total Amount ($):")
        self.amount_label.pack()
        self.amount_entry = tk.Entry(window)
        self.amount_entry.pack()

        self.people_label = tk.Label(window, text="Number of People:")
        self.people_label.pack()
        self.people_entry = tk.Entry(window)
        self.people_entry.pack()

        self.calculate_button = tk.Button(window, text="Calculate", command=self.calculate_split)
        self.calculate_button.pack()

        self.result_label = tk.Label(window, text="")
        self.result_label.pack()

    def calculate_split(self):
        try:
            total_amount = float(self.amount_entry.get())
            num_people = int(self.people_entry.get())
            if num_people <= 0:
                raise ValueError("Number of people must be positive.")
            split_amount = round(total_amount / num_people, 2)
            remaining_amount = round(total_amount - split_amount * num_people, 2)
            self.result_label['text'] = f"Each person should pay: ${split_amount}\n" \
                                        f"The first person should pay an additional: ${remaining_amount}"
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

def main():
    root = tk.Tk()
    app = SplitwiseApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
