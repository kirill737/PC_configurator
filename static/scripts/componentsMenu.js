// Загрузка комплектующих в сборке
async function loadBuildComponents() {
    console.log("Загрузка деталей в сборке");
    const response = await fetch(`/all/builds/components`);
    const components = await response.json();

    const container = document.getElementById("components-container");
    container.innerHTML = "";
    // console.log(components);
    components.forEach(component => {
        const component_btn = document.createElement("a");
        component_btn.className = "component-button";
        component_btn.textContent = component.type;
        component_btn.href = "#";
        component_btn.addEventListener("click", () => loadComponentFields(component.id, component.type));
        
        container.appendChild(component_btn);
        console.log("Добавлена кнопка: " + component.type);
        // console.log(`${key}: ${obj[key]}`);
    })
    let menu = document.getElementById("builds-menu");
    menu.classList.add("hidden");
}

// Отображение полей для редактирования
async function loadComponentFields(componentId, componentType, buildId) {
    let response = await fetch(`/open/${componentId}/fields`);
    const data = await response.json();

    const container = document.getElementById("components-settings-container");
    container.innerHTML = "<table id='fields-list'></table>";

    const field_list = document.getElementById("fields-list");
    field_list.innerHTML = "";

    Object.keys(data).forEach(field => {
        const row = document.createElement("tr");

        const name_td = document.createElement("td");
        name_td.textContent = field + ":";
        name_td.classList.add("component-field-name");
        name_td.id = field;

        const input = document.createElement("input");
        input.type ="text";
        input.placeholder = field;
        input.value = data[field];
        input.setAttribute("data-key", field);
        input.classList.add("input-component-field");

        const input_td = document.createElement("td")
        input_td.appendChild(input)
        
        row.appendChild(name_td)
        row.appendChild(input);
        
        field_list.appendChild(row);
    });

    const saveBtn = document.createElement("button");
    saveBtn.textContent = "Сохранить";
    saveBtn.classList.add("base-button")
    saveBtn.classList.add("main-menu-button");
    saveBtn.addEventListener("click", () => saveComponentData(componentId));
    container.appendChild(saveBtn);
}

// Выделение активной комплектующей
document.querySelectorAll(".component-button").forEach(btn => {
    btn.addEventListener("click", function() {
        document.querySelectorAll(".component-button").forEach(b => b.classList.remove("active"));
        this.classList.add("active");
    });
});




