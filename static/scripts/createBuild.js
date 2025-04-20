import { translate } from "./help.js";

async function loadNewComponentFields(component) {
    await setCurrentCT(component.type);

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

async function loadNewBuildInfo() {
    let response = await fetch(`/all/builds/components`);
    const current_components = await response.json();
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
        name_td.textContent = translate(current_component.type);
        row.appendChild(name_td);

        // Кнопка выпадающего меню
        const component_drop_td = document.createElement("td");

        const drop_btn = document.createElement("button"); // Кнопка
        drop_btn.textContent = translate(current_component.name); // Тут имя детали
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
                current_component
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

export async function loadNewBuildComponents(buildName) {
    let response = await fetch(`/all/new_build/components`); // Добавить  запрос на создание сборки
    const components_name = await response.json();


    const container = document.getElementById("main-menu-container");
    container.innerHTML = "";

    const build_name_label = document.createElement("input");
    build_name_label.textContent = "";
    build_name_label.placeholder = "Введине название";
    build_name_label.id = "build-name-input";
    build_name_label.type = "text";
    
    container.appendChild(build_name_label); 

    

    let future_build_components = {};
    const components_drop_menu = document.createElement("table");
        components_drop_menu.id = "components-drop-menu";
        
        for (let current_component of components_name) {
            // let response = await fetch(`/get/component/data/${current_component.id}`);
            // let data = await response.json();
            
            const row = document.createElement("tr");
            row.classList.add("drop-container");
    
            const name_td = document.createElement("td"); 
            name_td.textContent = current_component.ct_rus;
            row.appendChild(name_td);
    
            // Кнопка выпадающего меню
            const component_drop_td = document.createElement("td");
    
            const drop_btn = document.createElement("button"); // Кнопка
            // drop_btn.textContent = data["name"]; // HERE Тут имя детали
            // drop_btn.textContent = current_component.name;
            drop_btn.textContent = "Выбрать";
            drop_btn.classList.add("drop-btn");
            component_drop_td.appendChild(drop_btn);
    
            const drop_menu = document.createElement("div"); // Список
            drop_menu.classList.add("drop-content", "hidden");
            component_drop_td.appendChild(drop_menu);
    
            // При нажатии на кнопку закрываются все другие меню и открывается текущее
            drop_btn.addEventListener("click", async function () {
                drop_menu.innerHTML = "";
                // Заполняем список доступных деталей
                response = await fetch(`/get/all/components/type/${current_component.ct}`);
                const components_list_data = await response.json();
    
                components_list_data.forEach(async component => {
                    const a = document.createElement("a");
                    a.href = "#";
                    a.textContent = component.name;
                    a.addEventListener("click", async function () {
                        // let current_data = await getCurrentBuildId();
                        future_build_components[current_component.ct] = component.id;
                        // updateBuildComponent(current_data['build_id'], current_component.id, component.id);
                        // current_component.id = component.id
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

    container.appendChild(components_drop_menu);

    // Кнопка создания сборки с заполнеными данными
    const saveBtn = document.createElement("button");
    saveBtn.textContent = "Создать сборку";
    saveBtn.classList.add("base-button")
    saveBtn.classList.add("main-menu-button");
    saveBtn.addEventListener("click", async () => {
        const buildName = build_name_label.value.trim();
        if (!buildName) {
            alert("Введите имя сборки");
            return;
        }
    
        
        const response = await fetch(`/create/build/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "build_info": future_build_components,
                "build_name": buildName
            })
        });

        const result = await response.json();

        if (result.status == "success") {
            alert("Сборка успешно создана");
        } else {
            alert(result.message);
        }
    });
    
    container.appendChild(saveBtn); 
    
}

// document.getElementById("create-build-button").addEventListener("click", async () => {

//     await loadNewBuildComponents("");

// })





