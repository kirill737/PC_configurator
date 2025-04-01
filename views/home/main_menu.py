from flask import Flask, render_template, request, redirect, session, jsonify
from database.psql import get_psql_db_connection

from controllers.session_controller import delete_session_by_user_id
from controllers.db.user_controller import *

from controllers.db.component_controller import *

from logger_settings import setup_logger

# Настрофка логов
logger = setup_logger("main_menu")
logger.info("Запуск меню насроек комплектующих")

def init_component_settings_menu(app):
    
    @app.route('/get/<int:component_id>/fields')
    def component_fields(component_id: int):
        logger.info(f"Открытие настроек коплектующей{component_id}")
        component_fields = get_component_fields(component_id)
        return component_fields
    
    @app.route('/create/component', methods=['POST'])
    def create_new_component():
        ct = request.json.get('ct')
        logger.info(f"Создание новой компектующей: {ct}")
        component_field_names = type2fields_dict[ct]
        return component_field_names
    
    @app.route('/get/all/components/type/<ct>')
    def get_all_components(ct: ComponentType):
        logger.info(f"Получение всех деталей типа {ct}")
        components_list = get_all_component_by_type(ct)
        return components_list
    
    @app.route('/get/current/component/data')
    def current_component_data():
        logger.info("Попытка получить данные")
        data = {
            'ct': session['ct'],
            'build_id': session['build_id']
        }
        return data
    
    @app.route('/set/current/component/data/build_id', methods=['POST'])
    def set_current_component_build_id():
        logger.info("Попытк установить данные (build_id)...")
        dataJson = request.json
        data = {
            'build_id': dataJson.get('build_id')
        }
        session['build_id'] = data['build_id']
        logger.info(f"Data changed to {data}")
        return data
    @app.route('/set/current/component/data/ct', methods=['POST'])
    def set_current_component_type():
        logger.info("Попытка установить данные (ct)...")
        dataJson = request.json
        data = {
            'ct': dataJson.get('ct')
        }
        session['ct'] = data['ct']
        logger.info(f"Data changed to {data}")
        return data

    @app.route('/get/build/info/<int:build_id>')
    def build_info(build_id: int):
        logger.info(f"Получения краткой информации о сборке: {build_id}")
        data = get_build_info(build_id)