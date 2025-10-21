from flask import Flask, render_template, request, redirect
import csv
import os
from datetime import datetime

app = Flask(__name__)

# Restaurant name (change here if needed)
RESTAURANT_NAME = "Hot N Spicy"

CSV_FILE = 'feedback.csv'
HEADERS = [
    "timestamp", "branch", "order_no", "server", "table_no",
    "name", "mobile", "heard_about", "visits",
    "experience_emoji", "what_you_liked", "favorite_item",
    "smaller_portion", "liked_items"
]

# Create CSV with header if it doesn't exist
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(HEADERS)

@app.route('/')
def index():
    # servers and table options passed to template
    branches = ["Malier", "Khada", "Rahat", "Tower", "Nazimabad"]
    servers = ["Ali", "Zain", "Safdar", "Nasi", "Saad", "Asad"]
    tables = [f"Table {i}" for i in range(1, 21)]
    heard_options = [
        "Friends or Family", "Social Media", "Google / Maps",
        "Walk-in / Nearby", "Food Delivery App", "Other"
    ]
    return render_template('index.html',
                           restaurant=RESTAURANT_NAME,
                           branches=branches,
                           servers=servers,
                           tables=tables,
                           heard_options=heard_options)

@app.route('/submit', methods=['POST'])
def submit():
    # Collect form fields
    branch = request.form.get('branch', '').strip()
    order_no = request.form.get('order_no', '').strip()
    server = request.form.get('server', '').strip()
    table_no = request.form.get('table_no', '').strip()
    name = request.form.get('name', '').strip()
    mobile = request.form.get('mobile', '').strip()
    heard_about = request.form.get('heard_about', '').strip()
    visits = request.form.get('visits', '').strip()
    experience = request.form.get('experience', '').strip()
    what_liked = request.form.get('what_liked', '').strip()
    favorite_item = request.form.get('favorite_item', '').strip()
    smaller_portion = request.form.get('smaller_portion', '').strip()
    liked_items = request.form.getlist('liked_items')

    liked_items_str = ';'.join(liked_items)

    row = [
        datetime.now().isoformat(), branch, order_no, server, table_no,
        name, mobile, heard_about, visits,
        experience, what_liked, favorite_item,
        smaller_portion, liked_items_str
    ]

    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(row)

    return redirect('/thankyou')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html', restaurant=RESTAURANT_NAME)

if __name__ == '__main__':
    app.run(debug=True)
