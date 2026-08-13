const menu = document.querySelector("#menu-btn");
const header = document.querySelector(".header");
const themeToggler = document.querySelector("#theme-toggler");
const navLinks = document.querySelectorAll(".header .navbar a");

if (menu) {
  menu.addEventListener("click", () => {
    menu.classList.toggle("fa-times");
    if (header) header.classList.toggle("active");
  });
}

// Close mobile menu when a nav link is clicked
navLinks.forEach((link) => {
  link.addEventListener("click", () => {
    if (menu) menu.classList.remove("fa-times");
    if (header) header.classList.remove("active");
  });
});

// Highlight active nav link based on scroll position
function setActiveNavLink() {
  const scrollPos = window.scrollY + 100;
  let currentSection = "";

  document.querySelectorAll("section[id]").forEach((section) => {
    const sectionTop = section.offsetTop;
    const sectionBottom = sectionTop + section.offsetHeight;
    if (scrollPos >= sectionTop && scrollPos < sectionBottom) {
      currentSection = section.getAttribute("id");
    }
  });

  navLinks.forEach((link) => {
    link.classList.remove("active");
    if (link.getAttribute("href") === `#${currentSection}`) {
      link.classList.add("active");
    }
  });
}

window.addEventListener("scroll", () => {
  if (menu) menu.classList.remove("fa-times");
  if (header) header.classList.remove("active");
  setActiveNavLink();
});

// Set active link on page load
window.addEventListener("load", () => {
  setActiveNavLink();
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
