document.getElementById("submit-button").addEventListener("click", () => {
  const form = document.getElementById("quiz-form");
  const formData = new FormData(form);
  const answers = {};
  for (const [key, value] of formData.entries()) {
    answers[key.substring(1)] = value;
  }

  fetch("/submit", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ answers }),
  })
    .then((response) => response.json())
    .then((data) => {
      alert(`You scored ${data.score} out of ${data.total}`);
    })
    .catch((error) => console.error("Error:", error));
});
