from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)


@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    incoming = request.values.get('Body', '').strip()
    resp = MessagingResponse()

    if not incoming:
        resp.message("I didn't receive any text. Send 'help' for commands.")
        return str(resp)

    text = incoming.lower()
    if text == 'ping':
        resp.message('pong')
    elif text == 'help':
        resp.message("Commands:\n- ping -> pong\n- echo <text> -> echoes back")
    elif text.startswith('echo '):
        resp.message(incoming[5:])
    else:
        resp.message(f"You said: {incoming}\nSend 'help' for options.")

    return str(resp)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
