from flask import Flask, render_template, request, redirect, session
from controllers.session_controller import *
from controllers.db.user_controller import change_user_data_by_user_id
import logging

logging.basicConfig(
    filename="logs/pc_config_settings.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S"
)

def init_settings(app):
    @app.route('/open_settings_page')
    def open_settings_page():
        return render_template('settings.html', user_data=get_user_data(session['user_id']))

    @app.route('/save_settings', methods=['GET', 'POST'])
    def save_settings():
        logging.info("Страница настроек")
        if request.method == 'POST':
            new_user_data = {
                'username': request.form.get('username'),
                'email': request.form.get('email'),
                'password': request.form.get('password')
            }

            try:
                change_user_data_by_user_id(session['user_id'], new_user_data)
            except Exception as e:
                logging.error(f"Ошибка при смене данных {e}")
                render_template('settings.html', error={e})

            # return render_template('login.html', error='Неверный пароль')

        return render_template('settings.html', error=None)
