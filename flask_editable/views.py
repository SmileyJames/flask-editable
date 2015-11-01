from flask import Blueprint, request
from flask import current_app as app
import models
import flask

editable = Blueprint("editable", __name__, template_folder="templates", static_folder="static")

@editable.route("/", methods=["GET", "POST"])
@editable.route("/<path:url>", methods=["GET", "POST"])
def editor(url = ""):
    if request.method == "GET":
        flask.g.current_view_is_editor = True
        client = app.test_client()
        return client.get("/" + url, headers = list(request.headers))
    if request.method == "POST":
        for name, text in request.json["text"].items():
            app.extensions["editable"]["set_text"](name, text)
        for name, image in request.json["images"].items():
            app.extensions["editable"]["set_image"](name, image["file"], image["description"])
        for name, image in request.json["bgimages"].items():
            app.extensions["editable"]["set_bgimage"](name, image)
        return ("", 204)

