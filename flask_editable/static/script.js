$(function(){
    //JSON object
    var formData = {"text": {}, "images": {}, "bgimages": {}};

    $("[data-flask-editable-image], [data-flask-editable-bg-image]").keypress(function(e){
        if (e.which == 13) {
            $(this).click();
        }
    });

    /*
     *
     * When the text in an editable text element changes store
     * the text in the json object that will later be sent to
     * the server.
     *
     */
    $("[data-flask-editable-text]").keyup(function(){
        var element = $(this);
        var name = element.attr("data-flask-editable-text");
        var text = element.text();
        $('[data-flask-editable-text="' + name + '"]').not(element).text(text);
        formData["text"][name] = text
        publishButton.text("Publish");
    });

    // Setup the form for editable images
    var imageForm = $(
    '<div class="flask-edit-fixed">' +
    '    <div class="flask-edit-form">' +
    '        <label class="flask-edit-file-upload" for="file-upload">' +
    '             Choose image file' +
    '             <br />' +
    '             <svg fill="#FFFFFF" height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="M0 0h24v24H0z" fill="none"/><path d="M9 16h6v-6h4l-7-7-7 7h4zm-4 2h14v2H5z"/></svg>' +
    '             <input id="file-upload" type="file" name="image" accept="image/*"/>' +
    '        </label>' +
    '        <label class="flask-edit-label" for="description">Description of image:</label>' +
    '        <input class="flask-edit-input-text" type="text" id="description" name="description"/>' +
    '        <button class="flask-edit-close-button">Done</button>' +
    '    </div>' +
    '</div>');
    $("body").append(imageForm);
    imageForm.hide();
    imageForm.click(function(){
        imageForm.hide();
        $("body").removeClass("flask-edit-stop-scroll");
    }).children().click(function(e){
        e.stopPropagation();
    });
    imageForm.find(".flask-edit-close-button").click(function(){
        imageForm.hide();
        $("body").removeClass("flask-edit-stop-scroll");
    });

    /*
     *
     * When an editable image is clicked show the image form.
     * When the image form changes update the image itself aswell
     * as the json object that will later be sent to the sever.
     *
     */
    $("[data-flask-editable-image]").click(function() {
        var element = $(this);
        var name = element.attr("data-flask-editable-image");
        imageForm.find("#description").val(element.attr("alt"));
        formData["images"][name] = formData["images"][name] || {"file": "", "description": ""};
        imageForm.show();
        $("body").addClass("flask-edit-stop-scroll");

        imageForm.find('input[type="file"]').change(function(){
            var input = this;
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = function(e){
                    $('[data-flask-editable-image="' + name + '"]').attr("src", e.target.result);
                    formData["images"][name]["file"] = e.target.result;
                    publishButton.text("Publish");
                };
                reader.readAsDataURL(input.files[0])
            }
        });

        imageForm.find('input[type="text"]').change(function() {
            var description = $(this).val();
            $('[data-flask-editable-image="' + name + '"]').attr("alt", description);
            formData["images"][name]["description"] = description;
            publishButton.text("Publish");
        });
    });

    // Input to be used for uploading bg images
    var fileInput = $('<input type="file"></input>')
    $("body").append(fileInput);
    fileInput.hide();

    /*
     *
     * When an element with an editable background imgae is clicked
     * open a file upload dialog. When a file is selected set it as
     * the background image and save to the json object that will
     * later be sent to the server.
     *
     */
    $("[data-flask-editable-bg-image]").click(function(){
        var element = $(this);
        var name = element.attr("data-flask-editable-bg-image");
        fileInput.trigger("click").change(function(){
            var input = this;
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = function(e){
                    $('[data-flask-editable-bg-image="' + name + '"]').css("background-image", "url(" + e.target.result + ")");
                    formData["bgimages"][name] = e.target.result;
                    publishButton.text("Publish");
                };
                reader.readAsDataURL(input.files[0])
            }
        });
    });

    var publishButton = $("<button class='flask-edit-publish-button'>Publish</button>");
    $("body").append(publishButton);
    publishButton.click(function() {
        publishButton.text("Publishing...");
        $.ajax({
            url: "/editable/",
            data: JSON.stringify(formData),
            type: "POST",
            contentType: "application/json",
            success: function() {
                publishButton.text("Published");
            },
            error: function() {
                publishButton.text("Publish failed");
            },
        });
    });
})
