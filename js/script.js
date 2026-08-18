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

  const currentPage = window.location.pathname.split("/").pop() || "index.html";

  navLinks.forEach((link) => {
    link.classList.remove("active");
    const href = link.getAttribute("href") || "";

    // Same-page anchor: "#section"
    if (href === `#${currentSection}`) {
      link.classList.add("active");
      return;
    }

    // Cross-page anchor: "page.html#section" and we're on that page
    if (href.includes("#")) {
      const [hrefPage, hrefHash] = href.split("#");
      const hrefPageName = hrefPage.split("/").pop() || "index.html";
      if (hrefPageName === currentPage && hrefHash === currentSection) {
        link.classList.add("active");
        return;
      }
    }

    // Direct link to the current page (e.g. projects.html)
    if (href === currentPage && !href.includes("#")) {
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

// ===== LIGHTBOX / IMAGE ENLARGEMENT =====
const lightbox = document.getElementById("lightbox");
const lightboxImg = document.getElementById("lightbox-img");
const lightboxCaption = document.getElementById("lightbox-caption");
const lightboxClose = document.querySelector(".lightbox-close");
const lightboxPrev = document.getElementById("lightbox-prev");
const lightboxNext = document.getElementById("lightbox-next");

let lightboxImages = [];
let lightboxIndex = 0;

// Collect all portfolio images
function collectLightboxImages() {
  lightboxImages = Array.from(document.querySelectorAll(".portfolio .box-container .box img"));
}

function openLightbox(index) {
  if (!lightboxImages.length) return;
  lightboxIndex = index;
  const img = lightboxImages[lightboxIndex];
  lightboxImg.src = img.src;
  lightboxImg.alt = img.alt;
  const captionEl = img.closest(".box")?.querySelector(".content h3");
  lightboxCaption.textContent = captionEl ? captionEl.textContent : img.alt;
  lightbox.classList.add("show");
  document.body.style.overflow = "hidden";
}

function closeLightbox() {
  lightbox.classList.remove("show");
  document.body.style.overflow = "";
}

function navigateLightbox(direction) {
  if (!lightboxImages.length) return;
  lightboxIndex = (lightboxIndex + direction + lightboxImages.length) % lightboxImages.length;
  const img = lightboxImages[lightboxIndex];
  lightboxImg.src = img.src;
  lightboxImg.alt = img.alt;
  const captionEl = img.closest(".box")?.querySelector(".content h3");
  lightboxCaption.textContent = captionEl ? captionEl.textContent : img.alt;
}

// Attach click handlers directly to each portfolio box
function attachLightboxHandlers() {
  const boxes = document.querySelectorAll(".portfolio .box-container .box");
  boxes.forEach((box, index) => {
    box.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      collectLightboxImages();
      openLightbox(index);
    });
  });
}

// Also use event delegation as a fallback
document.addEventListener("click", (e) => {
  const box = e.target.closest(".portfolio .box-container .box");
  if (box) {
    e.preventDefault();
    e.stopPropagation();
    collectLightboxImages();
    const index = Array.from(document.querySelectorAll(".portfolio .box-container .box")).indexOf(box);
    openLightbox(index);
  }
});

// Attach handlers on DOM ready and after load
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", attachLightboxHandlers);
} else {
  attachLightboxHandlers();
}
window.addEventListener("load", attachLightboxHandlers);

// Close button
if (lightboxClose) {
  lightboxClose.addEventListener("click", closeLightbox);
}

// Prev / Next navigation
if (lightboxPrev) {
  lightboxPrev.addEventListener("click", (e) => {
    e.stopPropagation();
    navigateLightbox(-1);
  });
}

if (lightboxNext) {
  lightboxNext.addEventListener("click", (e) => {
    e.stopPropagation();
    navigateLightbox(1);
  });
}

// Close when clicking outside the image
if (lightbox) {
  lightbox.addEventListener("click", (e) => {
    if (e.target === lightbox) closeLightbox();
  });
}

// Keyboard navigation
document.addEventListener("keydown", (e) => {
  if (!lightbox || !lightbox.classList.contains("show")) return;
  if (e.key === "Escape") closeLightbox();
  if (e.key === "ArrowLeft") navigateLightbox(-1);
  if (e.key === "ArrowRight") navigateLightbox(1);
});

console.log("Portfolio script loaded successfully.");
