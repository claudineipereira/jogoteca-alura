#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for
from flask import session, flash


class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console


class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha


app = Flask(__name__)
app.secret_key = 'abcdef'

usuario1 = Usuario('dinei', 'Claudinei Pereira', 'cepk')
usuarios = {
    usuario1.id: usuario1
}

jogo1 = Jogo('Super Mario', 'Ação', 'SNES')
jogo2 = Jogo('Podemon Gold', 'RPG', 'GBA')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'SNES')
jogos = [jogo1, jogo2, jogo3]

@app.route('/')
def index():
    titulo = 'Jogos'
    return render_template('lista.html', titulo=titulo, jogos=jogos)

@app.route('/novo')
def novo():
    titulo='Novo Jogo'
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo=titulo)

@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    jogos.append(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    titulo = 'Faça seu login'
    proxima = request.args.get('proxima')
    return render_template('login.html', titulo=titulo, proxima=proxima)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    flash('Não logado, tente novamente.')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5200, debug=1)