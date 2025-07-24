from flask_sqlalchemy import SQLAlchemy
from datetime import date


db = SQLAlchemy()


class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    due_day = db.Column(db.Integer, nullable=False)
    recurring = db.Column(db.Boolean, default=True)


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.Integer, db.ForeignKey('bill.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    paid = db.Column(db.Boolean, default=False)
    amount = db.Column(db.Float, nullable=False)

    bill = db.relationship('Bill', backref=db.backref('payments', lazy=True))

    @staticmethod
    def for_month(year: int, month: int):
        return Payment.query.filter_by(year=year, month=month).all()

    @staticmethod
    def reset_month(year: int, month: int):
        bills = Bill.query.filter_by(recurring=True).all()
        for bill in bills:
            payment = Payment(bill_id=bill.id, year=year, month=month,
                              amount=bill.amount, paid=False)
            db.session.add(payment)
        db.session.commit()

    @staticmethod
    def current_year_month():
        today = date.today()
        return today.year, today.month
