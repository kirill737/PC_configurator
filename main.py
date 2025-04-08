from flask import Flask, render_template, request, redirect, session

from views.login_view import init_login
from views.register_view import init_register
from views.home_view import init_home
from views.settings_view import init_settings

from logger_settings import setup_logger

logger = setup_logger("main")
logger.info("Запуск сайта...")

# Запуск сервеоа
app = Flask(__name__)

# Загружаем все модули сайта 
init_login(app)
init_register(app)
init_home(app)
init_settings(app)

app.secret_key = 'supersecretkey'

@app.route('/')
def index():
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
