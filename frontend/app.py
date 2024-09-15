import os
import logging
from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
from gevent.pywsgi import WSGIServer

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static')

# Use the correct environment variable name
LLM_BACKEND_URL = os.getenv('LLM_BACKEND_URL')
logger.info(f"LLM_BACKEND_URL: {LLM_BACKEND_URL}")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.json
        user_input = data.get('user_input')
        chat_history = data.get('chat_history', [])

        if not user_input:
            logger.warning("No user input provided")
            return jsonify({"error": "No user input provided"}), 400

        try:
            # Prepare the context from chat history
            context = "\n".join([f"{'User' if msg['isUser'] else 'Assistant'}: {msg['message']}" for msg in chat_history])

            # Append the new user input
            context += f"\nUser: {user_input}\nAssistant:"

            logger.debug(f"Sending request to LLM backend with context: {context}")

            session = requests.Session()
            session.timeout = (5, 300)  # 5 seconds for connection, 300 seconds for reading

            response = session.post(LLM_BACKEND_URL, json={"text": context})

            if response.status_code == 200:
                llm_response = response.json()['response']
                logger.info("Successfully received response from LLM backend")
                return jsonify({"response": llm_response})
            else:
                logger.error(f"Failed to get response from LLM backend. Status code: {response.status_code}, Response: {response.text}")
                return jsonify({"error": f"Failed to get response from LLM backend. Status code: {response.status_code}"}), 500
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect to LLM backend: {str(e)}")
            return jsonify({"error": f"Failed to connect to LLM backend: {str(e)}"}), 500
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
    return render_template('index.html')


@app.route('/logo')
def serve_logo():
    return send_from_directory(app.static_folder, 'images/logo_no_backround.png')


if __name__ == '__main__':
    logger.info("Starting the server...")
    http_server = WSGIServer(('0.0.0.0', 5000), app, log=logger)
    http_server.serve_forever()
