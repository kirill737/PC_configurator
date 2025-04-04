// Открытие меню выбора детали
import { getCurrentComponentData } from "./help.js";
import { updateField } from "./leftMenu.js";

export async function showSelectComponentsMenu(ct) {

    const menu = document.getElementById("components-menu");
    if (!menu) {
        console.log("components menu не существует");
        return; // Проверяем, что меню есть
    }
    
    menu.classList.toggle("hidden");
    const data = await getCurrentComponentData();
    console.log(data);
    
    // const ct = data['ct'];
    const response = await fetch(`/get/all/components/type/${ct}`);
    const components = await response.json();

    const list = document.getElementById("components-list");
    if (!list) return; // Проверяем, что список есть
    
    list.innerHTML = "";

    components.forEach(component => {
        const li = document.createElement("li");
        li.textContent = component.name + ": " + component.id;
        li.addEventListener("click", async () => {
            console.log("Выбралась деталь c id: " + component.id);
            
            const response = await fetch(`/get/${component.id}/fields`)
            const data = await response.json();
            updateField(data);
            
            menu.classList.toggle('hidden'); // Закрываем меню после выбора
        });
        list.appendChild(li);
    });

    document.addEventListener("click", closeMenuOnClickOutside, { once: true });
};

// Функция для закрытия меню выбора детали при клике вне его
function closeMenuOnClickOutside(event) {
    let menu = document.getElementById("components-menu");
    let button = document.getElementById("select-component-button");

    if (!menu || !button) return; // Проверяем, что элементы существуют

    if (!menu.contains(event.target) && !button.contains(event.target)) {
        menu.classList.toggle('hidden');
    } else {
        // Если клик был по кнопке или меню, снова вешаем обработчик
        document.addEventListener("click", closeMenuOnClickOutside, { once: true });
    }
}
