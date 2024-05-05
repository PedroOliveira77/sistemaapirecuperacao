from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from apirecuperacao.models import Usuario


class FormCadastro(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(4, 10)])
    confirmacao_senha = PasswordField('Confirmação de Senha', validators=[
                                      DataRequired(), EqualTo('senha')])
    btn_submit_cadastro = SubmitField('Fazer Cadastro')
    token_acess = StringField('Token', validators=[DataRequired()])

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError(
                'E-mail já cadastrado. Faça login para continuar')


class FormEntrar(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(4, 10)])
    lembrar_senha = BooleanField('Lembrar senha')
    btn_submit_entrar = SubmitField('Entrar')

