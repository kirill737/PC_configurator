function toggle_menu() {
    let menu = document.getElementById("profile-menu");
    menu.style.display = (menu.style.display === "block") ? "none" : "block";
    console.log("Нажалось")
}

// Закрытие меню при клике вне его
document.addEventListener("click", function(event) {
    let menu = document.getElementById("profile-menu");
    let icon = document.getElementById("profile-icon");

    if (!menu.contains(event.target) && !icon.contains(event.target)) {
        menu.style.display = "none";
    }
});
