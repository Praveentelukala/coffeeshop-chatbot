import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai

#  Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

app = Flask(__name__)
CORS(app)

# Load data
try:
    with open("data.txt", "r", encoding="utf-8") as f:
        website_data = f.read()
except:
    website_data = "Coffee shop menu: espresso, cappuccino, latte"

#  Order memory
order = []

#  Menu
menu = {
    "espresso": 120,
    "cappuccino": 150,
    "latte": 140,
    "americano": 130,
    "cold coffee": 160,
    "iced latte": 170,
    "milkshake": 180,
    "cake": 100,
    "brownie": 90,
    "burger": 120,
    "fries": 80
}

# =========================
#  CHATBOT FUNCTION
# =========================
def chatbot_reply(message):
    msg = message.lower()

    # =========================
    #  ADD ITEM
    # =========================
    for item in menu:
        if f"add {item}" in msg:
            order.append(item)
            return f"✅ {item.title()} added (₹{menu[item]})"

    # =========================
    #  SHOW ORDER
    # =========================
    if "show order" in msg or "my order" in msg:
        if not order:
            return "🛒 Your order is empty."

        total = sum(menu[i] for i in order)
        items = "\n".join([f"• {i.title()} - ₹{menu[i]}" for i in order])

        return f"""🛒 Your Order:

{items}

💰 Total: ₹{total}
"""

    # =========================
    #  REMOVE ITEM
    # =========================
    if "remove" in msg:
        for item in menu:
            if item in msg and item in order:
                order.remove(item)
                return f"❌ {item.title()} removed!"

    # =========================
    #  MENU
    # =========================
    if "menu" in msg:
        items = "\n".join([f"• {item.title()} - ₹{price}" for item, price in menu.items()])
        return f"""☕ Menu:

{items}
"""

    # =========================
    #  AVAILABILITY
    # =========================
    if "available" in msg or "have" in msg:
        for item in menu:
            if item in msg:
                return f"✅ Yes, {item.title()} is available!"
        return "❌ Sorry, that item is not available."

    # =========================
    #  AI FALLBACK (IMPORTANT)
    # =========================
    try:
        prompt = f"""
You are a friendly coffee shop assistant.

Rules:
- Answer naturally like a human
- If question is about coffee → give helpful answer
- If general question → answer briefly
- DO NOT say "I am an AI model"
- Keep answers short (2–3 lines max)

Menu:
{website_data}

User: {message}
"""

        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        return response.text if response.text else "☕ Ask me about menu or drinks!"

    except Exception as e:
        print("Gemini Error:", e)
        return "⚠️ Server busy. Please try again."


# =========================
#  API
# =========================
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"reply": "Invalid request"}), 400

        reply = chatbot_reply(data["message"])
        return jsonify({"reply": reply})

    except Exception as e:
        print("Server Error:", e)
        return jsonify({"reply": "⚠️ Server error"}), 500


@app.route("/")
def home():
    return "☕ Coffee Chatbot Running"


# =========================
#  RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)