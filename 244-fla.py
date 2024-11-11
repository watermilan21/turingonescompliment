import tkinter as tk
from tkinter import messagebox
from rich.console import Console
from rich.table import Table

class TuringMachine:
    def __init__(self, tape, blank_symbol=" "):
        self.tape = list(tape)
        self.head_position = 0
        self.blank_symbol = blank_symbol
        self.state = "start"
        self.transitions = {
            ("start", "0"): ("complement", "1", 1),
            ("start", "1"): ("complement", "0", 1),
            ("start", " "): ("halt", " ", 0),
            ("complement", "0"): ("complement", "1", 1),
            ("complement", "1"): ("complement", "0", 1),
            ("complement", " "): ("halt", " ", 0),
        }
        self.console = Console()

    def display_transition_table(self):
        table = Table(title="Turing Machine Transition Table", show_lines=True, style="cyan")
        table.add_column("Current State", justify="center")
        table.add_column("Read Symbol", justify="center")
        table.add_column("New State", justify="center")
        table.add_column("Write Symbol", justify="center")
        table.add_column("Direction", justify="center")
        for (current_state, read_symbol), (new_state, write_symbol, direction) in self.transitions.items():
            direction_str = "Right" if direction == 1 else "Left"
            table.add_row(current_state, read_symbol, new_state, write_symbol, direction_str)
        self.console.print(table)

    def step(self):
        current_symbol = self.tape[self.head_position]
        if (self.state, current_symbol) not in self.transitions:
            raise ValueError("No valid transition found!")
        new_state, new_symbol, direction = self.transitions[(self.state, current_symbol)]
        self.tape[self.head_position] = new_symbol
        self.state = new_state
        self.head_position += direction
        if self.head_position == len(self.tape):
            self.tape.append(self.blank_symbol)

    def run(self):
        while self.state != "halt":
            self.step()
        return "".join(self.tape).strip()


def process_input():
    binary_input = input_entry.get().strip()
    if not all(c in "01" for c in binary_input):
        messagebox.showerror("Invalid Input", "Please enter a binary string containing only 0s and 1s.")
    else:
        turing_machine = TuringMachine(binary_input + " ")
        turing_machine.display_transition_table()
        result = turing_machine.run()
        output_label.config(text=f"One's Complement: {result}")


root = tk.Tk()
root.title("Turing Machine Simulator")
root.geometry("400x250")
root.resizable(False, False)

input_frame = tk.Frame(root)
input_frame.pack(pady=20)

input_label = tk.Label(input_frame, text="Enter Binary String:")
input_label.pack(side=tk.LEFT, padx=5)

input_entry = tk.Entry(input_frame, width=20)
input_entry.pack(side=tk.LEFT, padx=5)

process_button = tk.Button(root, text="Process", command=process_input)
process_button.pack(pady=10)

output_frame = tk.Frame(root)
output_frame.pack(pady=20)

output_label = tk.Label(output_frame, text="", font=("Arial", 12))
output_label.pack()

root.mainloop()