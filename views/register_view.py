from flask import (
    render_template, 
    request, 
    redirect, 
)

from controllers.db.user_controller import (
    DifferentPasswords,
    EmailTaken,
    reg_user,
)
from logger_settings import setup_logger


# Настрофка логов
logger = setup_logger("register")
logger.info("Загрузка страница регистрации")


def init_register(app):

    @app.route("/open_register_page")
    def open_register_page():
        return redirect("/register")


    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form.get("username")
            email = request.form.get("email")
            password_1 = request.form.get("password_1")
            password_2 = request.form.get("password_2")

            try:
                reg_user(
                    username=username, 
                    email=email, 
                    password_1=password_1, 
                    password_2=password_2,
                )
                return redirect("/login")
            except (DifferentPasswords, EmailTaken) as e:
                return render_template("registration.html", error=e)

        return render_template("registration.html", error=None)
