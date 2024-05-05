from flask_login import UserMixin
from apirecuperacao import database, login_manager
from sqlalchemy import Float

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)

class Transacoes(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String)
    email = database.Column(database.String)
    status = database.Column(database.String)
    valor = database.Column(Float)
    forma_pagamento = database.Column(database.String)
    parcelas = database.Column(database.Integer)
    acesso_curso = database.Column(database.String)
    enviar_mensagem = database.Column(database.String)
    tipo_mensagem = database.Column(database.String)
