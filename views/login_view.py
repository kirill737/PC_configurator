from flask import (
    render_template, 
    request, 
    redirect,
    session, 
    url_for,
)

from controllers.session_controller import (
    create_session,
    get_session_data,
)
from controllers.db.user_controller import (
    check_user_login_data,
    get_user_id,
)
from logger_settings import setup_logger


# Настройка логов
logger = setup_logger("login")
logger.info("Загрузка страница входа")


def init_login(app):

    @app.route("/open_login_page")
    def open_login_page():
        return redirect("/login")


    @app.route("/login", methods=["GET", "POST"])
    def login():
        logger.info("Страница входа")
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")
            login_code = check_user_login_data(email, password)

            if login_code == 1: # Введён верный пароль
                logger.info(f"Пользователь {email} ввёл верный пароль")
                
                session_id = create_session(user_id=get_user_id(email))
                session["session_id"] = session_id
                logger.info(f"Сессия {session_id} - началась")
                
                user_data = get_session_data(session_id)
                logger.debug(f"user_data: {user_data}")
                return redirect(url_for("home", user_data=user_data))
            
            elif login_code == -1:
                logger.info(f"Пользователь с почтой {email} не найден")
                return render_template("login.html", error="Пользователь не найден")
            
            else:
                logger.info(f"Неверный пароль пользователя {email}")
                return render_template("login.html", error="Неверный пароль")

        return render_template("login.html", error=None)
    

    @app.route("/guest_login")
    def guest_login():
        try:
            session_id = create_session()
            session["session_id"] = session_id
            logger.info(f"ГОСТЕВАЯ сессия {session_id} - началась")

            user_data = get_session_data(session_id)
            logger.debug(f"user_data: {user_data}")
            
            # После выполнения функции, можно сделать редирект
            return redirect("posts")  # Возвращаем успешный статус
        except Exception as e:
            return render_template("login.html", error=f"{e}")