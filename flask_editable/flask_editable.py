from flask import current_app
import views
import jinja_extensions
import models

class Editable(object):

    app = None

    def __init__(self, app=None, db=None, save_path="editable_uploads/"):
        self.app = app
        if app is not None:
            self.init_app(app, db)

    def init_app(self, app, db = None):
        app.teardown_appcontext(self.teardown)
        app.jinja_env.add_extension(jinja_extensions.EditorExtension)
        app.jinja_env.add_extension(jinja_extensions.EditorHeadExtension)
        app.register_blueprint(views.editable, url_prefix="/editable")
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions["editable"] = {}
        if db is not None:
            models.define_models(db)
            models.set_wrappers(self, db, app)

    def teardown(self, exception):
        pass

    def set_text(self, app):
        def decorator(func):
            app.extensions["editable"]["set_text"] = func
        return decorator

    def get_text(self, app):
        def decorator(func):
            app.extensions["editable"]["get_text"] = func
        return decorator

    def set_image(self, app):
        def decorator(func):
            app.extensions["editable"]["set_image"] = func
        return decorator

    def get_image(self, app):
        def decorator(func):
            app.extensions["editable"]["get_image"] = func
        return decorator

    def set_bgimage(self, app):
        def decorator(func):
            app.extensions["editable"]["set_bgimage"] = func
        return decorator

    def get_bgimage(self, app):
        def decorator(func):
            app.extensions["editable"]["get_bgimage"] = func
        return decorator
