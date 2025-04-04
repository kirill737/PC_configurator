from controllers.db.user_controller import add_user, get_user_id
from controllers.session_controller import create_session, get_session_data, delete_session
from controllers.db.component_controller import *
from controllers.db.build_controller import *
from test_components import components
# add_user('user1', 'kirill737apple@gmail.com', 'home9999', 'admin')

component_types = [
    ComponentType.cpu,
    ComponentType.motherboard,
    ComponentType.gpu,
    ComponentType.ram,
    ComponentType.case,
    ComponentType.headphones,
    ComponentType.keyboard,
    ComponentType.mouse,
    ComponentType.microphone,
    ComponentType.monitor,
    ComponentType.storage,
    ComponentType.power_supply
]

# add_component(ComponentType.cpu, 15000, build_info[ComponentType.cpu])
def create_users():
    emails = [
        'test1@yandex.ru',
        'test2@gmail.com',
        'test3@test.com'
        ]

    add_user('name1',  emails[0], 'root')
    add_user('name2',  emails[1], 'root')
    add_user('name3',  emails[2], 'root')

def create_components(components):
    for i in range(3):
        for ct, component_list in components.items():
            add_component(ct, 1000, component_list[i])

def fill_builds():
    for i in range(3):
        build = {}
        num = 0
        for t in component_types:
            num += 1
            build[t] = num
        print(build)
# print(ComponentType('cpu'))
# get_all_component_by_type(ComponentType('cpu'))
print(get_component_data(1))
# print(get_build_info(4))
# parameters = get_components_fields(1)
# print(parameters)
# create_components(components)
# create_users()


