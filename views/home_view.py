from flask import render_template, request, redirect, session, jsonify

from controllers.session_controller import delete_session_by_user_id
from controllers.db.user_controller import *

from controllers.db.component_controller import translate
from views.home.options_menu_view import init_options_menu
from views.home.edit_component_view import init_edit_component_menu
from views.home.help_view import init_help
from logger_settings import setup_logger

# Настрофка логов
logger = setup_logger("home")
logger.info("Запуск главное страницы")

def init_home(app):
    init_help(app)
    init_options_menu(app)
    init_edit_component_menu(app)

    @app.route('/home')
    def home():
        if 'user_id' not in session:
            return redirect('/login')

        return render_template('home.html', user_data=get_user_data(session['user_id']))

    @app.route('/logout')
    def logout():
        user_id = session.get("user_id")
        if user_id:
            delete_session_by_user_id(user_id)
            session.clear()

        return redirect('/login')

    @app.route('/translate', methods=['POST'])
    def translate_view():
        data = request.json
        result = translate(data.get('name'), data.get('capitalize'))
        return jsonify({"result": result})   
