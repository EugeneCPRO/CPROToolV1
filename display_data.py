import pymongo
import tkinter as tk
from tkinter import ttk
import threading
import time

from wallet_data_manipulation.user_prices import updatePortVal

# Global variables to store the previous values
previous_values = {}
asset_to_item = {}
name = "SITG"

# Function to fetch wallet data
def fetch_wallet_balances(collection):
    wallet_data = collection.find_one({"_id": "TotalBalance"})
    if wallet_data:
        return wallet_data["data"]
    else:
        return {}

# Function to calculate the overall portfolio value
def calculate_portfolio_value(wallet_data):
    total_value = sum(details.get('value', 0) for details in wallet_data.values())
    return total_value

# Format numbers to display nicely
def format_value(value):
    if isinstance(value, (int, float)):
        return f"${value:.2f}"  # Round to 2 decimal places and add the "$" prefix
    else:
        return "Unknown"

# Global variable to store the initial sorted data
sorted_data = []

def update_tree_values(tree, collection, total_value_label):
    global sorted_data
    while True:
        # Fetch wallet data
        wallet_data = fetch_wallet_balances(collection)

        if wallet_data:
            # Update prices along with wallet data
            updatePortVal(name)

            # Sort the data by "value" field in descending order only if there's a change
            new_sorted_data = sorted(wallet_data.items(), key=lambda item: item[1].get('value', 0), reverse=True)
            
            if new_sorted_data != sorted_data:
                # Clear existing items in the tree
                tree.delete(*tree.get_children())

                total_value = 0  # Initialize total value

                for asset, details in new_sorted_data:
                    confirmed_balance = details.get('confirmedBalance', 'Unknown')
                    current_value = details.get('value', 'Unknown')

                    # Get the item ID based on the asset or create a new one
                    item_id = tree.insert("", "end", values=(details["symbol"], round(float(confirmed_balance), 5), format_value(current_value)))

                    # If the value increased, flash green for 0.75 seconds
                    if current_value > previous_values.get(asset, current_value):
                        tree.item(item_id, tags=('green',))
                        tree.after(500, lambda i=item_id: tree.item(i, tags=()))
                    # If the value decreased, flash red for 0.75 seconds
                    elif current_value < previous_values.get(asset, current_value):
                        tree.item(item_id, tags=('red',))
                        tree.after(500, lambda i=item_id: tree.item(i, tags=()))

                    previous_values[asset] = current_value
                    total_value += current_value  # Add current value to total

                # Update the total portfolio value label
                total_value_label.config(text=f"Total Portfolio Value: {format_value(total_value)}")

                sorted_data = new_sorted_data
                # Schedule the next update after 1.5 seconds (1500 milliseconds)
                time.sleep(1.5)
            else:
                # No change, so check again after a shorter delay
                time.sleep(1.5)
        else:
            # If the collection does not exist, wait for a while before checking again
            print("Data does not exist!")
            time.sleep(5)


# Main function to create the GUI
def create_gui(collection):
    root = tk.Tk()
    root.title("Wallet Balances")
    root.geometry("800x400")
    root.configure(bg="black")

    # Create a label to display the total portfolio value
    total_value_label = tk.Label(root, text="Total Portfolio Value: Unknown", bg="black", fg="white")
    total_value_label.pack()

    # Create the treeview without the empty column on the left
    tree = ttk.Treeview(root, columns=("Asset", "Balance", "Value"), show="headings")
    tree.heading("#1", text="Asset")
    tree.heading("#2", text="Balance")
    tree.heading("#3", text="Value")

    # Create a thread to periodically update the values
    update_thread = threading.Thread(target=update_tree_values, args=(tree, collection, total_value_label))
    update_thread.daemon = True
    update_thread.start()

    tree.pack(expand=True, fill="both")

    exit_button = tk.Button(root, text="Exit", command=root.destroy, bg="red", fg="white")
    exit_button.pack()

    # Configure the tags to define the background color
    tree.tag_configure('green', background='green', foreground='white')
    tree.tag_configure('red', background='red', foreground='white')

    root.mainloop()

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb+srv://eugened:jO5F7L1PU1VL1fh1@walletdb.yzkhawm.mongodb.net/?retryWrites=true&w=majority")
    db = client["user_wallet_balances"]
    collection = db[name]
    create_gui(collection)
