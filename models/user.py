# models/user.py

import csv

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserManager:
    def __init__(self):
        self.users = []

    def register_user(self, user):
        self.users.append(user)
        self.save_to_csv()

    def check_credentials(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False

    def save_to_csv(self):
        with open('users.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Username', 'Password'])
            for user in self.users:
                writer.writerow([user.username, user.password])

    def load_from_csv(self):
        try:
            with open('users.csv', mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    user = User(row['Username'], row['Password'])
                    self.users.append(user)
        except FileNotFoundError:
            pass  # File not found, no users yet

