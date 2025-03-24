from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Cliente(db.Model):
    __tablename__ = 'cliente'
    idClient = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)
    dir = db.Column(db.String(255), nullable=False)
    tel = db.Column(db.String(100), nullable=False)
    fechaCom = db.Column(db.Date, nullable=False)

class Orden(db.Model):
    __tablename__ = 'orden'
    idOrden = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tam = db.Column(db.String(100), nullable=False)
    ing = db.Column(db.String(100), nullable=False)
    num = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.Integer, default=1, nullable=False)
    fechaCom = db.Column(db.Date, default=datetime.date.today, nullable=False)
    idClient = db.Column(db.Integer, db.ForeignKey('cliente.idClient'), nullable=False)
    cliente = db.relationship('Cliente', backref=db.backref('ordenes', lazy=True))