import { getCurrentBuildId, translate  } from "./help.js";
import { loadBuildInfo, loadComponentFields } from "./leftMenuFunctions.js"; 


// Функия создания меню создания комплектующей
export async function updateFieldList(data) {
    const field_list = document.getElementById("select-type-fields-list");
    field_list.innerHTML = "";
    const field_list_container = document.getElementById("select-type-fields-list-container");
    field_list_container.classList.remove("hidden");

    console.log(data);
    for (let i = 0; i < data.fields.length; i++) {
        const row = document.createElement("tr");

        const name_td = document.createElement("td");
        name_td.textContent = data.fields_rus[i];
        name_td.classList.add("component-field-name");
        name_td.id = data.fields[i];
        row.appendChild(name_td)

        const input_td = document.createElement("td")

        const input = document.createElement("input");
        input.type ="text";
        input.placeholder = data.fields_rus[i];
        input.classList.add("input-component-field");
        input_td.appendChild(input)
        row.appendChild(input_td);

        field_list.appendChild(row);
    };
}

// Функция создания списка 
export async function saveComponentButtonFunction(ct) {
    const component_data = {};
    component_data['ct'] = ct;
    component_data['price'] = 0; // TODO: добавить цену детали
    component_data['info'] = {};

    const inputs = document.querySelectorAll(".input-component-field");
    inputs.forEach(input => {
        const fieldName = input.parentElement.previousElementSibling.id;
        component_data['info'][fieldName] = input.value;
        console.log(fieldName, input.value);
    });

    const response = await fetch("/create/component", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(component_data)
    });
    const result = await response.json();
    console.log(result);
    if (result.status == "success") {
        alert("Деталь создана!");
        // location.reload();
    } else {
        alert(result.message);
    }
};

// Загрузка видов всех комплектующих в левое меню
export async function loadBuildComponents(buildName, buildId) {
    console.log("build_id в load: " + buildId)

    const container = document.getElementById("left-menu-container");
    container.innerHTML = "";

    const build_name_label = document.createElement("label");
    build_name_label.textContent = buildName;
    build_name_label.id = "build-name-label";
    build_name_label.type = "text";
    loadBuildInfo(buildId);
    build_name_label.addEventListener("click", () => loadBuildInfo(buildId));
    container.appendChild(build_name_label);

    let response = await fetch(`/all/component/types`); // NOW
    const types = await response.json();

    types.forEach(async ct_dict => {
        const component_btn = document.createElement("a");
        component_btn.className = "component-button";
        component_btn.textContent = ct_dict.ct_rus;
        component_btn.href = "#";
        component_btn.addEventListener("click", () => loadComponentFields(ct_dict.ct, buildId));

        component_btn.addEventListener("click", function () {
            document.querySelectorAll(".component-button").forEach(b => b.classList.remove("active"));
            this.classList.add("active");
        });

        container.appendChild(component_btn);
    });

    let menu = document.getElementById("builds-menu");
    menu.classList.add("hidden");
}

// Фу