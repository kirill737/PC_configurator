from flask import Flask, render_template, request, redirect, session, jsonify
from database.psql import get_psql_db_connection

from controllers.session_controller import delete_session_by_user_id
from controllers.db.user_controller import *

from logger_settings import setup_logger

# Настрофка логов
logger = setup_logger("home")
logger.info("Запуск главное страницы")

def init_home(app):
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
        conn = get_psql_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM builds")
        builds = [{"id": row[0], "name": row[1]} for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(builds)
    
    @app.route("/api/builds/<int:build_id>/components")
    def get_build_components(build_id):
        conn = get_psql_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, type FROM components WHERE build_id = %s", (build_id,))
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



