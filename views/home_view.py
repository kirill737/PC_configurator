from flask import render_template, request, redirect, session, jsonify, url_for

from controllers.session_controller import delete_session_by_user_id, get_session_data
from controllers.db.user_controller import *
import json
from urllib.parse import unquote
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

    @app.route('/home')
    def home():
        # Получаем строку user_data из query string, где кавычки правильные
        raw_user_data = request.args.get('user_data', '{"role":"guest","user_id":null}')
        logger.debug(f"raw_user_data: {raw_user_data}")
        
        # Декодируем URL
        user_data = unquote(raw_user_data)
        logger.debug(f"user_data: {str(user_data)}")
        logger.debug(f"user_data type: {type(user_data)}")
        logger.debug('{"role": "guest", "user_id": null}')
        # Если user_data строка, то пытаемся распарсить её в JSON
        if isinstance(user_data, str):
            try:
                user_data = json.loads(user_data)
            except:
                user_data = user_data.replace("'", '"')
                user_data = json.loads(user_data)
    
        # Проверка роли пользователя
        if user_data['role'] != 'guest':
            user_id = user_data['user_id']
            if not user_id:
                return redirect('/login')
            logger.debug(request.args.get("session_id"))
            
            return render_template('home.html', user_data=get_user_data(user_id))
        else:
            return redirect(url_for('posts_view', user_data=json.dumps({"role": "guest", "user_id": None})))
    
    
    @app.route('/logout')
    def logout():
        raw_user_data = request.args.get('user_data', '{"role": "guest", "user_id": null}')
        user_data = {}
        logger.debug(type(raw_user_data))
        if type(raw_user_data) != dict:
            user_data = json.loads(raw_user_data)
        else:
            user_data = json.loads(unquote(raw_user_data))
        user_id = user_data['user_id']
        if user_id:
            delete_session_by_user_id(user_id)

        return redirect('/login')

    
    @app.route('/translate', methods=['POST'])
    def translate_view():
        data = request.json
        result = translate(data.get('name'), data.get('capitalize'))
        return jsonify({"result": result})   
