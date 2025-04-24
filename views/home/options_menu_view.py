from flask import redirect, session, jsonify

from controllers.db.user_controller import *
from controllers.db.build_controller import get_user_builds, get_build_info
from controllers.db.component_controller import *
from controllers.session_controller import get_user_data
from views.home.main_menu_view import init_component_settings_menu

from logger_settings import setup_logger

logger = setup_logger("options_menu")

def init_options_menu(app):
    init_component_settings_menu(app)

    @app.route('/open_builds')
    def open_builds():
        return redirect('/home')
    
    # Боковое меню
    # Открытие всех достыпных сборок
    @app.route("/all/builds")
    def get_builds():
        logger.info("Нажали на кнопку выбора сборки")
        builds = get_user_builds(session['user_id'])
        return jsonify(builds)
    
    # @app.route("/select/build/<int:build_id>")
    # def select_build(build_id):
    #     session['build_id'] = build_id
    #     logger.info(f"Сборка {build_id} выбрана")
    #     return '', 204
    
    # Выдаёт список всех комплектующих
    @app.route("/all/build/components")
    def get_build_components() -> dict:
        build_id = session['build_id']
        logger.info(f"Попытка получить данные сборки {build_id}...")
        
        components = get_build_info(build_id)
        logger.info(f"Даннные получены: {components}")

        return jsonify(components)
    
    @app.route("/all/new_build/components")
    def get_all_new_build_components() -> dict:
        ct_list = get_all_component_types()
        return jsonify(ct_list)


    @app.route("/all/component/types")
    def get_all_component_types_view() -> dict:
        logger.info(f"Получаем все виды деталей...")
        
        all_types = get_all_component_types()
        logger.info(f"Все типы получены")

        return jsonify(all_types)
    
    @app.route("/create/new/build")
    def create_new_build_view():
        logger.info(f"Создание новой сборки")

        return jsonify({"build_id": 100})
    
    
    


