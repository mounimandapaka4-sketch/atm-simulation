import flask
from flask import Flask, request, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For sessions; change in production

# Initialize variables as in your code
balance = 1000.00
pin = "1234"  # Hardcoded for demo; use secure storage in real apps
transaction_history = []

def verify_pin(entered_pin):
    """Helper to verify PIN as in your code."""
    return entered_pin == pin

@app.route('/check-balance', methods=['GET'])
def check_balance_route():
    """API endpoint for checking balance."""
    return jsonify({'balance': balance})

@app.route('/deposit', methods=['POST'])
def deposit_route():
    """API endpoint for deposit, based on your deposit function."""
    data = request.json
    entered_pin = data.get('pin')
    amount = data.get('amount')
    
    if not verify_pin(entered_pin):
        return jsonify({'error': 'Incorrect PIN. Deposit cancelled.'}), 401
    
    if amount and amount > 0:
        global balance
        balance += amount
        transaction = f"Deposited ${amount:.2f}"
        transaction_history.append(transaction)
        return jsonify({'message': f'Deposit successful! New balance: ${balance:.2f}', 'balance': balance})
    else:
        return jsonify({'error': 'Deposit amount must be greater than zero.'}), 400

@app.route('/withdraw', methods=['POST'])
def withdraw_route():
    """API endpoint for withdrawal, based on your withdraw function."""
    data = request.json
    entered_pin = data.get('pin')
    amount = data.get('amount')
    
    if not verify_pin(entered_pin):
        return jsonify({'error': 'Incorrect PIN. Withdrawal cancelled.'}), 401
    
    if amount > balance:
        return jsonify({'error': 'Insufficient funds for this withdrawal.'}), 400
    elif amount <= 0:
        return jsonify({'error': 'Withdrawal amount must be greater than zero.'}), 400
    else:
        global balance
        balance -= amount
        transaction = f"Withdrew ${amount:.2f}"
        transaction_history.append(transaction)
        
        history = "\n".join([f"{i}. {trans}" for i, trans in enumerate(transaction_history, start=1)])
        return jsonify({
            'message': f'Withdrawal successful! New balance: ${balance:.2f}',
            'balance': balance,
            'history': history if transaction_history else 'No transactions yet.'
        })

@app.route('/')
def serve_index():
    return flask.send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
