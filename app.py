import streamlit as st
import sqlite3
import pandas as pd

# Database connection
conn = sqlite3.connect("bank.db", check_same_thread=False)
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY,
    name TEXT,
    balance REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    name TEXT,
    type TEXT,
    amount REAL,
    fraud TEXT
)
""")

conn.commit()

# Page title
st.title("🏦 Smart Bank Fraud Detection System")

# Sidebar menu
menu = st.sidebar.selectbox(
    "Menu",
    ["Create Account", "Deposit", "Withdraw", "Show Accounts", "Transactions"]
)

# Create Account
if menu == "Create Account":
    st.header("Create New Account")

    name = st.text_input("Enter Name")
    balance = st.number_input("Initial Balance", min_value=0.0)

    if st.button("Create Account"):
        cursor.execute("INSERT INTO accounts(name, balance) VALUES (?, ?)", (name, balance))
        conn.commit()
        st.success("Account created successfully")

# Deposit
elif menu == "Deposit":
    st.header("Deposit Money")

    name = st.text_input("Account Holder Name")
    amount = st.number_input("Deposit Amount", min_value=0.0)

    if st.button("Deposit"):
        cursor.execute("UPDATE accounts SET balance = balance + ? WHERE name=?", (amount, name))

        fraud = "Fraud" if amount > 50000 else "Safe"

        cursor.execute(
            "INSERT INTO transactions(name, type, amount, fraud) VALUES (?, ?, ?, ?)",
            (name, "Deposit", amount, fraud)
        )

        conn.commit()

        if fraud == "Fraud":
            st.error("⚠ Fraud Detected")
        else:
            st.success("✅ Safe Transaction")

# Withdraw
elif menu == "Withdraw":
    st.header("Withdraw Money")

    name = st.text_input("Account Holder Name")
    amount = st.number_input("Withdraw Amount", min_value=0.0)

    if st.button("Withdraw"):
        cursor.execute("UPDATE accounts SET balance = balance - ? WHERE name=?", (amount, name))

        fraud = "Fraud" if amount > 50000 else "Safe"

        cursor.execute(
            "INSERT INTO transactions(name, type, amount, fraud) VALUES (?, ?, ?, ?)",
            (name, "Withdraw", amount, fraud)
        )

        conn.commit()

        if fraud == "Fraud":
            st.error("⚠ Fraud Detected")
        else:
            st.success("✅ Safe Transaction")

# Show Accounts
elif menu == "Show Accounts":
    st.header("Customer Accounts")

    cursor.execute("SELECT * FROM accounts")
    rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns=["ID", "Name", "Balance"])
    st.dataframe(df)

# Transactions
elif menu == "Transactions":
    st.header("Transaction History")

    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns=["ID", "Name", "Type", "Amount", "Fraud"])
    st.dataframe(df)