import sqlite3

conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

print("Database connected")

# Create accounts table
cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY,
    name TEXT,
    balance REAL
)
""")

conn.commit()

print("Table created")

# Create account function
def create_account():
    name = input("Enter name: ")
    balance = float(input("Enter balance: "))

    cursor.execute("INSERT INTO accounts(name, balance) VALUES (?, ?)", (name, balance))
    conn.commit()

    print("Account created")

# Deposit function
def deposit():
    name = input("Enter name: ")
    amount = float(input("Enter deposit amount: "))

    cursor.execute("UPDATE accounts SET balance = balance + ? WHERE name=?", (amount, name))
    conn.commit()

    if amount > 50000:
        print("Fraud detected")
    else:
        print("Safe transaction")

# Run functions
while True:
    print("\n1 Create Account")
    print("2 Deposit")
    print("3 Show Accounts")
    print("4 Exit")

    choice = input("Enter choice: ")

    if choice == '1':
        create_account()

    elif choice == '2':
        deposit()

    elif choice == '3':
        cursor.execute("SELECT * FROM accounts")
        rows = cursor.fetchall()

        for row in rows:
            print(row)

    elif choice == '4':
        break