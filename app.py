import json
from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

def categorize_transactions(df):
    # Create a mapping of transaction descriptions to categories
    description_mapping = {
         "groceries": "Food",
  "restaurant": "Food",
  "coffee": "Food",
  "supermarket": "Food",
  "clothes": "Clothing",
  "shoes": "Clothing",
  "accessories": "Clothing",
  "utilities": "Utilities",
  "electricity bill": "Utilities",
  "water bill": "Utilities",
  "gas bill": "Utilities",
  "rent": "Housing",
  "mortgage": "Housing",
  "insurance": "Insurance",
  "healthcare": "Insurance",
  "travel": "Travel",
  "transportation": "Transportation",
  "gasoline": "Transportation",
  "car maintenance": "Transportation",
  "entertainment": "Entertainment",
  "movies": "Entertainment",
  "concert": "Entertainment",
  "subscriptions": "Subscriptions",
  "internet": "Subscriptions",
  "streaming services": "Subscriptions",
  "gym": "Fitness",
  "sports": "Fitness",
  "education": "Education",
  "books": "Education",
  "tuition": "Education",
  "donations": "Charity",
  "gifts": "Gifts",
  "shopping": "Shopping",
  "miscellaneous": "Miscellaneous"
    }

    df['Category'] = df['Transaction_Description'].map(description_mapping)
    categorized_transactions = df.groupby('Category')['Transaction_Amount'].sum().reset_index()
    categorized_transactions = categorized_transactions.to_dict(orient='records')
    return categorized_transactions

def calculate_monthly_summary(df):
    # Extract the month and year from the transaction date
    df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'])
    df['Month'] = df['Transaction_Date'].dt.month
    df['Year'] = df['Transaction_Date'].dt.year

    # Group the transactions by month, year, and category, and calculate the total amount
    monthly_summary = df.groupby(['Year', 'Month', 'Category'])['Transaction_Amount'].sum().reset_index()

    # Convert the monthly summary to a list of dictionaries
    monthly_summary = monthly_summary.to_dict(orient='records')

    return monthly_summary


# Endpoint for training and making predictions
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/monthly-summary', methods=['POST'])
def generate_monthly_summary():
    data = request.json
    
    # Load the dataset
    df = pd.DataFrame(data)

    categorized_transactions = categorize_transactions(df)
    monthly_summary = calculate_monthly_summary(df)
    
    summary_data = {
        'categorized_transactions': categorized_transactions,
        'monthly_summary': monthly_summary
    }
    
    # Return the monthly summary as a JSON response
    return jsonify(summary_data)


if __name__ == '__main__':
    app.run(debug = True)
