
async function loadBuildInfo(build_id) {
    const container = document.getElementById("components-container");
    container.innerHTML = "";

    const response = await fetch(`/build/info/${build_id}`);
    const components = await response.json();
    
}

// Загрузка комплектующих в сборке
async function loadBuildComponents() {
    console.log("Загрузка деталей в сборке");
    const response = await fetch(`/all/builds/components`);
    const components = await response.json();

    let data = getCurrentComponentData();
    build_id = data['build_id'];

    const container = document.getElementById("components-container");
    container.innerHTML = "";

    const build_name_label = document.createElement("label");
    build_name_label.textContent = "Тест";
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

        // Назначаем обработчик сразу!
        component_btn.addEventListener("click", function () {
            console.log("\t\tКНОПКА АКТИВНА");
            document.querySelectorAll(".component-button").forEach(b => b.classList.remove("active"));
            this.classList.add("active");
        });

        container.appendChild(component_btn);
        console.log("Добавлена кнопка: " + component.type);
    });

    let menu = document.getElementById("builds-menu");
    menu.classList.add("hidden");
}


// Заполняет поля в информации о комплектующей
function updateField(data) {
    const field_list = document.getElementById("fields-list");
    field_list.innerHTML = "";
    data.forEach(field => {
        const row = document.createElement("tr");

        const name_td = document.createElement("td");
        name_td.textContent = field.name + ":";
        name_td.classList.add("component-field-name");
        name_td.id = field.value;

        const input = document.createElement("input");
        input.type ="text";
        input.placeholder = field.name;
        input.value = field.value;
        input.setAttribute("data-key", field.name);
        input.classList.add("input-component-field");

        const input_td = document.createElement("td")
        input_td.appendChild(input)
        
        row.appendChild(name_td)
        row.appendChild(input);
        
        field_list.appendChild(row);
    });
}

// Открыть меню настройки детали
async function loadComponentFields(component) {
    console.log("Setup CT <<<>>>");
    await setCurrentComponentDataCT(component.type);

    

    let response = await fetch(`/get/${component.id}/fields`);
    const data = await response.json();

    const container = document.getElementById("main-menu-container");
    container.innerHTML = "";

    const components_menu = document.createElement("div");
    components_menu.id = 'components-menu';
    components_menu.classList.add("hidden");

    const components_list = document.createElement("ul");
    components_list.id = 'components-list';
    components_menu.appendChild(components_list);
    container.appendChild(components_menu);

    const field_list = document.createElement("table");
    field_list.id = 'fields-list';
    container.appendChild(field_list);

    updateField(data);

    const select_component_button = document.createElement("button");
    select_component_button.id = 'select-component-button';
    select_component_button.classList.add("base-button");
    select_component_button.textContent = 'Выбрать деталь';
    select_component_button.onclick = showSelectComponentsMenu;
    container.appendChild(select_component_button);

    // const saveBtn = document.createElement("button");
    // saveBtn.textContent = "Сохранить";
    // saveBtn.classList.add("base-button")
    // saveBtn.classList.add("main-menu-button");
    // saveBtn.addEventListener("click", () => saveComponentData(component.id));
    // container.appendChild(saveBtn); 
}

// // Выделение активной комплектующей
// document.querySelectorAll(".component-button").forEach(btn => {
//     console.log("\t\tКНОПКА АКТИВНА");
//     btn.addEventListener("click", function() {
//         document.querySelectorAll(".component-button").forEach(b => b.classList.remove("active"));
//         this.classList.add("active");
//     });
// });

