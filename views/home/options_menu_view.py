from flask import Flask, render_template, request, redirect, session, jsonify
from database.psql import get_psql_db_connection

from controllers.session_controller import delete_session_by_user_id
from controllers.db.user_controller import *
from controllers.db.build_controller import get_user_builds, get_build_info
from controllers.db.component_controller import *
from views.home.main_menu import init_component_settings_menu

from logger_settings import setup_logger

logger = setup_logger("options_menu")

def init_options_menu(app):
    init_component_settings_menu(app)
    @app.route('/open_builds')
    def open_builds():
        return redirect('/home')

    @app.route('/open_wishlists')
    def open_wishlists():
        return redirect('/home')
    
    # Боковое меню
    # Открытие всех достыпных сборок
    @app.route("/all/builds")
    def get_builds():
        logger.info("Нажали на кнопку выбора сборки")
        builds = get_user_builds(session['user_id'])
        return jsonify(builds)
    
    @app.route("/select/build/<int:build_id>")
    def select_build(build_id):
        session['build_id'] = build_id
        logger.info(f"Сборка {build_id} выбрана")
        return '', 204
    
    # Выдаёт список всех клмпдектующих
    @app.route("/all/builds/components")
    def get_build_components() -> dict:
        build_id = session['build_id']
        logger.info(f"Попытка получить данные сборки {build_id}...")
        
        components = get_build_info(build_id)
        logger.info(f"Даннные получены: {components}")

        return jsonify(components)
    
    @app.route("/all/component/types")
    def get_all_component_types_view() -> dict:
        logger.info(f"Получаем все виды деталей...")
        
        all_types = get_all_component_types()
        logger.info(f"Все типы получены")

        return jsonify(all_types)
    
    

    
    # @app.route("/api/components/<int:component_id>")
    # def get_component_data(component_id):
    #     conn = get_psql_db_connection()
    #     cur = conn.cursor()
    #     cur.execute("SELECT * FROM components WHERE id = %s", (component_id,))
    #     data = cur.fetchone()
    #     cur.close()
    #     conn.close()
        
    #     if not data:
    #         return jsonify({"error": "Component not found"}), 404

    #     return jsonify(dict(zip(["id", "type", "name", "brand"], data)))
    
    # @app.route("/api/builds/<int:build_id>", methods=["DELETE"])
    # def delete_build(build_id): 
    #     conn = get_psql_db_connection()
    #     cur = conn.cursor()
    #     try:
    #         cur.execute("DELETE FROM builds WHERE id = %s", (build_id,))
    #         conn.commit()
    #         return jsonify({"status": "success"})
    #     except Exception as e:
    #         conn.rollback()
    #         return jsonify({"error": str(e)}), 500
    #     finally:
    #         cur.close()
    #         conn.close()
    
    


