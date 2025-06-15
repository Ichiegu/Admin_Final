// Mobile menu toggle functionality
document
  .querySelector(".mobile-menu-toggle")
  .addEventListener("click", function () {
    document.querySelector(".sidebar").classList.toggle("active");
    document.querySelector(".main-content").classList.toggle("active");
  });

// Update current year in footer
document.getElementById("current-year").textContent = new Date().getFullYear();

// Notification badge click event
document.querySelector(".notification").addEventListener("click", function () {
  alert("You have 5 unread notifications");
});
// Example of a simple chart using Chart.js
const ctx = document.getElementById("myChart").getContext("2d");
const myChart = new Chart(ctx, {
  type: "bar",
  data: {
    labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
    datasets: [
      {
        label: "# of Votes",
        data: [12, 19, 3, 5, 2, 3],
        backgroundColor: [
          "rgba(255, 99, 132, 0.2)",
          "rgba(54, 162, 235, 0.2)",
          "rgba(255, 206, 86, 0.2)",
          "rgba(75, 192, 192, 0.2)",
          "rgba(153, 102, 255, 0.2)",
          "rgba(255, 159, 64, 0.2)",
        ],
        borderColor: [
          "rgba(255, 99, 132, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(75, 192, 192, 1)",
          "rgba(153, 102, 255, 1)",
          "rgba(255, 159, 64, 1)",
        ],
        borderWidth: 1,
      },
    ],
    },

    options: {
        scales: {
            y: {
            beginAtZero: true,
            },
        },
    }
});
// Example of a simple table sorting functionality
const table = document.querySelector("table");
const headers = table.querySelectorAll("th");
headers.forEach((header, index) => {
  header.addEventListener("click", () => {
    const rows = Array.from(table.querySelectorAll("tr:nth-child(n+2)"));
    const isAscending = header.classList.toggle("asc");
    const direction = isAscending ? 1 : -1;

    rows.sort((a, b) => {
      const aText = a.children[index].textContent.trim();
      const bText = b.children[index].textContent.trim();
      return aText.localeCompare(bText, undefined, { numeric: true }) * direction;
    });

    rows.forEach((row) => table.appendChild(row));
  });
});
// Example of a simple form validation
const form = document.querySelector("form");
const emailInput = form.querySelector("input[type='email']");

form.addEventListener("submit", (event) => {

    event.preventDefault();
    const emailValue = emailInput.value.trim();
    if (!validateEmail(emailValue)) {
        alert("Please enter a valid email address.");
        return;
    }
    alert("Form submitted successfully!");
    }
);
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
}
// Example of a simple modal functionality
const modal = document.querySelector(".modal");

const openModalButton = document.querySelector(".open-modal");
const closeModalButton = modal.querySelector(".close-modal");
openModalButton.addEventListener("click", () => {
  modal.classList.add("active");
});
closeModalButton.addEventListener("click", () => {
  modal.classList.remove("active");
});
// Example of a simple tooltip functionality
const tooltipTrigger = document.querySelector(".tooltip-trigger");
const tooltip = document.querySelector(".tooltip");
tooltipTrigger.addEventListener("mouseover", () => {
  tooltip.classList.add("active");
});