# app.py - Combined Flask Application for Python ATM Simulator

import flask
from flask import Flask, render_template, request, session, redirect, url_for

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for sessions; change this in production

# Initialize accounts in the session (if not already set)
def init_accounts():
    if 'accounts' not in session:
        session['accounts'] = {'current': 1000.00, 'savings': 500.00}

# ATM Functions (integrated into routes)
def check_balance(account_type):
    init_accounts()  # Ensure accounts are loaded
    accounts = session['accounts']
    if account_type in accounts:
        return accounts[account_type]
    return None

def deposit(account_type, amount):
    init_accounts()
    accounts = session['accounts']
    if account_type in accounts and amount > 0:
        accounts[account_type] += amount
        session['accounts'] = accounts  # Update session
        return True
    return False

def withdraw(account_type, amount):
    init_accounts()
    accounts = session['accounts']
    if account_type in accounts and amount > 0 and amount <= accounts[account_type]:
        if account_type == 'savings' and (accounts[account_type] - amount) < 100:
            return False  # Minimum balance check
        accounts[account_type] -= amount
        session['accounts'] = accounts  # Update session
        return True
    return False

# Flask Routes
@app.route('/')
def index():
    init_accounts()  # Load accounts on first visit
    accounts = session['accounts']
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python ATM Simulator</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to bottom, #007BFF, #28A745);
            color: #fff;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .atm-container {
            background: #ffffff;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
            width: 90%;
            max-width: 600px;
            padding: 20px;
            text-align: center;
        }
        h1 { color: #007BFF; }
        .balance-section { background: #28A745; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
        .transaction-section { margin-bottom: 20px; }
        .menu-section button { background: #007BFF; color: #fff; border: none; padding: 10px; margin: 5px; border-radius: 5px; cursor: pointer; transition: background 0.3s; }
        .menu-section button:hover { background: #0056b3; }
        .account-selection { background: #f8f9fa; color: #000; padding: 10px; border-radius: 8px; margin-top: 10px; }
        .account-selection button { background: #28A745; color: #fff; margin: 5px; padding: 8px; border-radius: 5px; cursor: pointer; transition: background 0.3s; }
        .account-selection button:hover { background: #218838; }
        @media (max-width: 600px) { .atm-container { width: 95%; padding: 10px; } .menu-section button { width: 100%; } }
    </style>
</head>
<body>
    <div class="atm-container">
        <h1>Python ATM Simulator</h1>
        <div class="balance-section">
            <h2><i class="fas fa-wallet"></i> Account Balances</h2>
            <p>Current Account: ${}</p>
            <p>Savings Account: ${}</p>
        </div>
        <div class="transaction-section">
            <h2><i class="fas fa-exchange-alt"></i> Select Transaction</h2>
            <div class="menu-section">
                <form action="/check_balance" method="post">
                    <button type="submit">Check Balance</button>
                </form>
                <form action="/deposit" method="post">
                    <button type="submit">Deposit Funds</button>
                </form>
                <form action="/withdraw" method="post">
                    <button type="submit">Withdraw Funds</button>
                </form>
                <form action="/exit" method="post">
                    <button type="submit">Exit</button>
                </form>
            </div>
        </div>
        <div id="account-selection" class="account-selection" style="display: none;">
            <h3>Select Account:</h3>
            <form action="/process_action" method="post">
                <input type="hidden" id="action" name="action" value="">
                <button type="submit" name="account" value="current">1. Current Account</button>
                <button type="submit" name="account" value="savings">2. Savings Account</button>
            </form>
        </div>
    </div>
    <script>
        // Simple JS to handle flows (basic simulation)
        document.querySelectorAll('.menu-section form button').forEach(button => {
            button.addEventListener('click', (e) => {
                document.getElementById('action').value = e.target.form.action.split('/')[1];  // Set action
                document.getElementById('account-selection').style.display = 'block';  // Show selection
            });
        });
    </script>
</body>
</html>
""".format(accounts['current'], accounts['savings']))  # Inject dynamic balances

@app.route('/process_action', methods=['POST'])
def process_action():
    action = request.form.get('action')
    account = request.form.get('account')
    if action == 'deposit':
        amount = float(request.form.get('amount', 0))  # Assume amount is sent; add to form if needed
        if deposit(account, amount):
            return redirect(url_for('index'))  # Redirect to refresh
        else:
            return "Error in deposit"
    elif action == 'withdraw':
        amount = float(request.form.get('amount', 0))
        if withdraw(account, amount):
            return redirect(url_for('index'))
        else:
            return "Error in withdrawal"
    elif action == 'check_balance':
        balance = check_balance(account)
        return f"Balance for {account}: ${balance}"
    return redirect(url_for('index'))

@app.route('/exit')
def exit_app():
    session.clear()  # Clear session
    return "Session ended. <a href='/'>Return home</a>"

if __name__ == '__main__':
    app.run(debug=True)
