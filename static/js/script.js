console.log("Script loaded");

// Optionally handle redirects or alerts on form submission
document.addEventListener("DOMContentLoaded", () => {
  const forms = document.querySelectorAll("form");
  forms.forEach(form => {
    form.addEventListener("submit", (e) => {
      console.log("Form submitted:", form.action);
    });
  });
});
