from flask import Flask, render_template, request, redirect, session, jsonify
from database.psql import get_psql_db_connection

from controllers.session_controller import delete_session_by_user_id
from controllers.db.user_controller import *
from controllers.db.build_controller import get_user_builds
from views.component_settings_view import init_component_settings_menu

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
    
    @app.route("/api/builds/<int:build_id>/components")
    def get_build_components(build_id):
        logger.info(f"Попытка получить данные сборки {build_id}")
        
        conn = get_psql_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT component_id FROM build_components WHERE build_id = %s", (build_id,))
        
        component_ids = cur.fetchall() 
        
        logger.info(f"Check: {component_ids}")
        components = [{"id": row[0], "type": row[1]} for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(components)
    
    @app.route("/api/components/<int:component_id>")
    def get_component_data(component_id):
        conn = get_psql_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM components WHERE id = %s", (component_id,))
        data = cur.fetchone()
        cur.close()
        conn.close()
        
        if not data:
            return jsonify({"error": "Component not found"}), 404

        return jsonify(dict(zip(["id", "type", "name", "brand"], data)))
    
    @app.route("/api/builds/<int:build_id>", methods=["DELETE"])
    def delete_build(build_id): 
        conn = get_psql_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM builds WHERE id = %s", (build_id,))
            conn.commit()
            return jsonify({"status": "success"})
        except Exception as e:
            conn.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            cur.close()
            conn.close()
    
    


