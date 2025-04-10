from flask import Flask, render_template, request, redirect, session, jsonify



from controllers.db.user_controller import *

from controllers.db.component_controller import *
from controllers.db.build_component_controller import change_build_component, get_component_id

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
    
    
    
    @app.route('/change/build/component', methods=['POST'])
    def change_build_component_view():
        dataJson = request.json
        data = {
            'build_id': dataJson.get('build_id'),
            'old_id': dataJson.get('old_id'),
            'new_id': dataJson.get('new_id')
        }
        change_build_component(
            build_id=data['build_id'], 
            old_id=data['old_id'],
            new_id=data['new_id']
        )
        return '', 204
    
    @app.route('/get/component_id', methods=['POST'])
    def get_component_id_view():
        dataJson = request.json
        data = {
            'build_id': dataJson.get('build_id'),
            'ct': dataJson.get('ct')
        }
        component_id = get_component_id(
            build_id=data['build_id'], 
            ct=data['ct']
        )
        return jsonify({"component_id": component_id})

    
    
    
    
    
    