// Добавление меню выбора сборки
document.getElementById("select-build-button").addEventListener("click", async () => {
    console.log("Нажали кнопку")
    const menu = document.getElementById("builds-menu");
    menu.classList.toggle("hidden");

    const response = await fetch("/api/builds");
    const builds = await response.json();

    const list = document.getElementById("builds-list");
    list.innerHTML = "";
    builds.forEach(build => {
        const li = document.createElement("li");
        li.textContent = build.name;
        li.addEventListener("click", () => loadBuildComponents(build.id));
        list.appendChild(li);
    });
});



// Загрузка комплектующих в сборке
async function loadBuildComponents(buildId) {
    const response = await fetch(`/api/builds/${buildId}/components`);
    const components = await response.json();

    const container = document.getElementById("components-container");
    container.innerHTML = "";

    components.forEach(component => {
        const btn = document.createElement("a");
        btn.className = "side-menu-button";
        btn.textContent = component.type;
        btn.href = "#";
        btn.addEventListener("click", () => loadComponentSettings(component.id, component.type));
        container.appendChild(btn);
    });
}

// Отображение полей для редактирования
async function loadComponentSettings(componentId, type) {
    const response = await fetch(`/api/components/${componentId}`);
    const data = await response.json();

    const container = document.getElementById("components-settings-container");
    container.innerHTML = `<h3>${type}</h3>`;

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
document.querySelectorAll(".side-menu-button").forEach(btn => {
    btn.addEventListener("click", function() {
        document.querySelectorAll(".side-menu-button").forEach(b => b.classList.remove("active"));
        this.classList.add("active");
    });
});

// Удаление сборки
document.getElementById("delete-build-btn").addEventListener("click", async () => {
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


