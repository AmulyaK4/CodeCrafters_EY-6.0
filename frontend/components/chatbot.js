export function renderChat(container) {
  container.classList.add("flex", "flex-col");
}

export function pushMessage(container, { from, text }) {
  const bubble = document.createElement("div");
  bubble.className = `chat-bubble ${from === "user" ? "user ml-auto" : "bot mr-auto"}`;
  bubble.textContent = text;
  container.appendChild(bubble);
  container.scrollTop = container.scrollHeight;
}

export function pushStructured(container, text) {
  const bubble = document.createElement("div");
  bubble.className = "chat-bubble bot mr-auto whitespace-pre-line";
  bubble.textContent = text;
  container.appendChild(bubble);
  container.scrollTop = container.scrollHeight;
}

