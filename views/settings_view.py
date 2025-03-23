from flask import Flask, render_template, request, redirect, session
from controllers.session_controller import *
from controllers.db.user_controller import change_user_data_by_user_id

from logger_settings import setup_logger



logger = setup_logger("settings")
logger.info("Загрузка страницы с данными пользователя")

def init_settings(app):
    @app.route('/open_settings_page')
    def open_settings_page():
        return render_template('settings.html', user_data=get_user_data(session['user_id']))

    @app.route('/save_settings', methods=['GET', 'POST'])
    def save_settings():
    
        if request.method == 'POST':
            logger.info("Сохроняем данные...")
            new_user_data = {
                'username': request.form.get('username'),
                'email': request.form.get('email'),
                'password': request.form.get('password')
            }
            user_id = session['user_id']
            try:
                logger.info(f"Меняем данные о пользователе {user_id} на:\n {new_user_data}")
                change_user_data_by_user_id(user_id, new_user_data)
                logger.info(f"Данные успешно сохранены")
            except Exception as e:
                logger.error(f"Ошибка при смене данных {e}")
                render_template('settings.html', user_data=get_user_data(user_id))

            # return render_template('login.html', error='Неверный пароль')

        return render_template('settings.html', user_data=get_user_data(user_id), error=None)
