from flask import render_template, request, redirect, session
from logger_settings import setup_logger

from controllers.db.component_controller import get_all_component_by_type, ComponentType, get_component_data

logger = setup_logger("help")
logger.info("Запуск главное страницы")

def init_help(app):
    @app.route('/set/current/data/build_id', methods=['POST'])
    def set_current_build_id_view():
        logger.debug("Запуск<set_current_component_build_id_view>")
        logger.info("Попытк установить текущий id сборки...")

        dataJson = request.json
        data = {
            'build_id': dataJson.get('build_id')
        }
        session['build_id'] = data['build_id']
        logger.info(f"Data changed to '{data}'")
        return data
    
    @app.route('/set/current/data/ct', methods=['POST'])
    def set_current_ct_view():
        logger.debug("Запуск <set_current_component_type_view>")
        logger.info("Попытка установить текущий тип данных...")
        dataJson = request.json
        ct = dataJson.get('ct')
        logger.debug(f"Тип получен из запроса: {ct}")
        data = {
            'ct': ct
        }
        session['ct'] = ct
        logger.info(f"Текущий тип изменён на '{data}'")
        return data
    
    @app.route('/get/current/data')
    def get_current_data():
        logger.info("Попытка получить данные")
        data = {
            'ct': session['ct'],
            'build_id': session['build_id']
        }
        return data
    
    @app.route('/get/current/data/ct')
    def get_current_ct():
        logger.info("Попытка получить текущий тип комплектующей")
        data = {
            'ct': session['ct']
        }
        return data
    
    @app.route('/get/current/data/build_id')
    def get_current_build_id():
        logger.info("Попытка получить текущий тип комплектующей")
        data = {
            'build_id': session['build_id']
        }
        return data

    @app.route('/get/component/data/<int:component_id>')
    def component_data_view(component_id: int):
        logger.debug("Запуск <component_data_view>")
        logger.info(f"Получения текущей информации о комплектующей: {component_id}")
        data_dict = get_component_data(component_id)
        
        return data_dict
    
    @app.route('/get/all/components/type/<ct>')
    def get_all_components(ct: ComponentType):
        logger.info(f"Получение всех деталей типа {ct}")
        components_list = get_all_component_by_type(ct)
        return components_list
    
    