from flask import Flask, render_template, request, redirect, session, jsonify
from database.psql import get_psql_db_connection

from controllers.session_controller import delete_session_by_user_id
from controllers.db.user_controller import *

from controllers.db.component_controller import *

from logger_settings import setup_logger

# Настрофка логов
logger = setup_logger("component-settings")
logger.info("Запуск меню насроек комплектующих")

def init_component_settings_menu(app):
    
    @app.route('/open/<int:component_id>/fields')
    def open_field_settings(component_id: int):
        logger.info(f"Открытие настроек коплектующей{component_id}")
        component_fields = get_component_fields(component_id)
        return component_fields
    
    @app.route('/create/component', methods=['POST'])
    def create_new_component():
        ct = request.json.get('ct')
        logger.info(f"Создание новой компектующей: {ct}")
        component_field_names = type2fields_dict[ct]
        return component_field_names
    
    # Боковое меню
    # @app.route("/api/builds")
    # def get_builds():
    #     logger.info("Нажали на кнопку выбора сборки")
    #     builds = get_user_builds(session['user_id'])
    #     # conn = get_psql_db_connection()
    #     # cur = conn.cursor()
    #     # cur.execute("SELECT id, name FROM builds")
    #     # builds = [{"id": row[0], "name": row[1]} for row in cur.fetchall()]
    #     # cur.close()
    #     # conn.close()
    #     return jsonify(builds)