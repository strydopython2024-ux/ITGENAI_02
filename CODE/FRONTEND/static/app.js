document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("file-input");
  const name = document.getElementById("file-name");

  if (input && name) {
    input.addEventListener("change", () => {
      name.textContent = input.files.length
        ? input.files[0].name
        : "CSV files up to 25 MB";
    });
  }

  const form = document.getElementById("ai-chat-form");
  const question = document.getElementById("ai-question");
  const messages = document.getElementById("ai-messages");
  const sendButton = document.getElementById("ai-send");
  const sendLabel = document.getElementById("ai-send-label");
  const clearButton = document.getElementById("clear-chat");
  const suggestions = document.querySelectorAll(".ai-suggestion");

  if (!form || !question || !messages) return;

  const history = [];

  function escapeHtml(value) {
    const div = document.createElement("div");
    div.textContent = value;
    return div.innerHTML;
  }

  function addMessage(role, content, temporary = false) {
    const wrapper = document.createElement("div");
    wrapper.className = `ai-message ${role}${temporary ? " ai-temporary" : ""}`;

    const avatar = role === "user" ? "You" : "AI";
    const label = role === "user" ? "You" : "Gemini Business Analyst";

    wrapper.innerHTML = `
      <div class="ai-avatar">${avatar}</div>
      <div class="ai-bubble">
        <div class="ai-message-label">${label}</div>
        <div class="ai-message-content">${escapeHtml(content).replace(/\n/g, "<br>")}</div>
      </div>
    `;

    messages.appendChild(wrapper);
    messages.scrollTop = messages.scrollHeight;
    return wrapper;
  }

  function setLoading(loading) {
    sendButton.disabled = loading;
    question.disabled = loading;
    sendLabel.textContent = loading ? "Thinking..." : "Send";
  }

  function resizeInput() {
    question.style.height = "auto";
    question.style.height = `${Math.min(question.scrollHeight, 150)}px`;
  }

  question.addEventListener("input", resizeInput);

  question.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      form.requestSubmit();
    }
  });

  suggestions.forEach((button) => {
    button.addEventListener("click", () => {
      question.value = button.textContent.trim();
      resizeInput();
      question.focus();
    });
  });

  clearButton?.addEventListener("click", () => {
    history.length = 0;
    messages.innerHTML = `
      <div class="ai-message assistant">
        <div class="ai-avatar">AI</div>
        <div class="ai-bubble">
          <div class="ai-message-label">Gemini Business Analyst</div>
          <div>Hello. I’m ready to analyze your active dataset. Ask me a question.</div>
        </div>
      </div>
    `;
  });

  async function checkStatus() {
    const dot = document.getElementById("ai-status-dot");
    const text = document.getElementById("ai-status-text");
    if (!dot || !text) return;

    try {
      const endpoint = (window.AI_CHAT_CONFIG?.endpoint || "").replace("/chat", "/status");
      const response = await fetch(endpoint);
      const data = await response.json();

      if (response.ok && data.configured) {
        dot.classList.add("online");
        text.textContent = `${data.model} ready`;
      } else {
        dot.classList.add("offline");
        text.textContent = "Gemini API key not configured";
      }
    } catch {
      dot.classList.add("offline");
      text.textContent = "AI service unavailable";
    }
  }

  checkStatus();

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const text = question.value.trim();
    if (!text || sendButton.disabled) return;

    addMessage("user", text);
    history.push({ role: "user", content: text });

    const temporary = addMessage("assistant", "Analyzing your dataset...", true);
    setLoading(true);
    question.value = "";
    resizeInput();

    try {
      const endpoint = window.AI_CHAT_CONFIG?.endpoint;
      if (!endpoint) throw new Error("AI endpoint is not configured.");

      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: text,
          history: history.slice(-11, -1)
        })
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.detail || data.message || "Unable to get an AI response.");
      }

      const answer = data.answer || "No answer was generated.";
      temporary.remove();
      addMessage("assistant", answer);
      history.push({ role: "assistant", content: answer });
    } catch (error) {
      temporary.remove();
      addMessage("assistant", `Sorry, I couldn't complete that request. ${error.message}`);
      history.pop();
    } finally {
      setLoading(false);
      question.focus();
    }
  });
});
