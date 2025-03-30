// Добавление меню выбора сборки
document.getElementById("select-build-button").addEventListener("click", async () => {
    const menu = document.getElementById("builds-menu");
    menu.classList.toggle("hidden");
    const create_build_button = document.getElementById("create-build-button");

    const response = await fetch("/api/builds");
    const builds = await response.json();

    const list = document.getElementById("builds-list");
    list.innerHTML = "";
    create_build_button.dispay ="block";
    builds.forEach(build => {
        const li = document.createElement("li");
        li.textContent = build.name + build.id;
        li.addEventListener("click", () => loadBuildComponents(build.id));
        list.appendChild(li);
    });
});

// Скрытие меню при нажатии вне него
document.addEventListener("click", function(event) {
    let menu = document.getElementById("builds-menu");
    let select_build_button = document.getElementById("select-build-button");
    if (!menu.contains(event.target) && !select_build_button.contains(event.target)) {
        menu.classList.add("hidden");
    }
});

// Загрузка комплектующих в сборке
async function loadBuildComponents(buildId) {
    const response = await fetch(`/open/builds/${buildId}/components`);
    const components = await response.json();

    const container = document.getElementById("components-container");
    container.innerHTML = "";
 
    for (let ct in components) {
        const component_btn = document.createElement("a");
        component_btn.className = "component-button";
        component_btn.textContent = ct;
        component_btn.href = "#";
        component_btn.addEventListener("click", () => loadComponentFields(component.id, component.type, buildId));
        
        container.appendChild(component_btn);

        // console.log(`${key}: ${obj[key]}`);
    }    

}

// Отображение полей для редактирования
async function loadComponentFields(componentId, componentType, buildId) {
    const response = await fetch(`/open/${componentId}/fields`);
    const data = await response.json();

    const container = document.getElementById("components-settings-container");
    container.innerHTML = "";

    Object.keys(data).forEach(key => {
        const label = document.createElement("label");
        label.textContent = key;

        const input = document.createElement("input");
        input.value = data[key];
        input.setAttribute("data-key", key);

        container.appendChild(label);
        container.appendChild(input);
    });

    const saveBtn = document.createElement("button");
    saveBtn.textContent = "Сохранить";
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

// Удаление сборки
document.getElementById("delete-build-button").addEventListener("click", async () => {
    const buildId = currentBuildId;  // Сохраняем ID текущей сборки при выборе
    if (!buildId) return;

    const response = await fetch(`/api/builds/${buildId}`, { method: "DELETE" });

    if (response.ok) {
        alert("Сборка удалена!");
        location.reload();
    } else {
        alert("Ошибка при удалении!");
    }
});


