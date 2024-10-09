import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QInputDialog
from wallet.wallet import Wallet

class WalletGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.wallet = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Crypto Wallet')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.address_label = QLabel('Address:')
        layout.addWidget(self.address_label)

        self.address_entry = QLineEdit()
        self.address_entry.setReadOnly(True)
        layout.addWidget(self.address_entry)

        self.balance_label = QLabel('Balance:')
        layout.addWidget(self.balance_label)

        self.balance_entry = QLineEdit()
        self.balance_entry.setReadOnly(True)
        layout.addWidget(self.balance_entry)

        self.recipient_label = QLabel('Recipient Address:')
        layout.addWidget(self.recipient_label)

        self.recipient_entry = QLineEdit()
        layout.addWidget(self.recipient_entry)

        self.amount_label = QLabel('Amount:')
        layout.addWidget(self.amount_label)

        self.amount_entry = QLineEdit()
        layout.addWidget(self.amount_entry)

        self.send_button = QPushButton('Send')
        self.send_button.clicked.connect(self.send_transaction)
        layout.addWidget(self.send_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.prompt_password()

    def prompt_password(self):
        password, ok = QInputDialog.getText(self, 'Password', 'Enter your wallet password:', QLineEdit.Password)
        if ok:
            self.wallet = Wallet(password)
            self.address_entry.setText(self.wallet.address)
            self.balance_entry.setText(str(self.wallet.balance))
        else:
            QMessageBox.critical(self, 'Error', 'Password is required to access the wallet.')
            self.close()

    def send_transaction(self):
        recipient_address = self.recipient_entry.text()
        amount = float(self.amount_entry.text())
        try:
            transaction = self.wallet.create_transaction(recipient_address, amount)
            QMessageBox.information(self, 'Transaction Successful', f'Transaction: {transaction}')
            self.balance_entry.setText(str(self.wallet.balance))
        except ValueError as e:
            QMessageBox.critical(self, 'Transaction Failed', str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = WalletGUI()
    gui.show()
    sys.exit(app.exec_())