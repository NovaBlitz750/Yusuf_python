import os
import datetime

# ─── Data Storage ────────────────────────────────────────────────────────────
accounts = {}  # { account_number: { name, pin, balance, transactions } }
next_account_number = 1001


# ─── Helpers ─────────────────────────────────────────────────────────────────
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log(account_number, entry):
    accounts[account_number]["transactions"].append(f"[{timestamp()}] {entry}")

def header(title):
    print("\n" + "═" * 40)
    print(f"  {title}")
    print("═" * 40)

def find_account(acc_num):
    return accounts.get(acc_num)

def verify_pin(account, pin):
    return account["pin"] == pin


# ─── Features ────────────────────────────────────────────────────────────────
def create_account():
    global next_account_number
    header("CREATE ACCOUNT")

    name = input("Full name: ").strip()
    if not name:
        print("❌ Name cannot be empty.")
        return

    while True:
        pin = input("Set a 4-digit PIN: ").strip()
        if pin.isdigit() and len(pin) == 4:
            break
        print("❌ PIN must be exactly 4 digits.")

    initial = input("Initial deposit (or 0): ").strip()
    try:
        initial = float(initial)
        if initial < 0:
            raise ValueError
    except ValueError:
        print("❌ Invalid amount.")
        return

    acc_num = next_account_number
    next_account_number += 1

    accounts[acc_num] = {
        "name": name,
        "pin": pin,
        "balance": initial,
        "transactions": []
    }

    if initial > 0:
        log(acc_num, f"Account opened with initial deposit of ${initial:.2f}")

    print(f"\n✅ Account created!")
    print(f"   Account Number : {acc_num}")
    print(f"   Name           : {name}")
    print(f"   Balance        : ${initial:.2f}")


def deposit():
    header("DEPOSIT")
    acc_num, account = login()
    if not account:
        return

    try:
        amount = float(input("Amount to deposit: $"))
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("❌ Invalid amount.")
        return

    account["balance"] += amount
    log(acc_num, f"Deposited ${amount:.2f} | Balance: ${account['balance']:.2f}")
    print(f"✅ Deposited ${amount:.2f}. New balance: ${account['balance']:.2f}")


def withdraw():
    header("WITHDRAW")
    acc_num, account = login()
    if not account:
        return

    try:
        amount = float(input("Amount to withdraw: $"))
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("❌ Invalid amount.")
        return

    if amount > account["balance"]:
        print("❌ Insufficient funds.")
        return

    account["balance"] -= amount
    log(acc_num, f"Withdrew ${amount:.2f} | Balance: ${account['balance']:.2f}")
    print(f"✅ Withdrew ${amount:.2f}. New balance: ${account['balance']:.2f}")


def transfer():
    header("TRANSFER")
    print("--- Sender ---")
    sender_num, sender = login()
    if not sender:
        return

    try:
        recipient_num = int(input("Recipient account number: "))
    except ValueError:
        print("❌ Invalid account number.")
        return

    recipient = find_account(recipient_num)
    if not recipient:
        print("❌ Recipient account not found.")
        return

    if recipient_num == sender_num:
        print("❌ Cannot transfer to yourself.")
        return

    try:
        amount = float(input(f"Amount to transfer: $"))
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("❌ Invalid amount.")
        return

    if amount > sender["balance"]:
        print("❌ Insufficient funds.")
        return

    sender["balance"] -= amount
    recipient["balance"] += amount

    log(sender_num, f"Transferred ${amount:.2f} to Acc#{recipient_num} | Balance: ${sender['balance']:.2f}")
    log(recipient_num, f"Received ${amount:.2f} from Acc#{sender_num} | Balance: ${recipient['balance']:.2f}")

    print(f"✅ Transferred ${amount:.2f} to {recipient['name']} (Acc#{recipient_num}).")
    print(f"   Your new balance: ${sender['balance']:.2f}")


def check_balance():
    header("CHECK BALANCE")
    _, account = login()
    if not account:
        return

    print(f"\n  Name    : {account['name']}")
    print(f"  Balance : ${account['balance']:.2f}")


def transaction_history():
    header("TRANSACTION HISTORY")
    _, account = login()
    if not account:
        return

    txns = account["transactions"]
    if not txns:
        print("  No transactions yet.")
    else:
        for t in txns:
            print(f"  {t}")


def login():
    """Returns (account_number, account_dict) or (None, None) on failure."""
    try:
        acc_num = int(input("Account number: "))
    except ValueError:
        print("❌ Invalid account number.")
        return None, None

    account = find_account(acc_num)
    if not account:
        print("❌ Account not found.")
        return None, None

    pin = input("PIN: ").strip()
    if not verify_pin(account, pin):
        print("❌ Incorrect PIN.")
        return None, None

    print(f"  Welcome, {account['name']}!")
    return acc_num, account


# ─── Main Menu ───────────────────────────────────────────────────────────────
def main():
    while True:
        header("🏦 MINI BANK")
        print("  1. Create Account")
        print("  2. Deposit")
        print("  3. Withdraw")
        print("  4. Transfer")
        print("  5. Check Balance")
        print("  6. Transaction History")
        print("  0. Exit")
        print()

        choice = input("  Choose an option: ").strip()

        if choice == "1":
            create_account()
        elif choice == "2":
            deposit()
        elif choice == "3":
            withdraw()
        elif choice == "4":
            transfer()
        elif choice == "5":
            check_balance()
        elif choice == "6":
            transaction_history()
        elif choice == "0":
            print("\n👋 Goodbye!\n")
            break
        else:
            print("❌ Invalid option.")

        input("\n  Press Enter to continue...")


if __name__ == "__main__":
    main()