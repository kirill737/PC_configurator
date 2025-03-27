from flask import Flask, render_template, request, redirect, session, jsonify
from database.psql import get_psql_db_connection

from controllers.session_controller import delete_session_by_user_id
from controllers.db.user_controller import *

from controllers.db.component_controller import ComponentType as CT, componentTypes, type2fields_dict

from logger_settings import setup_logger

# Настрофка логов
logger = setup_logger("component-settings")
logger.info("Запуск меню насроек комплектующих")

def init_component_settings_menu(app):
    
    @app.route('/open/<ct>')
    def open_settings(ct: CT):
        logger.info(f"Открытие настроек {ct}")
        result_json = {}
        for field in type2fields_dict[ct]:
            # result_json[field] = 
            # Написать функцию которая будет по component_id 
            # возвращать заполненный словарь полей комплектующей
            pass
        return 

    @app.route('/open_wishlists')
    def open_wishlists():
        return redirect('/home')
    
    # Боковое меню
    @app.route("/api/builds")
    def get_builds():
        logger.info("Нажали на кнопку выбора сборки")
        builds = get_user_builds(session['user_id'])
        # conn = get_psql_db_connection()
        # cur = conn.cursor()
        # cur.execute("SELECT id, name FROM builds")
        # builds = [{"id": row[0], "name": row[1]} for row in cur.fetchall()]
        # cur.close()
        # conn.close()
        return jsonify(builds)