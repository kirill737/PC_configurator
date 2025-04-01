
async function getCurrentComponentData() {
    const response = await fetch(`/get/current/component/data`);
    const data = await response.json();
    console.log("Данные получен");
    return data;
}

async function setCurrentComponentDataBuildId(build_id) {
    const response = await fetch("/set/current/component/data/build_id", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            'build_id': build_id
        })
    });
}

async function setCurrentComponentDataCT(ct) {
    console.log("setCurrentComponentDataCT");
    const response = await fetch("/set/current/component/data/ct", {
        
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            'ct': ct
        })
    });
}

// Открытие меню выбора детали
async function showSelectComponentsMenu() {
    console.log("Выбор детали...");
    // const button = document.getElementById("select-component-button");

    const menu = document.getElementById("components-menu");
    if (!menu) return; // Проверяем, что меню есть

    menu.classList.toggle("hidden");
    const data = await getCurrentComponentData();
    console.log(data);
    const ct = data['ct'];
    const response = await fetch(`/get/all/components/type/${ct}`);
    const components = await response.json();

    const list = document.getElementById("components-list");
    if (!list) return; // Проверяем, что список есть
    
    console.log("Заполняем список деталей...");
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
