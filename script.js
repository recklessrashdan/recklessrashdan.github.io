const menuToggle = document.querySelector(".menu-toggle");
const navLinks = document.querySelector(".nav-links");
const navAnchors = document.querySelectorAll(".nav-links a");
const sections = document.querySelectorAll("main section[id]");
const year = document.getElementById("year");
const contactForm = document.getElementById("contactForm");
const formNotice = document.getElementById("formNotice");
// Update this URL after deploying the Cloudflare Worker (see workers/wrangler.toml).
const CONTACT_API_URL =
  window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
    ? "/api/contact"
    : "https://recklessrashdan-contact.YOUR_SUBDOMAIN.workers.dev";

if (menuToggle && navLinks) {
  menuToggle.addEventListener("click", () => {
    navLinks.classList.toggle("open");
  });
}

navAnchors.forEach((anchor) => {
  anchor.addEventListener("click", () => {
    if (navLinks) {
      navLinks.classList.remove("open");
    }
  });
});

window.addEventListener("scroll", () => {
  let currentSectionId = "";

  sections.forEach((section) => {
    const sectionTop = section.offsetTop - 120;
    if (window.scrollY >= sectionTop) {
      currentSectionId = section.getAttribute("id") || "";
    }
  });

  navAnchors.forEach((anchor) => {
    anchor.classList.remove("active");
    if (anchor.getAttribute("href") === `#${currentSectionId}`) {
      anchor.classList.add("active");
    }
  });
});

if (year) {
  year.textContent = String(new Date().getFullYear());
}

if (contactForm && formNotice) {
  contactForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const submitButton = contactForm.querySelector('button[type="submit"]');
    const formData = new FormData(contactForm);

    const payload = {
      name: String(formData.get("name") || "").trim(),
      email: String(formData.get("email") || "").trim(),
      message: String(formData.get("message") || "").trim()
    };

    if (!payload.name || !payload.email || !payload.message) {
      formNotice.textContent = "Please complete all fields before sending.";
      return;
    }

    formNotice.textContent = "Sending...";
    if (submitButton) {
      submitButton.disabled = true;
    }

    try {
      const response = await fetch(CONTACT_API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || "Request failed");
      }

      formNotice.textContent = "Message sent successfully. Thank you.";
      contactForm.reset();
    } catch (error) {
      formNotice.textContent = "Could not send message. Please try again.";
    } finally {
      if (submitButton) {
        submitButton.disabled = false;
      }
    }
  });
}
