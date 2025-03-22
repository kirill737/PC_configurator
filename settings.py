from flask import Flask, render_template, request, redirect, session
from controllers.session_controller import *

def init_settings(app):

    @app.route('/open_settings_page')
    def open_settings_page():
        return render_template('settings.html', user_data=get_user_data(session['user_id']))

    @app.route('/save_settings', methods=['GET', 'POST'])
    def save_settings():
        logging.info("Страница настроек")
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')

            if login_code == 1: # Введён верный пароль
                logging.info(f"Пользователь {email} ввёл верный пароль")
                user_id = get_user_id(email)
                
                session_id = create_session(user_id)
                logging.info(f"Сессия {session_id} - началась")
                session["user_id"] = get_user_id(email)
                
                return redirect('/dashboard')
            elif login_code == -1:
                logging.info(f"Пользователь с почтой {email} не найден")
                return render_template('login.html', error='Пользователь не найден')
            else:
                logging.info(f"Неверный пароль пользователя {email}")
                return render_template('login.html', error='Неверный пароль')

        return render_template('login.html', error=None)
