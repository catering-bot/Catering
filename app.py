import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

orders = {}

@app.event("message")
def handle_message(event, say, client):
    user = event.get("user")
    text = event.get("text", "").lower()

    if not user:
        return

    if user not in orders:
        orders[user] = {"step": 0}

    step = orders[user]["step"]

    if step == 0:
        say("👋 Здравствуйте! Напишите *старт* чтобы оформить заказ.")
        orders[user]["step"] = 1

    elif step == 1 and "старт" in text:
        say("📅 Укажите дату мероприятия (например: 25 мая)")
        orders[user]["step"] = 2

    elif step == 2:
        orders[user]["date"] = event["text"]
        say("👥 Сколько гостей ожидается?")
        orders[user]["step"] = 3

    elif step == 3:
        orders[user]["guests"] = event["text"]
        say("🍽️ Какой тип меню?\n1️⃣ Фуршет\n2️⃣ Банкет\n3️⃣ Бизнес-ланч")
        orders[user]["step"] = 4

    elif step == 4:
        orders[user]["menu"] = event["text"]
        say("📍 Укажите адрес мероприятия")
        orders[user]["step"] = 5

    elif step == 5:
        orders[user]["address"] = event["text"]
        summary = f"""
📦 *Новый заказ!*
👤 Клиент: <@{user}>
📅 Дата: {orders[user]['date']}
👥 Гостей: {orders[user]['guests']}
🍽️ Меню: {orders[user]['menu']}
📍 Адрес: {orders[user]['address']}
        """
        client.chat_postMessage(channel="#заказы", text=summary)
        say("✅ Ваш заказ принят! Менеджер свяжется с вами.")
        orders[user]["step"] = 0

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()
