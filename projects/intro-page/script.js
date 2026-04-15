const quoteElement = document.getElementById("quote");
const newQuoteButton = document.getElementById("newQuote");

const quotes = [
  "Start small, keep going, and your progress will surprise you.",
  "Great developers are built one project at a time.",
  "Learn by building, and build while learning.",
  "Consistency is stronger than talent when talent does not practice."
];

function showRandomQuote() {
  const randomIndex = Math.floor(Math.random() * quotes.length);
  quoteElement.textContent = quotes[randomIndex];
}

newQuoteButton.addEventListener("click", showRandomQuote);
showRandomQuote();
