import { translate } from "./help.js";
// import { loadBuildInfo } from "./leftMenuFunctions.js";


// Заполняет поля в информации о комплектующей
export function updateField(data) {
    const field_list = document.getElementById("fields-list");
    field_list.innerHTML = "";
    data.forEach(async field => {
        const row = document.createElement("tr");

        const name_td = document.createElement("td");
        name_td.textContent = await translate(field.name);
        name_td.classList.add("component-field-name");
        name_td.id = field.name;

        const input = document.createElement("input");
        input.type ="text";
        input.placeholder = await translate(field.name);
        input.value = field.value;
        input.setAttribute("data-key", field.name);
        input.classList.add("input-component-field");

        const input_td = document.createElement("td")
        input_td.appendChild(input)
        
        row.appendChild(name_td)
        row.appendChild(input_td);
        
        field_list.appendChild(row);
    });
}
