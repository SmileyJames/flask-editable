from werkzeug import secure_filename
import os
import imghdr
from flask import url_for
from flask import current_app as app
from uuid import uuid4

def save(image, name):
    if image:
        image_data = image[image.find(","):].decode("base64")
        extension = imghdr.what(None, image_data)
        filename = secure_filename(name + "." + extension)
        filepath = os.path.join(app.static_folder, filename)
        f = open(filepath, "wb")
        f.write(image_data)
        f.close()
        return url_for("static", filename=filename), filepath
    else:
        return "", ""

