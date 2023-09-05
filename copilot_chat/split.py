class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class Group:
    def __init__(self, name, members):
        self.name = name
        self.members = members
        self.expenses = []
        self.payments = []

    def add_expense(self, description, amount, payer, participants):
        self.expenses.append({'description': description, 'amount': amount, 'payer': payer, 'participants': participants})
        self.update_balances()

    def add_payment(self, amount, payer, payee):
        self.payments.append({'amount': amount, 'payer': payer, 'payee': payee})
        self.update_balances()

    def update_balances(self):
        balances = {member: 0 for member in self.members}
        for expense in self.expenses:
            amount_per_participant = expense['amount'] / len(expense['participants'])
            balances[expense['payer']] -= expense['amount']
            for participant in expense['participants']:
                balances[participant] += amount_per_participant
        for payment in self.payments:
            balances[payment['payer']] -= payment['amount']
            balances[payment['payee']] += payment['amount']
        self.balances = balances

user1 = User('Alice', 'alice@example.com', 'password')
user2 = User('Bob', 'bob@example.com', 'password')
user3 = User('Charlie', 'charlie@example.com', 'password')

group1 = Group('Group 1', [user1, user2, user3])
group1.add_expense('Dinner', 100, user1, [user1, user2])
group1.add_expense('Movie', 50, user2, [user2, user3])
group1.add_payment(60, user3, user1)

print(group1.balances)