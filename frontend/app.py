import logging
from flask import Flask, render_template
from gevent.pywsgi import WSGIServer

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder="static")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/component/<path:name>")
def component(name):
    return render_template(f"components/{name}.html")


if __name__ == "__main__":
    logger.info("Starting the server...")
    http_server = WSGIServer(("0.0.0.0", 5000), app, log=logger)
    http_server.serve_forever()
