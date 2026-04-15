
import os
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ClientError, ServerError

#  Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

#  Gemini client
client = genai.Client(api_key=api_key)

# Flask app
app = Flask(__name__)
CORS(app)

#  Load website data
with open("data.txt", "r", encoding="utf-8") as f:
    website_data = f.read()

#  Chat history
chat_history = []

# Order storage
order = []

#  Token counter
token_number = 100

#  Delivery state
order_mode = None
delivery_mode = False
delivery_data = {}

#  Menu with prices
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

#  Chatbot function
def chatbot_reply(message):
    global token_number, order_mode, delivery_mode, delivery_data

    msg = message.lower()

    # =========================
    #  ADD ITEM
    # =========================
    for item in menu:
        if item in msg:
            order.append(item)
            return f"✅ {item.title()} added (₹{menu[item]})"

    # =========================
    #  SHOW ORDER
    # =========================
    if "my order" in msg or "show order" in msg:
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
                return f"❌ {item.title()} removed from your order!"

    # =========================
    #  PLACE ORDER → CHOOSE TYPE
    # =========================
    if "place order" in msg or "checkout" in msg:
        if not order:
            return "🛒 Your cart is empty."

        order_mode = "choose"

        return """🪑 Please choose order type:

1️⃣ Dine-in  
2️⃣ Delivery  

Type 'dine-in' or 'delivery'
"""

    # =========================
    #  DINE-IN OR  DELIVERY
    # =========================
    if order_mode == "choose":

        #  Dine-in
        if "dine" in msg:
            order_mode = None

            token_number += 1

            total = sum(menu[i] for i in order)
            items = "\n".join([f"• {i.title()} - ₹{menu[i]}" for i in order])

            order.clear()

            return f"""🪑 Dine-in Order Confirmed!

🎟️ Token Number: {token_number}

🛒 Items:
{items}

💰 Total: ₹{total}

👉 Please tell your token number at the counter.
⏳ Ready in 5–10 minutes.
☕ Enjoy your coffee!
"""

        #  Delivery
        elif "delivery" in msg:
            order_mode = None
            delivery_mode = True
            delivery_data.clear()

            return "📦 Enter your name for delivery:"

    # =========================
    #  DELIVERY FLOW
    # =========================
    if delivery_mode:

        if "name" not in delivery_data:
            delivery_data["name"] = message
            return "📞 Enter your phone number:"

        elif "phone" not in delivery_data:
            delivery_data["phone"] = message
            return "🏠 Enter your delivery address:"

        elif "address" not in delivery_data:
            delivery_data["address"] = message

            total = sum(menu[i] for i in order)
            items = "\n".join([f"• {i.title()} - ₹{menu[i]}" for i in order])

            delivery_mode = False
            order.clear()

            return f"""🚚 Delivery Order Confirmed!

👤 Name: {delivery_data['name']}
📞 Phone: {delivery_data['phone']}
🏠 Address: {delivery_data['address']}

🛒 Items:
{items}

💰 Total: ₹{total}

🚚 Your order will be delivered soon!
☕ Thank you!
"""

    # =========================
    #  QUICK RESPONSES
    # =========================
    if "menu" in msg:
        return """☕ Our Menu:

• Espresso - ₹120  
• Cappuccino - ₹150  
• Latte - ₹140  
• Americano - ₹130  

❄️ Cold Drinks:
• Cold Coffee - ₹160  
• Iced Latte - ₹170  
• Milkshakes - ₹180  

🍰 Desserts:
• Cake - ₹100  
• Brownie - ₹90  
"""

    if "suggest" in msg or "recommend" in msg:
        return "☕ Try Cappuccino or Cold Coffee — both are popular!"

    if "offer" in msg:
        return "🎉 We have combo offers and discounts!"

    if "wifi" in msg:
        return "📶 Free WiFi available!"
    
    if "payment" in msg:
        return "💳 We accept UPI, cards, and cash."

    # =========================
    #  GEMINI AI
    # =========================
    chat_history.append(f"User: {message}")

    if len(chat_history) > 6:
        chat_history.pop(0)

    prompt = f"""
    You are a coffee shop assistant.

    Answer ONLY from this data:
    {website_data}

    Keep answers short.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        reply = response.text

    except ClientError as e:
        if "quota" in str(e).lower():
            reply = "⚠️ API limit exceeded."
        else:
            reply = "⚠️ Request error."

    except ServerError:
        reply = "⚠️ Server busy."

    except Exception:
        reply = "⚠️ Something went wrong."

    chat_history.append(f"Bot: {reply}")

    return reply


#  API
@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json["message"]
    reply = chatbot_reply(user_msg)
    return jsonify({"reply": reply})


@app.route("/")
def home():
    return "☕ Coffee Chatbot Backend is running!"

#  Run
if __name__ == "__main__":
    print("🚀 Server running...")
    app.run(debug=True, port=5000)