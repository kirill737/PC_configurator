from controllers.db.user_controller import add_user, get_user_id
from controllers.session_controller import create_session, get_session_data, delete_session
from controllers.db.component_controller import add_component, ComponentType as CT
from controllers.db.build_controller import add_build
from test_data import all_for_build as build_info
# add_user('user1', 'kirill737apple@gmail.com', 'home9999', 'admin')


# add_component(CT.cpu, 15000, build_info[CT.cpu])
def create_users():
    emails = [
        'kirill737apple@yandex.ru',
        'kirill737apple@gmail.com',
        'existed_email@test.com',
        'not_existed_email@test.com'
        ]
    passwords = [
        'correct_password', 
        'correct_password',
        'incorrect_password',
        'incorrect_password'
    ]
    add_user('name1',  emails[0], passwords[0])
    add_user('name2',  emails[1], passwords[1])
    add_user('name3',  emails[2], passwords[2])
    # # add_user('name4',  emails[3], passwords[3])
    # for i in range(4):
    #     try: 
    #         user_id = get_user_id(emails[i])
    #         # print(type(user_id))
    #     except Exception as e:
    #         print(f"Ошибка в get_user_id({emails[i]}, {passwords[i]}): {e}")

    # user_id = get_user_id(emails[0])
    # session_id = create_session(user_id)
    # print("Создана сессия:", session_id)

    # session_data = get_session_data(session_id)  
    # print("Данные сессии:", session_data)

# create_users()
add_build(1, "Тестовая сборочка", build_info)