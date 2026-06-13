import json
print("BANK.PY IS LOADED")
import random
import string
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


DATABASE = "database.json"


def _load_data() -> list:
    if Path(DATABASE).exists():
        with open(DATABASE) as f:
            return json.loads(f.read())
    return []


def _save_data(data: list) -> None:
    with open(DATABASE, "w") as f:
        f.write(json.dumps(data, indent=2))


def _generate_account_number() -> str:
    alpha = random.choices(string.ascii_uppercase, k=4)
    num = random.choices(string.digits, k=8)
    acc = alpha + num
    random.shuffle(acc)
    return "".join(acc)


# ── Result helpers ────────────────────────────────────────────────────────────

def ok(payload=None, message: str = ""):
    return {"success": True, "data": payload, "message": message}

def err(message: str):
    return {"success": False, "data": None, "message": message}


# ── Core banking operations ───────────────────────────────────────────────────

def create_account(name: str, age: int, email: str, pin: str, initial_deposit: float = 0) -> dict:
    """Create a new bank account. Returns result dict."""
    if not name.strip():
        return err("Name cannot be empty.")
    if age < 12:
        return err("Applicant must be at least 12 years old.")
    if not pin.isdigit() or len(pin) != 4:
        return err("PIN must be exactly 4 digits.")
    if initial_deposit < 0:
        return err("Initial deposit cannot be negative.")

    data = _load_data()

    # Duplicate email check
    if any(u["email"].lower() == email.lower() for u in data):
        return err("An account with this email already exists.")

    account = {
        "name": name.strip(),
        "age": int(age),
        "email": email.strip().lower(),
        "account_no": _generate_account_number(),
        "pin": pin,
        "balance": float(initial_deposit),
    }
    data.append(account)
    _save_data(data)
    return ok(account, f"Account created successfully! Your account number is {account['account_no']}.")


def _find_user(account_no: str, pin: str) -> Optional[dict]:
    data = _load_data()
    for user in data:
        if user["account_no"] == account_no and str(user["pin"]) == str(pin):
            return user
    return None


def deposit(account_no: str, pin: str, amount: float) -> dict:
    """Deposit money into an account."""
    if amount <= 0:
        return err("Deposit amount must be greater than zero.")

    data = _load_data()
    for user in data:
        if user["account_no"] == account_no and str(user["pin"]) == str(pin):
            user["balance"] = round(user["balance"] + amount, 2)
            _save_data(data)
            return ok({"balance": user["balance"]}, f"₹{amount:,.2f} deposited. New balance: ₹{user['balance']:,.2f}")
    return err("Invalid account number or PIN.")


def withdraw(account_no: str, pin: str, amount: float) -> dict:
    """Withdraw money from an account."""
    if amount <= 0:
        return err("Withdrawal amount must be greater than zero.")

    data = _load_data()
    for user in data:
        if user["account_no"] == account_no and str(user["pin"]) == str(pin):
            if amount > user["balance"]:
                return err(f"Insufficient balance. Available: ₹{user['balance']:,.2f}")
            user["balance"] = round(user["balance"] - amount, 2)
            _save_data(data)
            return ok({"balance": user["balance"]}, f"₹{amount:,.2f} withdrawn. Remaining balance: ₹{user['balance']:,.2f}")
    return err("Invalid account number or PIN.")


def get_account(account_no: str, pin: str) -> dict:
    """Fetch account details."""
    user = _find_user(account_no, pin)
    if not user:
        return err("Invalid account number or PIN.")
    # Return a copy without the pin
    safe = {k: v for k, v in user.items() if k != "pin"}
    return ok(safe)


def update_account(account_no: str, pin: str, new_name: str = "", new_email: str = "", new_pin: str = "") -> dict:
    """Update mutable account fields."""
    data = _load_data()
    for user in data:
        if user["account_no"] == account_no and str(user["pin"]) == str(pin):
            if new_name.strip():
                user["name"] = new_name.strip()
            if new_email.strip():
                # Check email uniqueness (ignore self)
                if any(u["email"].lower() == new_email.lower() and u["account_no"] != account_no for u in data):
                    return err("Email is already used by another account.")
                user["email"] = new_email.strip().lower()
            if new_pin.strip():
                if not new_pin.isdigit() or len(new_pin) != 4:
                    return err("New PIN must be exactly 4 digits.")
                user["pin"] = new_pin
            _save_data(data)
            safe = {k: v for k, v in user.items() if k != "pin"}
            return ok(safe, "Account updated successfully.")
    return err("Invalid account number or PIN.")


def delete_account(account_no: str, pin: str) -> dict:
    """Permanently delete an account."""
    data = _load_data()
    for i, user in enumerate(data):
        if user["account_no"] == account_no and str(user["pin"]) == str(pin):
            data.pop(i)
            _save_data(data)
            return ok(message="Account deleted successfully.")
    return err("Invalid account number or PIN.")


def get_all_accounts() -> list:
    """Return all accounts (without PINs) — for admin/debug use."""
    data = _load_data()
    print("DATA LOADED =", data)
    return [{k: v for k, v in u.items() if k != "pin"} for u in data]