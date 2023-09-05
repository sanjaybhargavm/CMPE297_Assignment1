from typing import List

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

user1 = User('Alice', 'alice@example.com', 'password')
user2 = User('Bob', 'bob@example.com', 'password')
user3 = User('Charlie', 'charlie@example.com', 'password')

group1 = Group('Group 1', [user1, user2, user3])
group1.add_expense(Expense('Dinner', 100, user1, [user1, user2]))
group1.add_expense(Expense('Movie', 50, user2, [user2, user3]))
group1.add_payment(Payment(60, user3, user1))

for user in group1.members:
    balance = group1.get_balance(user)
    if balance > 0:
        print(f"{user.name} is owed {balance:.2f}")
    elif balance < 0:
        print(f"{user.name} owes {-balance:.2f}")
    else:
        print(f"{user.name} has no balance")