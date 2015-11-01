from jinja2.ext import Extension
from jinja2 import nodes
from markupsafe import Markup
from bs4 import BeautifulSoup
import flask
from flask import render_template
from flask import current_app as app

class EditorHeadExtension(Extension):
    tags = set(["editablehead"])

    def __init__(self, enviroment):
        super(EditorHeadExtension, self).__init__(enviroment)

    def parse(self, parser):
        lineno = parser.stream.next().lineno
        return nodes.CallBlock(self.call_method("_editablehead"), [], [], []).set_lineno(lineno)

    def _editablehead(self, caller):
        if flask.g.get("current_view_is_editor", False):
            return render_template("head.html")
        else:
            return ""

class EditorExtension(Extension):
    tags = set(["editableimage", "editabletext", "editablebgimage"])

    def __init__(self, enviroment):
        super(EditorExtension, self).__init__(enviroment)

    def parse(self, parser):
        function_name = "_" + parser.stream.current.value
        lineno = parser.stream.next().lineno
        args = [parser.parse_expression()]
        body = parser.parse_statements(["name:endeditabletext","name:endeditableimage","name:endeditablebgimage"], drop_needle=True)
        return nodes.CallBlock(self.call_method(function_name, args), [], [], body).set_lineno(lineno)

    def _editableimage(self, content_name, caller = None):
        soup = BeautifulSoup(caller(), "html.parser")
        image = app.extensions["editable"]["get_image"](content_name)
        soup.img["src"] = image["path"]
        soup.img["alt"] = image["description"]
        if flask.g.get("current_view_is_editor", False):
            soup.img["data-flask-editable-image"] = content_name
            soup.img["title"] = "Click to edit"
            soup.img["tabindex"] = "0"
        return Markup(soup)

    def _editabletext(self, content_name, caller = None):
        soup = BeautifulSoup(caller().lstrip(), "html.parser")
        element = soup.children.next()
        element.string = app.extensions["editable"]["get_text"](content_name)
        if flask.g.get("current_view_is_editor", False):
            element["contenteditable"] = "true"
            element["data-flask-editable-text"] = content_name
            element["title"] = "Click to edit"
        return Markup(soup)

    def _editablebgimage(self, content_name, caller = None):
        soup = BeautifulSoup(caller().lstrip(), "html.parser")
        element = soup.children.next()
        if element["style"].rstrip()[-1:] != ";":
            element["style"] += ";"
        url = app.extensions["editable"]["get_bgimage"](content_name)
        element["style"] += "background-image: url('%s');" % url
        if flask.g.get("current_view_is_editor", False):
            element["data-flask-editable-bg-image"] = content_name
            element["title"] = "Click to edit"
            element["tabindex"] = "0"
        return Markup(soup).unescape()
