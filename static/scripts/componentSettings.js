document.getElementById("open-component-settings-button").addEventListener("click", async () => {
    // console.log("Нажали кнопку")
    const menu = document.getElementById("components-settings-container");
    menu.classList.toggle("hidden");
    const create_build_button = document.getElementById("create-build-button");
    // create_build_button.classList.toggle("hidden");

    const response = await fetch("/open/<ct>");
    const component_fields = await response.json();

    const list = document.getElementById("fields-list");
    list.innerHTML = "";
    create_build_button.dispay ="block";
    builds.forEach(build => {
        const li = document.createElement("li");
        li.textContent = build.name + build.id;
        li.addEventListener("click", () => loadBuildComponents(build.id));
        list.appendChild(li);
    });
});