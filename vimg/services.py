from flask import redirect, flash
from flask.helpers import url_for
from vimg.models import User
from vimg import db

class UserService:
    
    def save(request):
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        user = User(first_name, last_name, email, password)

        if user.is_valid():
            try:
                db.session.add(user)
                db.session.commit()
                flash('Cadastro realizado com sucesso!', 'success')
            except:
                flash('Erro! Não possível cadastrar seu usuário. Por favor, entre em contato com o suporte.', 'error')
            return redirect(url_for('home'))
        else:
            flash('Erro! As informações fornecidas não são válidas.', 'error')
            return redirect(url_for('home'))