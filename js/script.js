const menu = document.querySelector("#menu-btn");
const header = document.querySelector(".header");
const themeToggler = document.querySelector("#theme-toggler");

if (menu) {
  menu.addEventListener("click", () => {
    menu.classList.toggle("fa-times");
    if (header) header.classList.toggle("active");
  });
}

window.addEventListener("scroll", () => {
  if (menu) menu.classList.remove("fa-times");
  if (header) header.classList.remove("active");
});

if (themeToggler) {
  themeToggler.addEventListener("click", () => {
    themeToggler.classList.toggle("fa-sun");
    document.body.classList.toggle("active");
  });
}

const typedElement = document.querySelector(".typed");
if (typedElement && typeof Typed !== "undefined") {
  const typedStrings = (typedElement.getAttribute("data-typed-items") || "").split(",");
  new Typed(".typed", {
    strings: typedStrings,
    loop: true,
    typeSpeed: 100,
    backSpeed: 50,
    backDelay: 100,
    showCursor: false,
  });
}

window.addEventListener("load", () => {
  document.body.classList.add("active");
});

console.log("Portfolio script loaded successfully.");
