from controllers.db.user_controller import add_user, get_user_id
from controllers.session_controller import create_session, get_session_data, delete_session
from controllers.db.component_controller import *
from controllers.db.build_controller import *
from test_components import components
import json
from controllers.db.build_component_controller import *
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
        'test2@yandex.ru',
        'test3@yandex.ru'
        ]

    add_user('name1',  emails[0], 'root')
    add_user('name2',  emails[1], 'root')
    add_user('name3',  emails[2], 'root')

def create_components(components):
    for i in range(3):
        for ct, component_list in components.items():
            add_component(ct, 1000, component_list[i])

def create_builds():
    build_names = ['Мой сетап', 'Тарахтелка Коляна', 'Ноут']
    for i in range(3):
        build = {}
        num = 0
        for ct in component_types:
            num += 1
            build[ct] = num
        # print(build
        create_build(i + 1, build_names[i], build)

with open("builds.json", "w", encoding="utf-8") as f:
    builds = []
    for build_id in range(1, 4):
        build_info = get_build_info(build_id)
        builds.append(build_info)
    json.dump(builds, f, ensure_ascii=False, indent=4)
# create_users()
# create_components()
# create_builds()


