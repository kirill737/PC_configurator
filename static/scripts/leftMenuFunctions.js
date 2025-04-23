import { getCurrentBuildId, setCurrentCT} from "./help.js";
import { showSelectComponentsMenu } from "./selectComponentMenu.js";
import { updateBuildComponent, translate } from "./help.js";
import { updateField } from "./leftMenu.js";


// Загрузка краткой информации о сборке
export async function loadBuildInfo() {
    let response = await fetch(`/all/component/types`); // NOW
    const all_types = await response.json();
    
    response = await fetch(`/all/build/components`);
    let current_components = await response.json();
    console.log(current_components);
    
    const main_menu = document.getElementById("main-menu-container");
    main_menu.innerHTML = "";

    const components_drop_menu = document.createElement("table");
    components_drop_menu.id = "components-drop-menu";
    
    for (let current_component of current_components) {
        // let response = await fetch(`/get/component/data/${current_component.id}`);
        // let data = await response.json();
        
        const row = document.createElement("tr");
        row.classList.add("drop-container");

        const name_td = document.createElement("td"); 
        name_td.textContent = current_component.rus_type;
        row.appendChild(name_td);

        // Кнопка выпадающего меню
        const component_drop_td = document.createElement("td");

        const drop_btn = document.createElement("button"); // Кнопка
        // drop_btn.textContent = data["name"]; // HERE Тут имя детали
        drop_btn.textContent = current_component.name;
        drop_btn.classList.add("drop-btn");
        component_drop_td.appendChild(drop_btn);

        const drop_menu = document.createElement("div"); // Список
        drop_menu.classList.add("drop-content", "hidden");
        component_drop_td.appendChild(drop_menu);

        // При нажатии на кнопку закрываются все другие меню и открывается текущее
        drop_btn.addEventListener("click", async function () {
            drop_menu.innerHTML = "";
            // Заполняем список доступных деталей
            response = await fetch(`/get/all/components/type/${current_component.type}`);
            const components_list_data = await response.json();

            components_list_data.forEach(async component => {
                const a = document.createElement("a");
                a.href = "#";
                a.textContent = component.name;
                a.addEventListener("click", async function () {
                    let current_data = await getCurrentBuildId();

                    updateBuildComponent(current_data['build_id'], current_component.id, component.id);
                    current_component.id = component.id
                    drop_btn.textContent = component.name;
                    drop_menu.classList.add("hidden"); // Закрываем меню после выбора
                });
                drop_menu.appendChild(a);
            });
            document.querySelectorAll(".drop-content").forEach(menu => {
                if (menu !== drop_menu) {
                    menu.classList.add("hidden");
                }
            });
            drop_menu.classList.toggle("hidden");
        });

        

        row.appendChild(component_drop_td);
        components_drop_menu.appendChild(row);
    }
    
    main_menu.appendChild(components_drop_menu);
    
    document.addEventListener("click", function(event) {
        let drop_menu = document.getElementById("components-drop-menu");
        
        if (!drop_menu.contains(event.target)) {
            document.querySelectorAll(".drop-content").forEach(menu => {
                if (menu !== drop_menu) {
                    menu.classList.add("hidden");
                }
            });
        }
    })
}



// Открыть меню настройки детали
export async function loadComponentFields(ct, build_id) {
    await setCurrentCT(ct);
    console.log("build_id: " + build_id)
    console.log("ct: " + ct)
    let response = await fetch("/get/component_id", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            'build_id': build_id,
            'ct': ct
        })
    });
    let data = await response.json();
    let component_id = data['component_id'];
    console.log("component_id: " + component_id)
    response = await fetch(`/get/${component_id}/fields`);
    data = await response.json();

    const container = document.getElementById("main-menu-container");
    container.innerHTML = "";

    const components_drop_menu = document.createElement("div");
    components_drop_menu.id = 'components-drop-menu';
    components_drop_menu.classList.add("hidden");

    const components_list = document.createElement("ul");
    components_list.id = 'components-list';
    components_drop_menu.appendChild(components_list);
    container.appendChild(components_drop_menu);

    const field_list = document.createElement("table");
    field_list.id = 'fields-list';
    container.appendChild(field_list);

    updateField(data);

    const select_component_button = document.createElement("button");
    select_component_button.id = 'select-component-button';
    select_component_button.classList.add("base-button");
    select_component_button.textContent = 'Выбрать деталь';

    select_component_button.addEventListener("click", function () {
        showSelectComponentsMenu(component_id);
    });
    container.appendChild(select_component_button);
}