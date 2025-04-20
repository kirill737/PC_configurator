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

        const input = document.createElement("a");
        input.type ="text";
        // input.placeholder = await translate(field.name);
        input.textContent = field.value;
        input.setAttribute("data-key", field.name);

        const input_td = document.createElement("td")
        input_td.classList.add("component-field");
        input_td.appendChild(input)
        
        row.appendChild(name_td)
        row.appendChild(input_td);
        
        field_list.appendChild(row);
    });
}
