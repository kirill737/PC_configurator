function toggleMenu() {
    let menu = document.getElementById("profileMenu");
    menu.style.display = (menu.style.display === "block") ? "none" : "block";
    console.log("Нажалось")
}

// Закрытие меню при клике вне его
document.addEventListener("click", function(event) {
    let menu = document.getElementById("profileMenu");
    let icon = document.querySelector(".profile-icon");

    if (!menu.contains(event.target) && !icon.contains(event.target)) {
        menu.style.display = "none";
    }
});
