from flask import Flask, render_template, request, redirect, session

from database.psql import get_psql_db_connection
from controllers.db.user_controller import check_user_data, get_user_id

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(f"Попытка входа: {email}")

        login_code = check_user_data(email, password)

        if login_code == 1: # Введён верный пароль
            print("Ввели верный пароль")
            user_id = get_user_id(email)
            session['user'] = user_id
            return redirect('/dashboard')
        elif login_code == -1:
            return render_template('login.html', error='Пользователь не найден')
        else:
            return render_template('login.html', error='Неверный пароль')

    return render_template('login.html', error=None)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    conn = get_psql_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM components")
    components = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('dashboard.html', components=components)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
