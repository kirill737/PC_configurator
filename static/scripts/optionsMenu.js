// document.getElementById("open-component-settings-button").addEventListener("click", async () => {
//     // console.log("Нажали кнопку")
//     const menu = document.getElementById("components-settings-container");
//     menu.classList.toggle("hidden");
//     const create_build_button = document.getElementById("create-build-button");
//     // create_build_button.classList.toggle("hidden");

//     const response = await fetch("/create/component/<ct>");
//     const component_fields = await response.json();
//     console.log(component_fields)
//     const list = document.getElementById("fields-list");
//     list.innerHTML = "";
//     create_build_button.dispay ="block";
//     builds.forEach(build => {
//         const li = document.createElement("li");
//         li.textContent = build.name + build.id;
//         li.addEventListener("click", () => loadBuildComponents(build.id));
//         list.appendChild(li);
//     });
// });

// Открытие меню выбора сборки
document.getElementById("select-build-button").addEventListener("click", async () => {

    // Передача id выбранной сборки в python (далее в redis)
    async function selectBuild(buildId) {
        console.log("Выбралась сборка c id: " + buildId);
        await fetch(`/select/build/${buildId}`);
        loadBuildComponents();
    }

    const menu = document.getElementById("builds-menu");
    menu.classList.toggle("hidden");
    const create_build_button = document.getElementById("create-build-button");

    const response = await fetch("/all/builds");
    const builds = await response.json();

    const list = document.getElementById("builds-list");
    list.innerHTML = "";
    create_build_button.dispay ="block";
    builds.forEach(build => {
        const li = document.createElement("li");
        li.textContent = build.name + ": " + build.id;
        li.addEventListener("click", () => selectBuild(build.id));
        list.appendChild(li);
    });
});

// Кнопка добавления новой детали
document.getElementById("create-component-button").addEventListener("click", async () => {
    const create_component_button = document.getElementById("create-component-button");
    // create_build_button.classList.toggle("hidden");
    const ct = "cpu";

    const response = await fetch("/create/component", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ct })
    });
    // const response = a.0wait fetch("/create/component/${cpu}");
    const component_fields = await response.json();
    // console.log(component_fields);
    const field_list = document.getElementById("fields-list");
    field_list.innerHTML = "";
    component_fields.forEach(field => {
        const row = document.createElement("tr");
        const name_td = document.createElement("td");
        name_td.textContent = field + ":";
        name_td.classList.add("component-field-name");
        name_td.id = field;
        const input_td = document.createElement("td")
        const input = document.createElement("input");
        input.type ="text";
        input.placeholder = field;
        input.classList.add("input-component-field");
        input_td.appendChild(input)
        
        row.appendChild(name_td)
        row.appendChild(input);

        field_list.appendChild(row);
    });
});

// Скрытие меню выбора сборки при нажатии вне него
document.addEventListener("click", function(event) {
    let menu = document.getElementById("builds-menu");
    let select_build_button = document.getElementById("select-build-button");
    if (!menu.contains(event.target) && !select_build_button.contains(event.target)) {
        menu.classList.add("hidden");
    }
});

// Кнопка удаление сборки
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