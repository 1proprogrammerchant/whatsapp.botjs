from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('bot.py')

app = Flask(__name__)

TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')


def validate_twilio(req):
if not TWILIO_AUTH_TOKEN:
return True
validator = RequestValidator(TWILIO_AUTH_TOKEN)
signature = req.headers.get('X-Twilio-Signature', '')
url = req.url
params = req.form.to_dict() if req.form else {}
try:
return validator.validate(url, params, signature)
except Exception:
return False


@app.route('/', methods=['GET'])
def index():
return '<html><body><h3>Simple WhatsApp bot (bot.py)</h3><p>POST /whatsapp to interact.</p></body></html>'


@app.route('/health', methods=['GET'])
def health():
return {'status': 'ok'}


@app.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp():
if request.method == 'GET':
return (
"<html><body><h3>WhatsApp webhook</h3><p>POST messages to this URL with form field <code>Body</code>.</p></body></html>",
200,
{'Content-Type': 'text/html'}
)

if not validate_twilio(request):
logger.warning('Twilio signature validation failed')
return ('', 403)

incoming = (request.values.get('Body', '') or '').strip()
resp = MessagingResponse()

if not incoming:
resp.message("I didn't receive any text. Send 'help' for commands.")
return str(resp)

lower = incoming.lower()
if lower == 'ping':
resp.message('pong')
elif lower == 'help':
resp.message('Commands:\n- ping\n- echo <text>\n- reverse <text>')
elif lower.startswith('echo '):
resp.message(incoming[5:])
elif lower.startswith('reverse '):
resp.message(incoming[8:][::-1])
else:
resp.message(f"You said: {incoming}\nSend 'help' for commands.")

return str(resp)


if __name__ == '__main__':
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
