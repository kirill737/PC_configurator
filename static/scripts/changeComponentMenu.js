import { updateField } from "./leftMenu.js";
import { translate, getCurrentCT, setCurrentCT } from "./help.js";

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

    all_types.forEach(async ct_dict => {
        const a = document.createElement("a");
        a.href = "#";
        a.textContent = ct_dict.ct_rus;
        a.addEventListener("click", async function () {
            // current_ct = ct;
            select_component_type_label.textContent = ct_dict.ct_rus;
            types_drop_menu.classList.add("hidden"); // Закрываем меню после выбора
            
            const main_container = document.getElementById("main-menu-container");
            main_container.innerHTML = "";
            console.log("<loadAllComponentsMenu>")
            await loadAllComponentWithType(ct_dict.ct);
        });
        types_drop_menu.appendChild(a);
    });

    const components_container = document.createElement("div");
    components_container.id = "components-container";
    // components_container.classList.add("hidden");
    container.appendChild(components_container);
}

async function loadAllComponentWithType(ct) {
    console.log("<loadAllComponentWithType>: Загрузка полей типа: " + ct);
    await setCurrentCT(ct);
    console.log("Обновляем поля");
    const components_container = document.getElementById("components-container");
    components_container.innerHTML = "";

    let response = await fetch(`/get/all/components/type/${ct}`);
    const components_list = await response.json();

    components_list.forEach(async component => {
        const a = document.createElement("a");
        a.href = "#";
        a.textContent = component.name;
        a.classList.add("component-button")
        a.addEventListener("click", async function () {
            document.querySelectorAll(".component-button").forEach(b => b.classList.remove("active"));
            this.classList.add("active");
            console.log("component.id:" + component.id)
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
    save_fields_button.addEventListener("click", async () => saveComponent(component_id));
    
    const delete_component_button = document.createElement("button");
    delete_component_button.classList.add("base-button");
    delete_component_button.textContent = "Удалить";
    buttons_container.appendChild(delete_component_button);
    delete_component_button.addEventListener("click", async () => deleteComponent(component_id));

    main_container.appendChild(buttons_container);
};

async function deleteComponent(component_id) {
    const response = await fetch(`/delete/component/${component_id}`);

    const result = await response.json();
    console.log(result);
    if (result.status == "success") {
        alert("Деталь удалена!");

        const ct = await getCurrentCT();
        
        console.log("<delete button>")
        await loadAllComponentWithType(ct);
        const main_container = document.getElementById("main-menu-container");
        main_container.innerHTML = "";
    } else {
        alert(result.message);
    }
}

async function saveComponent(component_id) {
    const component_data = {};
    component_data['id'] = component_id;
    component_data['price'] = 0; // TODO: добавить цену детали
    component_data['info'] = {};

    const inputs = document.querySelectorAll(".input-component-field");
    inputs.forEach(input => {
        const fieldName = input.parentElement.previousElementSibling.id;
        component_data['info'][fieldName] = input.value;
        console.log(fieldName, input.value);
    });

    const response = await fetch("/change/component", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(component_data)
    });

    const result = await response.json();
    console.log(result);
    if (result.status == "success") {
        alert("Деталь изменена!");
        const ct = await getCurrentCT();
        console.log("<save button>")
        await loadAllComponentWithType(ct);
    } else {
        alert(result.message);
    }
};