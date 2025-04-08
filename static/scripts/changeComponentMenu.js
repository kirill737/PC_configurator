import { updateField } from "./leftMenu.js";
import { translate } from "./help.js";
// Загрузка видов всех комплектующих в левое меню
export async function loadAllComponentsMenu() {
    
    const response = await fetch(`/all/component/types`);
    const all_types = await response.json();

    const container = document.getElementById("left-menu-container");
    container.innerHTML = "";

    const types_drop_menu_container = document.createElement("div");
    types_drop_menu_container.id = "select-type-drop-menu-container";

    const select_component_type_label = document.createElement("label");
    select_component_type_label.textContent = "Выбрать тип";
    select_component_type_label.id = "select-component-type-label";
    select_component_type_label.type = "text";
    select_component_type_label.addEventListener("click", async function () {
        types_drop_menu.classList.toggle("hidden");
    });
    container.appendChild(select_component_type_label);

    const types_drop_menu = document.createElement("div");
    types_drop_menu.id = "select-type-drop-menu";
    types_drop_menu.classList.add("drop-content", "hidden");
    types_drop_menu_container.appendChild(types_drop_menu);
    container.appendChild(types_drop_menu_container);

    let current_ct = null;
    all_types.forEach(async ct => {
        const a = document.createElement("a");
        a.href = "#";
        a.textContent = await translate(ct);
        a.addEventListener("click", async function () {
            current_ct = ct;
            select_component_type_label.textContent = await translate(ct);
            types_drop_menu.classList.add("hidden"); // Закрываем меню после выбора
            
            const main_container = document.getElementById("main-menu-container");
            main_container.innerHTML = "";
            
            await loadAllComponentWithType(ct);
        });
        types_drop_menu.appendChild(a);
    });

    const components_container = document.createElement("div");
    components_container.id = "components-container";
    // components_container.classList.add("hidden");
    container.appendChild(components_container);
}

async function loadAllComponentWithType(ct) {
    const components_container = document.getElementById("components-container");
    components_container.innerHTML = "";

    let response = await fetch(`/get/all/components/type/${ct}`);
    const components_list = await response.json();

    components_list.forEach(async component => {
        const a = document.createElement("a");
        a.href = "#";
        a.textContent = await translate(component.name);
        a.classList.add("component-button")
        a.addEventListener("click", async function () {
            document.querySelectorAll(".component-button").forEach(b => b.classList.remove("active"));
            this.classList.add("active");

            showSelectComponentsMenu(component.id);
            // drop_btn.textContent = component.name;
            // drop_menu.classList.add("hidden"); // Закрываем меню после выбора
        });
        components_container.appendChild(a);
    });

}

export async function showSelectComponentsMenu(component_id) {
    const main_container = document.getElementById("main-menu-container");
    main_container.innerHTML = "";

    const fields_container = document.createElement("div");
    fields_container.id = "fields-container";
    main_container.appendChild(fields_container);

    const fields_list = document.createElement("table");
    fields_list.id = 'fields-list';
    fields_container.appendChild(fields_list);

    const response = await fetch(`/get/${component_id}/fields`)
    const data = await response.json();
    updateField(data);

    const buttons_container = document.createElement("div");
    buttons_container.id = "button-container";
    const save_fields_button = document.createElement("button");
    save_fields_button.classList.add("base-button");
    save_fields_button.textContent = "Сохранить";
    buttons_container.appendChild(save_fields_button);

    const delete_component_button = document.createElement("button");
    delete_component_button.classList.add("base-button");
    delete_component_button.textContent = "Удалить";
    buttons_container.appendChild(delete_component_button);

    main_container.appendChild(buttons_container);
};