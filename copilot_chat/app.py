from flask import Flask, render_template, request
from typing import List

app = Flask(__name__)

class User:
    def __init__(self, name: str, email: str, password: str) -> None:
        self.name = name
        self.email = email
        self.password = password

class Expense:
    def __init__(self, description: str, amount: float, payer: User, participants: List[User]) -> None:
        self.description = description
        self.amount = amount
        self.payer = payer
        self.participants = participants

class Payment:
    def __init__(self, amount: float, payer: User, payee: User) -> None:
        self.amount = amount
        self.payer = payer
        self.payee = payee

class Group:
    def __init__(self, name: str, members: List[User]) -> None:
        self.name = name
        self.members = members
        self.expenses = []
        self.payments = []

    def add_expense(self, expense: Expense) -> None:
        self.expenses.append(expense)
        self.update_balances()

    def add_payment(self, payment: Payment) -> None:
        self.payments.append(payment)
        self.update_balances()

    def update_balances(self) -> None:
        balances = {member: 0 for member in self.members}
        for expense in self.expenses:
            amount_per_participant = expense.amount / len(expense.participants)
            balances[expense.payer] -= expense.amount
            for participant in expense.participants:
                balances[participant] += amount_per_participant
        for payment in self.payments:
            balances[payment.payer] -= payment.amount
            balances[payment.payee] += payment.amount
        self.balances = balances

    def get_balance(self, user: User) -> float:
        return self.balances.get(user, 0)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Create users
        user1 = User(request.form['user1_name'], request.form['user1_email'], request.form['user1_password'])
        user2 = User(request.form['user2_name'], request.form['user2_email'], request.form['user2_password'])
        user3 = User(request.form['user3_name'], request.form['user3_email'], request.form['user3_password'])

        # Create group
        group = Group(request.form['group_name'], [user1, user2, user3])

        # Add expenses
        group.add_expense(Expense(request.form['expense1_description'], float(request.form['expense1_amount']), user1, [user1, user2]))
        group.add_expense(Expense(request.form['expense2_description'], float(request.form['expense2_amount']), user2, [user2, user3]))

        # Add payments
        group.add_payment(Payment(float(request.form['payment1_amount']), user3, user1))

        # Get balances
        group.update_balances()
        user1_balance = group.get_balance(user1)
        user2_balance = group.get_balance(user2)
        user3_balance = group.get_balance(user3)

        return render_template('index.html', user1_balance=user1_balance, user2_balance=user2_balance, user3_balance=user3_balance)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    
    