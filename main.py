from flask import Flask, render_template, request, redirect, session
# import psycopg2
import bcrypt
from database.psql import get_psqsl_db_connection

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

        conn = get_psqsl_db_connection()
        cur = conn.cursor()

        # Запрос только хешированного пароля
        cur.execute("SELECT id, password_hash FROM users WHERE email = %s LIMIT 1", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            user_id, stored_hash = user

            # Проверяем введённый пароль с хешем из БД
            if bcrypt.checkpw(password.encode(), stored_hash.encode()):
                session['user'] = user_id
                return redirect('/dashboard')

        return render_template('login.html', error='Неверные учетные данные')

    return render_template('login.html', error=None)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    conn = get_psqsl_db_connection()
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
