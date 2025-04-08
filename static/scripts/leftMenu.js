import { getCurrentData, setCurrentComponentDataCT} from "./help.js";
import { showSelectComponentsMenu } from "./selectComponentMenu.js";
import { updateBuildComponent, translate } from "./help.js";
// Краткая информацию о сборке
async function loadBuildInfo() {
    let response = await fetch(`/all/builds/components`);
    const current_components = await response.json();
    console.log(current_components);
    
    const main_menu = document.getElementById("main-menu-container");
    main_menu.innerHTML = "";

    const components_drop_menu = document.createElement("table");
    components_drop_menu.id = "components-drop-menu";
    
    for (const current_component of current_components) {
        let response = await fetch(`/get/component/data/${current_component.id}`);
        let data = await response.json();
        
        const row = document.createElement("tr");
        row.classList.add("drop-container");

        const name_td = document.createElement("td"); 
        name_td.textContent = translate(current_component.type);
        row.appendChild(name_td);

        // Кнопка выпадающего меню
        const component_drop_td = document.createElement("td");

        const drop_btn = document.createElement("button"); // Кнопка
        drop_btn.textContent = translate(data["name"]); // Тут имя детали
        drop_btn.classList.add("drop-btn");
        component_drop_td.appendChild(drop_btn);

        const drop_menu = document.createElement("div"); // Список
        drop_menu.classList.add("drop-content", "hidden");
        component_drop_td.appendChild(drop_menu);

        // При нажатии на кнопку закрываются все другие меню и открывается текущее
        drop_btn.addEventListener("click", function () {
            document.querySelectorAll(".drop-content").forEach(menu => {
                if (menu !== drop_menu) {
                    menu.classList.add("hidden");
                }
            });
            drop_menu.classList.toggle("hidden");
        });

        // Заполняем список доступных деталей
        response = await fetch(`/get/all/components/type/${current_component.type}`);
        const components_list_data = await response.json();

        components_list_data.forEach(async component => {
            const a = document.createElement("a");
            a.href = "#";
            a.textContent = await translate(component.name);
            a.addEventListener("click", async function () {
                let current_data = await getCurrentData();

                updateBuildComponent(current_data['build_id'], current_component.id, component.id);
                drop_btn.textContent = await translate(component.name);
                drop_menu.classList.add("hidden"); // Закрываем меню после выбора
            });
            drop_menu.appendChild(a);
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

// Загрузка видов всех комплектующих в левое меню
export async function loadBuildComponents(buildName) {
    const response = await fetch(`/all/builds/components`);
    const components = await response.json();

    let data = getCurrentData();
    let build_id = data['build_id'];

    const container = document.getElementById("left-menu-container");
    container.innerHTML = "";

    const build_name_label = document.createElement("label");
    build_name_label.textContent = buildName;
    build_name_label.id = "build-name-label";
    build_name_label.type = "text";
    build_name_label.addEventListener("click", () => loadBuildInfo(build_id));
    container.appendChild(build_name_label);

    components.forEach(component => {
        const component_btn = document.createElement("a");
        component_btn.className = "component-button";
        component_btn.textContent = component.rus_type;
        component_btn.href = "#";
        component_btn.addEventListener("click", () => loadComponentFields(component));

        component_btn.addEventListener("click", function () {
            document.querySelectorAll(".component-button").forEach(b => b.classList.remove("active"));
            this.classList.add("active");
        });

        container.appendChild(component_btn);
    });

    let menu = document.getElementById("builds-menu");
    menu.classList.add("hidden");
}

// Заполняет поля в информации о комплектующей
export function updateField(data) {
    const field_list = document.getElementById("fields-list");
    field_list.innerHTML = "";
    data.forEach(async field => {
        const row = document.createElement("tr");

        const name_td = document.createElement("td");
        name_td.textContent = await translate(field.name);
        name_td.classList.add("component-field-name");
        name_td.id = field.name;

        const input = document.createElement("input");
        input.type ="text";
        input.placeholder = await translate(field.name);
        input.value = field.value;
        input.setAttribute("data-key", field.name);
        input.classList.add("input-component-field");

        const input_td = document.createElement("td")
        input_td.appendChild(input)
        
        row.appendChild(name_td)
        row.appendChild(input_td);
        
        field_list.appendChild(row);
    });
}

// Открыть меню настройки детали
async function loadComponentFields(component) {
    await setCurrentComponentDataCT(component.type);

    let response = await fetch(`/get/${component.id}/fields`);
    const data = await response.json();

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

    const ct = component.type;
    select_component_button.addEventListener("click", function () {
        showSelectComponentsMenu(ct);
    });
    container.appendChild(select_component_button);

    // const saveBtn = document.createElement("button");
    // saveBtn.textContent = "Сохранить";
    // saveBtn.classList.add("base-button")
    // saveBtn.classList.add("main-menu-button");
    // saveBtn.addEventListener("click", () => saveComponentData(component.id));
    // container.appendChild(saveBtn); 
}