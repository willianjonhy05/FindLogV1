
const sidebar = document.getElementById("sidebar");
const toggle = document.getElementById("sidebarToggle");
const overlay = document.getElementById("overlay");


toggle.addEventListener("click", () => {

    sidebar.classList.toggle("show");
    overlay.classList.toggle("show");

});


overlay.addEventListener("click", () => {

    sidebar.classList.remove("show");
    overlay.classList.remove("show");

});

