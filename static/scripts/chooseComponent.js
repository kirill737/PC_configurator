// Загрузка комплектующих в сборке
// async function selectComponentsMenu() {
//     console.log("Загрузка всех деталей вида");
//     const response = await fetch(`/select/component/<ct>`);
//     const components = await response.json();
    
//     const container = document.getElementById("components-menu");
    
//     container.innerHTML = "";
//     // console.log(components);
//     components.forEach(component => {
//         const component_btn = document.createElement("a");
//         component_btn.className = "";
//         component_btn.textContent = component.name;
//         component_btn.href = "#";
//         component_btn.addEventListener("click", () => loadComponentFields(component.id, component.type));
        
//         container.appendChild(component_btn);
//         console.log("Добавлена кнопка: " + component.type);
//         // console.log(`${key}: ${obj[key]}`);
//     })
//     let menu = document.getElementById("builds-menu");
//     menu.classList.add("hidden");
// }



