const dateElement = document.getElementById("date");
const timeElement = document.getElementById("time");
const toggleButton = document.getElementById("toggleFormat");

let is24Hour = false;

function updateClock() {
  const now = new Date();

  const dateText = now.toLocaleDateString(undefined, {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric"
  });

  const timeText = now.toLocaleTimeString(undefined, {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: !is24Hour
  });

  dateElement.textContent = dateText;
  timeElement.textContent = timeText;
}

toggleButton.addEventListener("click", () => {
  is24Hour = !is24Hour;
  toggleButton.textContent = is24Hour ? "Switch to 12-hour" : "Switch to 24-hour";
  updateClock();
});

updateClock();
setInterval(updateClock, 1000);
