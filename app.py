from flask import Flask, render_template, request, session, redirect, url_for

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # In production, use a secure key

# Initialize accounts in the session (if not already set)
def init_accounts():
    if 'accounts' not in session:
        session['accounts'] = {'current': 1000.00, 'savings': 500.00}

# ATM Logic
def check_balance(account_type):
    init_accounts()
    accounts = session['accounts']
    return accounts.get(account_type, None)

def deposit(account_type, amount):
    init_accounts()
    accounts = session['accounts']
    if account_type in accounts and amount > 0:
        accounts[account_type] += amount
        session['accounts'] = accounts
        return True
    return False

def withdraw(account_type, amount):
    init_accounts()
    accounts = session['accounts']
    if account_type in accounts and amount > 0 and amount <= accounts[account_type]:
        if account_type == 'savings' and (accounts[account_type] - amount) < 100:
            return False  # Minimum balance rule
        accounts[account_type] -= amount
        session['accounts'] = accounts
        return True
    return False

# Routes
@app.route('/')
def index():
    init_accounts()
    accounts = session['accounts']
    return render_template('index.html',
                           current=accounts['current'],
                           savings=accounts['savings'])

@app.route('/process_action', methods=['POST'])
def process_action():
    action = request.form.get('action')
    account = request.form.get('account')
    amount = float(request.form.get('amount', 0))

    if action == 'deposit':
        if deposit(account, amount):
            return redirect(url_for('index'))
        else:
            return "Error in deposit"
    elif action == 'withdraw':
        if withdraw(account, amount):
            return redirect(url_for('index'))
        else:
            return "Error in withdrawal"
    elif action == 'check_balance':
        balance = check_balance(account)
        return f"Balance for {account}: ${balance:.2f}"
    
    return redirect(url_for('index'))

@app.route('/exit', methods=['POST'])
def exit_app():
    session.clear()
    return "Session ended. <a href='/'>Return home</a>"

if __name__ == '__main__':
    app.run(debug=True)
