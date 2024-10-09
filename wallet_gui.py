import tkinter as tk
from tkinter import messagebox
from wallet.wallet import Wallet

class WalletGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Wallet")
        self.wallet = Wallet()

        self.create_widgets()

    def create_widgets(self):
        self.address_label = tk.Label(self.root, text="Address:")
        self.address_label.grid(row=0, column=0, padx=10, pady=10)

        self.address_entry = tk.Entry(self.root, width=50)
        self.address_entry.grid(row=0, column=1, padx=10, pady=10)
        self.address_entry.insert(0, self.wallet.address)
        self.address_entry.config(state='readonly')

        self.balance_label = tk.Label(self.root, text="Balance:")
        self.balance_label.grid(row=1, column=0, padx=10, pady=10)

        self.balance_entry = tk.Entry(self.root, width=20)
        self.balance_entry.grid(row=1, column=1, padx=10, pady=10)
        self.balance_entry.insert(0, str(self.wallet.balance))
        self.balance_entry.config(state='readonly')

        self.recipient_label = tk.Label(self.root, text="Recipient Address:")
        self.recipient_label.grid(row=2, column=0, padx=10, pady=10)

        self.recipient_entry = tk.Entry(self.root, width=50)
        self.recipient_entry.grid(row=2, column=1, padx=10, pady=10)

        self.amount_label = tk.Label(self.root, text="Amount:")
        self.amount_label.grid(row=3, column=0, padx=10, pady=10)

        self.amount_entry = tk.Entry(self.root, width=20)
        self.amount_entry.grid(row=3, column=1, padx=10, pady=10)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_transaction)
        self.send_button.grid(row=4, column=1, padx=10, pady=10)

    def send_transaction(self):
        recipient_address = self.recipient_entry.get()
        amount = float(self.amount_entry.get())
        try:
            transaction = self.wallet.create_transaction(recipient_address, amount)
            messagebox.showinfo("Transaction Successful", f"Transaction: {transaction}")
            self.balance_entry.config(state='normal')
            self.balance_entry.delete(0, tk.END)
            self.balance_entry.insert(0, str(self.wallet.balance))
            self.balance_entry.config(state='readonly')
        except ValueError as e:
            messagebox.showerror("Transaction Failed", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = WalletGUI(root)
    root.mainloop()