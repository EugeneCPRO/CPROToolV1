import tkinter as tk
from tkinter import ttk
import time
import finGet

class TestUI(object):
    def __init__(self, portfolio, portValue, name, chain):
        self.root = tk.Tk()
        self.root.title("{name}'s {chain} Portfolio")
        self.root.geometry("600x400")

        self.dark_bg = "#121212"
        self.dark_fg = "white"

        self.portfolio = portfolio
        self.portValue = portValue
        self.name = name
        self.chain = chain
        self.prev_values = []

        # Create a treeview widget (table)
        self.tree = ttk.Treeview(self.root, columns=("Assets", "Balance", "Value"), show="headings")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Define column headings
        self.tree.heading("Assets", text="Assets")
        self.tree.heading("Balance", text="Balance")
        self.tree.heading("Value", text="Value")

        # Set column widths
        self.tree.column("Assets", width=200)
        self.tree.column("Balance", width=200)
        self.tree.column("Value", width=200)

        # Set font size for the table
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 14))  # Set the desired font size here

        self.tree_items = []

    def init_table(self):
        for i in range(len(self.portfolio[0])):
            asset, balance, value, color = self.format_row(self.portfolio[0][i], self.portfolio[1][i], 0.0, 0.0)
            self.tree_items.append(self.tree.insert("", "end", values=(asset, balance, value), tags=("value", color)))

            self.init_table()

    def format_row(self, asset, balance, value, prev_value):
        asset_width = 10
        balance_width = 10
        value_width = 10

        # Calculate the color based on the change in value
        if value > prev_value:
            color_style = 'green'
        elif value < prev_value:
            color_style = 'red'
        else:
            color_style = 'normal'

        row = (
            (f'class:{color_style}', f'{asset:<{asset_width}}'),
            ('class:normal', ' | '),
            ('class:normal', f'{balance:<{balance_width}}'),
            ('class:normal', ' | '),
            (f'class:{color_style}', f'{value:<{value_width}}'),
            ('class:normal', '\n'),
        )

        return row

    def update_values(self):
        new_values = finGet.priceStream(self.portfolio[0])  # Replace with your logic

        for i in range(len(self.portfolio[0])):
            asset, balance, value, color = self.format_row(
                self.portfolio[0][i], self.portfolio[1][i], new_values, self.prev_values
            )
            self.tree.item(self.tree_items[i], values=(asset, balance, value), tags=("value", color))

        # Flash colors for 0.5 seconds
        self.root.update()
        time.sleep(0.5)

        for i in range(len(self.portfolio[0])):
            asset, balance, value, color = self.format_row(
                self.portfolio[0][i], self.portfolio[1][i], new_values[i], self.prev_values[i]
            )
            self.tree.item(self.tree_items[i], values=(asset, balance, value), tags=("value", color))

        self.prev_values = new_values  # Update previous values
        self.root.after(1000, self.update_values)  # Call update_values again after 1000ms (1 second)

    def run(self):
        self.update_values()
        self.root.mainloop()


