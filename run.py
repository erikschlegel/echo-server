import os
import pprint
from logging.config import dictConfig

from flask import Flask, jsonify, request


dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)


app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

app_name = os.getenv("APP_NAME")

ALL_METHODS = ["GET", "HEAD", "POST", "PUT", "DELETE", "OPTIONS"]


@app.route("/", defaults={"path": ""}, methods=ALL_METHODS)
@app.route("/<path:path>", methods=ALL_METHODS)
def index(path):
    data = {
        "path": request.path,
        "methods": request.method,
        "headers": list(request.headers.items()),
        "form": list(request.form.items()),
        "args": list(request.args.items()),
        "remote": {
            "address": request.environ.get("REMOTE_ADDR", "???"),
            "port": request.environ.get("REMOTE_PORT", "???"),
        },
        "content-type": request.content_type,
        "files": [(f[0], f[1].filename) for f in request.files.items()],
        "json-cobalt-demo": request.json,
        "raw-data": str(request.data),
    }

    if app_name:
        data["APP-NAME"] = app_name
    app.logger.info("\n" + pprint.pformat(data))
    return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
