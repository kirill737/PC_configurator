from flask import render_template, request, redirect, session

from controllers.session_controller import create_session
from controllers.db.user_controller import *


from logger_settings import setup_logger


# Настрофка логов
logger = setup_logger("login")
logger.info("Загрузка страница входа")

def init_login(app):
    @app.route('/open_login_page')
    def open_login_page():
        return redirect('/login')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        logger.info("Страница входа")
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            login_code = check_user_login_data(email, password)

            if login_code == 1: # Введён верный пароль
                logger.info(f"Пользователь {email} ввёл верный пароль")
                user_id = get_user_id(email)
                
                session_id = create_session(user_id)
                
                logger.info(f"Сессия {session_id} - началась")
                session["user_id"] = get_user_id(email)
                
                return redirect('/home')
            elif login_code == -1:
                logger.info(f"Пользователь с почтой {email} не найден")
                return render_template('login.html', error='Пользователь не найден')
            else:
                logger.info(f"Неверный пароль пользователя {email}")
                return render_template('login.html', error='Неверный пароль')

        return render_template('login.html', error=None)

