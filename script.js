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
const chatbot = document.getElementById("chatbot");
const toggleBtn = document.getElementById("chat-toggle");
const closeBtn = document.getElementById("close-btn");
const chatbox = document.getElementById("chatbox");

// =========================
// OPEN CHAT
// =========================
toggleBtn.onclick = () => {
  chatbot.classList.add("active");

  if (chatbox.innerHTML === "") {
    addBotMessage("Hi ☕ Welcome to Caffeine Hub! How can I help you?");
  }
};

// =========================
// CLOSE CHAT
// =========================
closeBtn.onclick = () => {
  chatbot.classList.remove("active");
};

// =========================
// ADD USER MESSAGE
// =========================
function addUserMessage(text) {
  const div = document.createElement("div");
  div.className = "message user";
  div.innerText = text;
  chatbox.appendChild(div);
}

// =========================
// ADD BOT MESSAGE
// =========================
function addBotMessage(text) {
  const div = document.createElement("div");
  div.className = "message bot";
  div.innerText = text;
  chatbox.appendChild(div);
}

// =========================
// SHOW TYPING
// =========================
function showTyping() {
  const div = document.createElement("div");
  div.className = "message bot";
  div.id = "typing";
  div.innerText = "Typing...";
  chatbox.appendChild(div);
}

// =========================
// REMOVE TYPING
// =========================
function removeTyping() {
  const typing = document.getElementById("typing");
  if (typing) typing.remove();
}

// =========================
// SEND MESSAGE
// =========================
async function sendMessage() {
  const input = document.getElementById("userInput");
  const message = input.value;

  if (!message) return;

  addUserMessage(message);
  showTyping();

  chatbox.scrollTop = chatbox.scrollHeight;

  try {
    const res = await fetch("https://coffeeshop-chatbot.onrender.com/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    // Check response
    if (!res.ok) {
      throw new Error("Server error");
    }

    const data = await res.json();

    removeTyping();
    addBotMessage(data.reply);

  } catch (error) {
    console.error("Error:", error);

    removeTyping();
    addBotMessage("⚠️ Server error. Please try again.");
  }

  chatbox.scrollTop = chatbox.scrollHeight;
  input.value = "";
}

// =========================
// QUICK BUTTONS
// =========================
function quickAsk(text) {
  const input = document.getElementById("userInput");

  input.value = text;
  sendMessage();

  input.focus();
}