from flask import Flask, render_template, request, redirect, session, jsonify
from database.psql import get_psql_db_connection

from controllers.session_controller import delete_session_by_user_id
from controllers.db.user_controller import *

from controllers.db.component_controller import *
from controllers.db.build_component_controller import change_component

from logger_settings import setup_logger

# Настрофка логов
logger = setup_logger("main_menu")
logger.info("Запуск меню насроек комплектующих")

def init_component_settings_menu(app):
    @app.route('/get/<int:component_id>/fields')
    def component_fields(component_id: int):
        logger.info(f"Открытие настроек коплектующей{component_id}")
        component_fields = get_components_fields(component_id)
        return component_fields
    
    @app.route('/create/component/fields', methods=['POST'])
    def create_component_fields():
        ct = request.json.get('ct')
        logger.info(f"Создание новой компектующей: {ct}")
        
        component_field_names_rus = [field.capitalize() for field in type2fields_rus_dict[ct]]
        component_field_names = type2fields_dict[ct]
        result = {
            'fields': component_field_names,
            'fields_rus': component_field_names_rus
        }
        return jsonify(result)
    
    @app.route("/create/component", methods=["POST"])
    def create_new_component():
        data = request.json
        ct = data.get('ct')
        logger.info(f"Создание новой комплектующей: {ct}")
        if add_component(ct, data.get('price'), data.get('info')):
            return jsonify({"status": "success"})
        return jsonify({"status": "error", "message": "Failed to create component"})
    
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
    
    @app.route('/update/build/component', methods=['POST'])
    def change_component_view():
        dataJson = request.json
        data = {
            'build_id': dataJson.get('build_id'),
            'old_id': dataJson.get('old_id'),
            'new_id': dataJson.get('new_id')
        }
        change_component(
            build_id=data['build_id'], 
            old_id=data['old_id'],
            new_id=data['new_id']
        )
        return '', 204
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

    @app.route('/get/component/data/<int:component_id>')
    def component_data(component_id: int):
        logger.info(f"Получения информации о комплектующей: {component_id}")
        data_dict = get_component_data(component_id)
        
        return data_dict