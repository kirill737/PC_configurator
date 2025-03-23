from flask import Flask, render_template, request, redirect, session
from controllers.session_controller import create_session, delete_session, delete_session_by_user_id
from database.psql import get_psql_db_connection
from controllers.db.user_controller import *
# check_user_login_data, get_user_id, reg_user, DifferentPasswords, EmailTaken, get_user_data
import logging
from settings import init_settings
# Настрофка логов
logging.basicConfig(
    filename="logs/pc_config_main.log",  # Лог в файл
    level=logging.INFO,  # Логируем всё (DEBUG и выше)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат вывода
    datefmt="%H:%M:%S"
)

# Запуск сервеоа
app = Flask(__name__)
init_settings(app)
app.secret_key = 'supersecretkey'

@app.route('/')
def index():
    return redirect('/login')

@app.route('/open_login_page')
def open_login_page():
    return redirect('/login')

@app.route('/open_register_page')
def open_register_page():
    return redirect('/register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    logging.info("Страница входа")
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        login_code = check_user_login_data(email, password)

        if login_code == 1: # Введён верный пароль
            logging.info(f"Пользователь {email} ввёл верный пароль")
            user_id = get_user_id(email)
            
            session_id = create_session(user_id)
            logging.info(f"Сессия {session_id} - началась")
            session["user_id"] = get_user_id(email)
            
            return redirect('/dashboard')
        elif login_code == -1:
            logging.info(f"Пользователь с почтой {email} не найден")
            return render_template('login.html', error='Пользователь не найден')
        else:
            logging.info(f"Неверный пароль пользователя {email}")
            return render_template('login.html', error='Неверный пароль')

    return render_template('login.html', error=None)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password_1 = request.form.get('password_1')
        password_2 = request.form.get('password_2')

        try:
            reg_user(username=username, email=email, password_1=password_1, password_2=password_2)
            return redirect('/login')
        except DifferentPasswords as e:
            return render_template('registration.html', error=e)
        except EmailTaken as e:
            return render_template('registration.html', error=e)

    return render_template('registration.html', error=None)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    
    conn = get_psql_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM components;")
    components = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('dashboard.html', user_data=get_user_data(session['user_id']))

@app.route('/logout')
def logout():
    user_id = session.get("user_id")
    if user_id:
        delete_session_by_user_id(user_id)
        session.clear()
    # session.pop('user', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
