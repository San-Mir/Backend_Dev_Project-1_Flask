import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# File to store customer data
DATA_FILE = 'customer_data.json'

def load_data():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return [] # Returns whatever is stored in JSON file

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Load customer data at startup
customer_data = load_data()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/customer-details')
def customer_details():
    return render_template('customer_details.html', customers=customer_data)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    message = request.form['message']
    customer_data.append({
        'name': name,
        'email': email,
        'phone': phone,
        'message': message
    })
    save_data(customer_data)
    return redirect(url_for('customer_details'))

@app.route('/delete/<int:index>', methods=['POST'])
def delete(index):
    if 0 <= index < len(customer_data):
        del customer_data[index]
        save_data(customer_data)
    return redirect(url_for('customer_details'))

if __name__ == '__main__':
    app.run()
