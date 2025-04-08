from flask import Flask, render_template, request, redirect, session, jsonify
from database.psql import get_psql_db_connection

from controllers.session_controller import delete_session_by_user_id
from controllers.db.user_controller import *

from controllers.db.component_controller import translate
from views.home.options_menu_view import init_options_menu

from logger_settings import setup_logger

# Настрофка логов
logger = setup_logger("home")
logger.info("Запуск главное страницы")

def init_home(app):
    init_options_menu(app)
    # init_component_settings_menu(app)
    @app.route('/home')
    def home():
        if 'user_id' not in session:
            return redirect('/login')
        
        conn = get_psql_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM components;")
        components = cur.fetchall()
        cur.close()
        conn.close()

        return render_template('home.html', user_data=get_user_data(session['user_id']))

    @app.route('/logout')
    def logout():
        user_id = session.get("user_id")
        if user_id:
            delete_session_by_user_id(user_id)
            session.clear()
        # session.pop('user', None)
        return redirect('/login')

    @app.route('/translate', methods=['POST'])
    def translate_view():
        data = request.json
        result = translate(data.get('name'), data.get('capitalize'))
        return jsonify({"result": result})   
