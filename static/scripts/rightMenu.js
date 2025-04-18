
import { loadAllComponentsMenu } from "./changeComponentMenu.js";
import { translate, setCurrentBuildId } from "./help.js";
import { updateFieldList, saveComponentButtonFunction, loadBuildComponents } from "./rightMenuFunctions.js";


// Кнопка выбора сборки
// Открывает меню выбора сборки
document.getElementById("select-build-button").addEventListener("click", async () => {

    // Передача id выбранной сборки в python (далее в redis)
    async function selectBuild(buildId, buildName) {
        await setCurrentBuildId(buildId);
        loadBuildComponents(buildName);
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
        li.textContent = build.name;
        li.addEventListener("click", () => selectBuild(build.id, build.name));
        list.appendChild(li);
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

// Кнопка создания сборки
document.getElementById("create-build-button").addEventListener("click", async () => {
    await setCurrentBuildId(buildId);
    loadBuildComponents(buildName);
});

// Кнопка добавления новой детали
document.getElementById("create-component-button").addEventListener("click", async () => {
    const main_menu = document.getElementById("main-menu-container");
    main_menu.innerHTML = "";

    const types_drop_menu_container = document.createElement("div");
    types_drop_menu_container.id = "select-type-drop-menu-container";
    // Кнопка выбора типа детали
    const select_type_button = document.createElement("button");
    select_type_button.id = "select-type-button";
    select_type_button.textContent = "Выбрать тип";
    // select_type_button.classList.add("base-button");
    select_type_button.addEventListener("click", async function () {
        types_drop_menu.classList.toggle("hidden");
    });
    types_drop_menu_container.appendChild(select_type_button);

    const response = await fetch(`/all/component/types`);
    const types_list = await response.json();

    const types_drop_menu = document.createElement("div");
    types_drop_menu.id = "select-type-drop-menu";
    types_drop_menu.classList.add("drop-content", "hidden");
    types_drop_menu_container.appendChild(types_drop_menu);

    main_menu.appendChild(types_drop_menu_container);

    const field_list_container = document.createElement("div");
    field_list_container.id = "select-type-fields-list-container";
    field_list_container.classList.add("hidden");

    const field_list = document.createElement("table");
    field_list.id = "select-type-fields-list";
    field_list_container.appendChild(field_list);
    main_menu.appendChild(field_list_container);

    let current_ct = null;
    types_list.forEach(async ct_dict => {
        const a = document.createElement("a");
        a.href = "#";
        a.textContent = ct_dict.ct_rus;
        a.addEventListener("click", async function () {
            // вот сюда фунукцию загрузки TODO
            select_type_button.textContent = ct_dict.ct_rus;
            current_ct = ct_dict.ct;
            types_drop_menu.classList.add("hidden"); // Закрываем меню после выбора

            // Запрос на получение типов деталей
            const response = await fetch("/create/component/fields", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ ct })
            });
            const component_fields = await response.json();

            await updateFieldList(component_fields);
            
            create_component_button.classList.remove("hidden");
        });
        types_drop_menu.appendChild(a);
    });
    
    // Кнопка создания детали
    const create_component_button = document.createElement("button");
    create_component_button.id = "save-component-button";
    create_component_button.textContent = "Добавить";
    create_component_button.classList.add("base-button", "hidden");

    main_menu.appendChild(create_component_button);

    create_component_button.addEventListener("click", async () => saveComponentButtonFunction(current_ct));
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

// Кнопка изменения деталей
document.getElementById("change-component-button").addEventListener("click", async () => {
    await loadAllComponentsMenu();
});
    
