const navbarLinks = document.querySelectorAll(".nav-menu .nav-link");
const menuOpenButton = document.querySelector("#menu-open-button");
const menuCloseButton = document.querySelector("#menu-close-button");

menuOpenButton.addEventListener("click", () => {
  document.body.classList.toggle("show-mobile-menu");
});

menuCloseButton.addEventListener("click", () => menuOpenButton.click());
navbarLinks.forEach((link) => {
  link.addEventListener("click", () => menuOpenButton.click());
});
let swiper = new Swiper(".slider-wrapper", {
  loop: true,
  grabCursor: true,
  spaceBetween: 25,
  // Pagination bullets
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
    dynamicBullets: true,
  },
  // Navigation arrows
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  /* Responsive breakpoints */
  breakpoints: {
    0: {
      slidesPerView: 1,
    },
    768: {
      slidesPerView: 2,
    },
    1024: {
      slidesPerView: 3,
    },
  },
});

async function sendMessage() {
  const input = document.getElementById("userInput");
  const message = input.value;

  const chatbox = document.getElementById("chatbox");

  // User message
  chatbox.innerHTML += `<div class="user">You: ${message}</div>`;

  // Typing effect
  chatbox.innerHTML += `<div class="bot" id="typing">Bot is typing...</div>`;

  const res = await fetch("http://localhost:5000/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message }),
  });

  const data = await res.json();

  // Remove typing
  document.getElementById("typing").remove();

  // Bot message
  chatbox.innerHTML += `<div class="bot">Bot: ${data.reply}</div>`;

  chatbox.scrollTop = chatbox.scrollHeight;

  input.value = "";
}

const chatbot = document.getElementById("chatbot");
const toggleBtn = document.getElementById("chat-toggle");
const closeBtn = document.getElementById("close-btn");
const chatbox = document.getElementById("chatbox");

// Open chatbot
toggleBtn.onclick = () => {
  chatbot.classList.add("active");

  if (chatbox.innerHTML === "") {
    addBotMessage("Hi ☕ Welcome to Caffeine Hub! How can I help you?");
  }
};

// Close chatbot
closeBtn.onclick = () => {
  chatbot.classList.remove("active");
};

// Add user message
function addUserMessage(text) {
  const div = document.createElement("div");
  div.className = "message user";
  div.innerText = text;
  chatbox.appendChild(div);
}

// Add bot message
function addBotMessage(text) {
  const div = document.createElement("div");
  div.className = "message bot";
  div.innerText = text;
  chatbox.appendChild(div);
}

// Typing animation
function showTyping() {
  const div = document.createElement("div");
  div.className = "message bot";
  div.id = "typing";
  div.innerText = "Typing...";
  chatbox.appendChild(div);
}

// Remove typing
function removeTyping() {
  const typing = document.getElementById("typing");
  if (typing) typing.remove();
}

// Send message
async function sendMessage() {
  const input = document.getElementById("userInput");
  const message = input.value;

  if (!message) return;

  addUserMessage(message);
  showTyping();

  chatbox.scrollTop = chatbox.scrollHeight;

  const res = await fetch("https://coffeeshop-chatbot.onrender.com/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });

  const data = await res.json();

  removeTyping();
  addBotMessage(data.reply);

  chatbox.scrollTop = chatbox.scrollHeight;

  input.value = "";
}

function quickAsk(text) {
  const input = document.getElementById("userInput");

  input.value = text;

  // simulate Enter key feel
  sendMessage();

  input.focus();
}
