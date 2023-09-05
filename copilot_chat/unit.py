import unittest
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

class TestGroup(unittest.TestCase):
    def setUp(self):
        self.user1 = User('Alice', 'alice@example.com', 'password')
        self.user2 = User('Bob', 'bob@example.com', 'password')
        self.user3 = User('Charlie', 'charlie@example.com', 'password')
        self.group1 = Group('Group 1', [self.user1, self.user2, self.user3])

    def test_add_expense(self):
        self.group1.add_expense(Expense('Dinner', 100, self.user1, [self.user1, self.user2]))
        self.assertEqual(len(self.group1.expenses), 1)

    def test_add_payment(self):
        self.group1.add_payment(Payment(60, self.user3, self.user1))
        self.assertEqual(len(self.group1.payments), 1)

    def test_update_balances(self):
        self.group1.add_expense(Expense('Dinner', 100, self.user1, [self.user1, self.user2]))
        self.group1.add_expense(Expense('Movie', 50, self.user2, [self.user2, self.user3]))
        self.group1.add_payment(Payment(60, self.user3, self.user1))
        self.group1.update_balances()
        self.assertEqual(self.group1.get_balance(self.user1), -20)
        self.assertEqual(self.group1.get_balance(self.user2), 10)
        self.assertEqual(self.group1.get_balance(self.user3), 10)

    def test_get_balance(self):
        self.group1.add_expense(Expense('Dinner', 100, self.user1, [self.user1, self.user2]))
        self.group1.add_expense(Expense('Movie', 50, self.user2, [self.user2, self.user3]))
        self.group1.add_payment(Payment(60, self.user3, self.user1))
        self.group1.update_balances()
        self.assertEqual(self.group1.get_balance(self.user1), -20)
        self.assertEqual(self.group1.get_balance(self.user2), 10)
        self.assertEqual(self.group1.get_balance(self.user3), 10)

if __name__ == '__main__':
    unittest.main()