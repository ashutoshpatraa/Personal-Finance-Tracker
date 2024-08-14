from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

# Directory setup
if not os.path.exists('data'):
    os.makedirs('data')

# CSV file setup
csv_file = 'data/transactions.csv'

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Function to add transaction
@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        category = request.form['category']
        date = request.form['date']
        
        # Check if CSV file exists
        if not os.path.isfile(csv_file):
            df = pd.DataFrame(columns=['amount', 'category', 'date'])
            df.to_csv(csv_file, index=False)
        
        # Append new transaction to CSV
        df = pd.read_csv(csv_file)
        new_transaction = pd.DataFrame([[amount, category, date]], columns=['amount', 'category', 'date'])
        
        # Ensure the DataFrame is not empty before concatenation
        if not new_transaction.empty:
            df = pd.concat([df, new_transaction], ignore_index=True)
            df.to_csv(csv_file, index=False)
        
        return redirect(url_for('add_transaction'))
    
    return render_template('add_transaction.html')

# Function to visualize data
@app.route('/visualize')
def visualize_data():
    df = pd.read_csv(csv_file)
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df, x='date', y='amount', hue='category')
    plt.savefig('static/visualization.png')
    plt.close()
    return render_template('visualize_data.html')

# Function to generate report
@app.route('/report')
def generate_report():
    df = pd.read_csv(csv_file)
    report = df.groupby('category').sum()
    return render_template('generate_report.html', report=report.to_html())

if __name__ == "__main__":
    app.run(debug=True)