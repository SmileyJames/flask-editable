from flask import current_app as app
from flask import url_for
import upload
from sqlalchemy.event import listen
from os.path import basename

def define_models(db):
    global EditorText
    global EditorImage
    global EditorBackgroundImage

    class EditorText(db.Model):
        name = db.Column(db.String(80), primary_key = True)
        text = db.Column(db.Text)

    class EditorImage(db.Model):
        name = db.Column(db.String(80), primary_key = True)
        path = db.Column(db.String(80))
        description = db.Column(db.String(80))
        filepath = db.Column(db.String(255))

    class EditorBackgroundImage(db.Model):
        name = db.Column(db.String(80), primary_key = True)
        path = db.Column(db.String(80))
        filepath = db.Column(db.String(255))

def set_wrappers(extension, db, app):
    @extension.set_text(app)
    def sqlalchemy_set_text(name, text):
        editor_text = EditorText(name=name)
        if text:
            editor_text.text = text
        db.session.merge(editor_text)
        db.session.commit()

    @extension.get_text(app)
    def sqlalchemy_get_text(name):
        text_obj = EditorText.query.filter_by(name = name).first()
        if hasattr(text_obj, "text") and text_obj.text:
            return text_obj.text
        else:
            return "Editable text content."

    @extension.set_image(app)
    def sqlalchemy_set_image(name, image, description):
        path, filepath = upload.save(image, "image-" + name)
        image = EditorImage(name=name)
        if path:
            image.path = path
            image.filepath = filepath
        if description:
            image.description = description
        db.session.merge(image)
        db.session.commit()

    @extension.get_image(app)
    def sqlalchemy_get_image(name):
        image = EditorImage.query.filter_by(name = name).first()
        return_dict = {"path": url_for("static", filename="editable.png"), "description": ""}
        if hasattr(image, "path") and image.path:
            return_dict["path"] = image.path
        if hasattr(image, "description") and image.description:
            return_dict["description"] = image.description
        return return_dict

    @extension.set_bgimage(app)
    def sqlalchemy_set_bgimage(name, image):
        path, filepath = upload.save(image, "bg-image-" + name)
        image = EditorBackgroundImage(name=name)
        if path:
            image.path = path
        if filepath:
            image.filepath = filepath
        db.session.merge(image)
        db.session.commit()

    @extension.get_bgimage(app)
    def sqlalchemy_get_bgimage(name):
        bgimage = EditorBackgroundImage.query.filter_by(name = name).first()
        fallback_path = url_for("static", filename="editable.png")
        if hasattr(bgimage, "path"):
            return EditorBackgroundImage.query.filter_by(name = name).first().path or fallback_path
        else:
            return fallback_path

    #If for some reason a model is deleted, delete the file associated to it
    def delete_image(target):
        os.remove(target.filepath)

    listen(EditorImage, "after_delete", delete_image)
    listen(EditorBackgroundImage, "after_delete", delete_image)
