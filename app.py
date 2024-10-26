from flask import Flask, request, render_template, redirect, flash, session
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'
users = {}  

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session['username'] = username 
            return redirect('/home2')
        else:
            flash('Invalid Username or Password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fname = request.form['firstname']
        lname = request.form['lastname']
        username = request.form['username']
        password = request.form['password']
        
        if username not in users:
            users[username] = generate_password_hash(password)
            flash('Registration successful!') 
            return redirect('/home2') 
        else:
            flash('Username already exists!') 
            return redirect('/register')
    return render_template('register.html')

@app.route('/home2')
def home2():
    return render_template('home2.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/financial_review')
def financial_review():
    return render_template('financial_review.html')

@app.route('/savings_calendar')
def savings_calendar():
    return render_template('savings_calendar.html')

@app.route('/mydreams')
def mydreams():
    return render_template('mydreams.html')

@app.route('/creategoal')
def creategoal():
    return render_template('creategoal.html')

@app.route('/notepad')
def notepad():
    return render_template('notepad.html')

@app.route('/services')
def services():
    return render_template('services.html')
    

@app.route('/month', methods=['POST'])
def calculate_review():
    try:
        income = float(request.form['income'])
        rent = float(request.form['rent'])
        utilities = float(request.form['utilities'])
        groceries = float(request.form['groceries'])
        credit_loan = float(request.form['credit_loan'])
        other_expenses = float(request.form['other_expenses'])
    except ValueError:
        flash('Please enter valid numbers for income and expenses.')
        return redirect('/home2')

    total_expenses = rent + utilities + groceries + credit_loan + other_expenses
    remaining_amount = income - total_expenses

    savings = remaining_amount * 0.50
    entertainment = remaining_amount * 0.10
    personal_use = remaining_amount * 0.10
    emergency = remaining_amount * 0.10
    dream = remaining_amount * 0.20

    return render_template('month.html', 
                           remaining_amount=remaining_amount,
                           savings=savings,
                           entertainment=entertainment,
                           personal_use=personal_use,
                           emergency=emergency,
                           dream=dream)  

@app.route('/daily', methods=['POST'])
def calculate_daily_review():
    income = float(request.form['income'])
    rent = float(request.form['rent'])
    utilities = float(request.form['utilities'])
    groceries = float(request.form['groceries'])
    credit_loan = float(request.form['credit_loan'])
    other_expenses = float(request.form['other_expenses'])

    # Calculate total expenses and remaining income
    total_expenses = rent + utilities + groceries + credit_loan + other_expenses
    remaining_amount = income - total_expenses

    # Calculate daily amount (assuming 30 days in a month)
    daily_amount = remaining_amount / 30

    # Calculate daily allocations for savings, entertainment, personal use, emergency
    savings = daily_amount * 0.50
    entertainment = daily_amount * 0.10
    personal_use = daily_amount * 0.10
    emergency = daily_amount * 0.10
    dream = daily_amount * 0.20  

    return render_template('daily.html', 
                           remaining_amount=daily_amount,
                           savings=savings,
                           entertainment=entertainment,
                           personal_use=personal_use,
                           emergency=emergency,
                           dream=dream) 
    
@app.route('/weekly', methods=['POST'])
def calculate_weekly_review():
    income = float(request.form['income'])
    rent = float(request.form['rent'])
    utilities = float(request.form['utilities'])
    groceries = float(request.form['groceries'])
    credit_loan = float(request.form['credit_loan'])
    other_expenses = float(request.form['other_expenses'])

    # Calculate total expenses and remaining income
    total_expenses = rent + utilities + groceries + credit_loan + other_expenses
    remaining_amount = income - total_expenses

    # Calculate weekly amount (assuming 4 weeks in a month)
    weekly_amount = remaining_amount / 4

    # Calculate weekly allocations for savings, entertainment, personal use, emergency
    savings = weekly_amount * 0.50
    entertainment = weekly_amount * 0.10
    personal_use = weekly_amount * 0.10
    emergency = weekly_amount * 0.10
    dream = weekly_amount * 0.20  

    return render_template('weekly.html', 
                           remaining_amount=weekly_amount,
                           savings=savings,
                           entertainment=entertainment,
                           personal_use=personal_use,
                           emergency=emergency,
                           dream=dream)  

@app.route('/savings_calendar', methods=['POST'])
def calculate_dream():
    dream_amount = float(request.form['dream_amount'])
    dream_date = request.form['dream_date']
    today = datetime.now()

    try:
        target_date = datetime.strptime(dream_date, '%Y-%m-%d')
    except ValueError:
        flash('Please enter a valid date in YYYY-MM-DD format.')
        return redirect('/home2')

    total_days = (target_date - today).days
    total_months = (total_days // 30) + (1 if total_days % 30 > 0 else 0)  # Round up for partial months

    if total_days <= 0:
        flash('The target date must be in the future.')
        return redirect('/home2')

    # Calculate daily and monthly savings needed
    daily_savings = dream_amount / total_days
    monthly_savings = dream_amount / total_months if total_months > 0 else 0

    # Prepare a list of days for the calendar
    days = [{'date': (today + timedelta(days=i)).strftime('%Y-%m-%d')} for i in range(total_days)]

    # Redirect to a new page with the savings calendar
    return render_template('savings_calendar.html', 
                           dream_amount=dream_amount, 
                           dream_date=dream_date, 
                           daily_savings=daily_savings, 
                           monthly_savings=monthly_savings, 
                           days=days)


if __name__ == '__main__':
    app.run(debug=True)
