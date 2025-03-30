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
    console.log(component_fields);
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
        // li.addEventListener("click", () => loadBuildComponents(build.id));
        field_list.appendChild(row);
    });
});