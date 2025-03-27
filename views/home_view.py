from flask import Flask, render_template, request, redirect, session, jsonify
from database.psql import get_psql_db_connection

from controllers.session_controller import delete_session_by_user_id
from controllers.db.user_controller import *


from views.side_menu_view import init_side_menu
from views.component_settings import init_component_settings_menu

from logger_settings import setup_logger

# Настрофка логов
logger = setup_logger("home")
logger.info("Запуск главное страницы")

def init_home(app):
    init_side_menu(app)
    init_component_settings_menu(app)
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

   
