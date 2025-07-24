from flask import Flask, render_template, request, redirect, url_for
from models import db, Bill, Payment
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///homeeconomy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.cli.command('db_init')
def db_init():
    """Initialize the database."""
    db.create_all()
    year, month = Payment.current_year_month()
    Payment.reset_month(year, month)
    print('Database initialized.')


@app.route('/')
def index():
    year, month = Payment.current_year_month()
    payments = Payment.for_month(year, month)
    if not payments:
        Payment.reset_month(year, month)
        payments = Payment.for_month(year, month)
    return render_template('index.html', payments=payments, year=year, month=month)


@app.route('/toggle/<int:payment_id>')
def toggle(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    payment.paid = not payment.paid
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        amount = float(request.form['amount'])
        due_day = int(request.form['due_day'])
        recurring = 'recurring' in request.form
        bill = Bill(name=name, amount=amount, due_day=due_day, recurring=recurring)
        db.session.add(bill)
        db.session.commit()
        year, month = Payment.current_year_month()
        if recurring:
            Payment.reset_month(year, month)
        else:
            payment = Payment(bill_id=bill.id, year=year, month=month, amount=amount, paid=False)
            db.session.add(payment)
            db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')


if __name__ == '__main__':
    app.run(debug=True)
