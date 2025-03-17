from flask import Flask, render_template, request, redirect, session
import psycopg2

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Подключение к БД
DB_CONFIG = {
    'dbname': 'pc_configurator_db',
    'user': 'kirill',
    'password': 'root',
    'host': 'localhost',
    'port': '5432'
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(f"{email} {password}")
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if user:
            session['user'] = user[0]
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Неверные учетные данные')
    
    return render_template('login.html', error=None)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    
    conn = get_db_connection()
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
