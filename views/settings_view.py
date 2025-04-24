from flask import (
    render_template, 
    request, 
    session,
)

from controllers.db.user_controller import change_user_data_by_user_id
from controllers.session_controller import (
    get_session_data,
    create_session,
    delete_session,
)
from logger_settings import setup_logger


logger = setup_logger("settings")
logger.info("Загрузка страницы с данными пользователя")


def init_settings(app):

    @app.route("/open_settings_page")
    def open_settings_page():
        return render_template("settings.html", user_data=get_session_data(session["session_id"]))


    @app.route("/save_settings", methods=["GET", "POST"])
    def save_settings():
    
        if request.method == "POST":
            logger.info("Сохроняем данные...")

            new_user_data = {
                "username": request.form.get("username"),
                "email": request.form.get("email"),
                "password": request.form.get("password"),
            }
            
            session_id = session["session_id"]

            user_data = get_session_data(session_id)
            user_id = user_data["user_id"]
            try:
                logger.info(f"Меняем данные о пользователе {user_id} на:\n{new_user_data}")
                change_user_data_by_user_id(user_id, new_user_data)
                delete_session(session_id)
                session["session_id"] = create_session(user_id)
                logger.info(f"Данные успешно сохранены")
            except Exception as e:
                logger.error(f"Ошибка при смене данных {e}")
                return render_template("settings.html", user_data=user_data, error=e)

            # return render_template("login.html", error="Неверный пароль")

        return render_template("settings.html", user_data=get_session_data(session["session_id"]), error=None)
