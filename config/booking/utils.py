import requests


BOT_TOKEN = "TOKEN"


def send_telegram_notification(chat_id, appointment):
    if not chat_id:
        return

    message = (
        f"🩺 *Yangi Qabul Zayavkasi!*\n\n"
        f"👤 *Bemor:* {appointment.patient_name}\n"
        f"📞 *Tel:* {appointment.patient_phone}\n"
        f"⏰ *Vaqti:* {appointment.date_time.strftime('%Y-%m-%d %H:%M')}\n"
        f"📝 *Shikoyati:* {appointment.symptoms}\n"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram Notification Error: {e}")