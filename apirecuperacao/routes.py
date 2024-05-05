from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from flask_paginate import Pagination
from sqlalchemy import or_
from apirecuperacao import app, database, bcrypt
from apirecuperacao.forms import FormEntrar, FormCadastro
from apirecuperacao.models import Usuario, Transacoes


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Cria a rota para um endpoint especificado

    Args:
        None

    Returns:
        Página para a qual a rota leva
    """
    form_entrar = FormEntrar()
    if form_entrar.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_entrar.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_entrar.senha.data):
            login_user(usuario, remember=form_entrar.lembrar_senha.data)
            flash(
                'Login feito com sucesso', 'alert-success')
            p_next = request.args.get('next')
            if p_next:
                return redirect(p_next)
            else:
                return redirect(url_for('clientes'))
        else:
            flash('Email ou senha inválidos. Tente novamente!', 'alert-danger')
            return redirect(url_for('home'))
    return render_template('home.html', form_entrar=form_entrar)


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    """
    Cria a rota para um endpoint especificado

    Args:
        None

    Returns:
        Página para a qual a rota leva
    """
    form_cadastro = FormCadastro()
    if form_cadastro.validate_on_submit():
        if form_cadastro.token_acess.data != 'uhdfaAADF123':
            flash('Token incorreto. Tente novamente.', 'alert-danger')
            return redirect(url_for('cadastro'))
        senha_cript = bcrypt.generate_password_hash(form_cadastro.senha.data)
        usuario = Usuario(
            nome=form_cadastro.nome.data, email=form_cadastro.email.data, senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        flash(
            'Cadastro feito com sucesso', 'alert-success')
        return redirect(url_for("home"))
    return render_template('cadastro.html', form_cadastro=form_cadastro)


@app.route('/transacoes')
@login_required
def clientes():
    """
    Cria a rota para um endpoint especificado

    Args:
        None

    Returns:
        Página para a qual a rota leva 
    """
    page = request.args.get('page', 1, type=int)
    per_page = 50
    filtro = request.args.get('filtro', 'id')
    termo = request.args.get('termo', '')

    campos_filtro = {
        'id': Transacoes.id,
        'nome': Transacoes.nome,
        'email': Transacoes.email,
        'status': Transacoes.status,
    }

    campo = campos_filtro[filtro]

    if filtro != 'id':
        lista_clientes = Transacoes.query.filter(campo.like(
            f"%{termo}%")).paginate(page=page, per_page=per_page)
    else:
        lista_clientes = Transacoes.query.paginate(
            page=page, per_page=per_page)
    return render_template('transacoes.html', lista_clientes=lista_clientes)


@app.route('/sair')
@login_required
def sair():
    """
    Cria a rota para fazer o logout do usuário

    Args:
        None

    Returns:
        Página para a qual a rota leva 
    """
    logout_user()
    return redirect(url_for('home'))


@app.route('/webhook', methods=['POST'])
def webhook():

    def alimentar_banco(acesso_curso, enviar_mensagem, tipo_mensagem):
        transacao = Transacoes(
            nome=data['nome'],
            email=data['email'],
            status=data['status'],
            valor=data['valor'],
            forma_pagamento=data['forma_pagamento'],
            parcelas=data['parcelas'],
            acesso_curso=acesso_curso,
            enviar_mensagem=enviar_mensagem,
            tipo_mensagem=tipo_mensagem
        )
        database.session.add(transacao)
        database.session.commit()

    if request.method == 'POST':
        data = request.json
        if data['status'] == 'aprovado':
            print(
                f'Liberar acesso do curso para o email: {data["email"]}')
            print(
                f'Enviar mensagem de boas vindas para o email: {data["email"]}')
            alimentar_banco('liberado', 'sim', 'boas vindas')
        elif data['status'] == 'recusado':
            print(
                f'Enviar mensagem de Pagamento Recusado para o email: {data["email"]}')
            alimentar_banco('bloqueado', 'sim', 'pagamento recusado')
        else:
            print(
                f'Retirar acesso do curso para o email: {data["email"]}')
            alimentar_banco('retirado', 'nao', '')
        return 'Recebido com sucesso', 200
    else:
        return 'Método não permitido', 405
