import json

from flask import (
    render_template, 
    request, 
    redirect, 
    session, 
    jsonify, 
    url_for,
)

from controllers.session_controller import (
    delete_session_by_user_id, 
    get_session_data,
)
from controllers.db.component_controller import translate
from views.home.options_menu_view import init_options_menu
from views.home.edit_component_view import init_edit_component_menu
from views.home.help_view import init_help
from views.post_view import init_post
from logger_settings import setup_logger


# Настрофка логов
logger = setup_logger("home")
logger.info("Запуск главное страницы")

def init_home(app):
    init_help(app)
    init_options_menu(app)
    init_edit_component_menu(app)
    init_post(app)

    @app.route("/home")
    def home():
        user_data = get_session_data(session["session_id"])

        logger.debug(f"user_data: {str(user_data)}")

        # Проверка роли пользователя
        if user_data["role"] != "guest":
            return render_template("home.html", user_data=user_data)
        else:
            return redirect(url_for("posts_view", user_data=user_data))
    
    
    @app.route("/logout")
    def logout():
        delete_session_by_user_id(session["session_id"])
        return redirect("/login")

    
    @app.route("/translate", methods=["POST"])
    def translate_view():
        data = request.json
        result = translate(data.get("name"), data.get("capitalize"))
        return jsonify({"result": result})
