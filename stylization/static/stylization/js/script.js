// IMAGE UPLOAD VARIABLES
const formStyleImage = document.querySelector("#form-image-stylization"),
    formImageIdSelector = '#form-image-stylization',
    formImageId = 'form-image-stylization',
    mainImageUploadWindow = document.querySelector("#image-main-upload-window"),
    styleImageUploadWindow = document.querySelector("#image-style-upload-window"),
    imageMainInput = document.querySelector(".image-input-main"),
    imageStyleInput = document.querySelector(".image-input-style"),
    mainUploadedAreaImage = document.querySelector("#image-main-uploaded-area"),
    styleUploadedAreaImage = document.querySelector("#image-style-uploaded-area"),
    formImageSubmitBtn = document.querySelector('#image-submit-btn');


// ARCHIVE UPLOAD VARIABLES
const formStyleArchive = document.querySelector("#form-archive-stylization"),
    formArchiveIdSelector = '#form-archive-stylization',
    formArchiveId = 'form-archive-stylization',
    mainArchiveUploadWindow = document.querySelector("#archive-main-upload-window"),
    styleArchiveUploadWindow = document.querySelector("#archive-style-upload-window"),
    archiveMainInput = document.querySelector(".archive-input-main"),
    archiveStyleInput = document.querySelector(".archive-input-style"),
    mainUploadedAreaArchive = document.querySelector("#archive-main-uploaded-area"),
    styleUploadedAreaArchive = document.querySelector("#archive-style-uploaded-area"),
    formArchiveSubmitBtn = document.querySelector('#archive-submit-btn');

// IMAGE LISTENERS
mainImageUploadWindow.addEventListener("click", () => {
    imageMainInput.click();
});

styleImageUploadWindow.addEventListener("click", () => {
    imageStyleInput.click();
})

imageMainInput.onchange = ({target}) => {
    input_onchange(mainUploadedAreaImage, target, 5);
}

imageStyleInput.onchange = ({target}) => {
    input_onchange(styleUploadedAreaImage, target, 5);
}

formImageSubmitBtn.addEventListener('click', () => {
    submit_btn_on_click_extended(imageMainInput, imageStyleInput, formImageIdSelector, mainUploadedAreaImage,
                                 styleUploadedAreaImage);
});

// ARCHIVE LISTENERS
mainArchiveUploadWindow.addEventListener("click", () => {
    archiveMainInput.click();
});

styleArchiveUploadWindow.addEventListener("click", () => {
    archiveStyleInput.click();
})

archiveMainInput.onchange = ({target}) => {
    input_onchange(mainUploadedAreaArchive, target, 5);
}

archiveStyleInput.onchange = ({target}) => {
    input_onchange(styleUploadedAreaArchive, target, 5);
}

formArchiveSubmitBtn.addEventListener('click', () => {
    submit_btn_on_click_extended(archiveMainInput, archiveStyleInput, formArchiveIdSelector, mainUploadedAreaArchive,
                                 styleUploadedAreaArchive);
});


$(formImageIdSelector).submit(function (e) {
    e.preventDefault();
    spinnerBox.fadeIn(500);
    const formData = getFormData(formStyleImage, 'form_type_image', 'Upload');
    const responseFilename = 'result.jpg';
    const contentType = 'image/jpeg';

    $.ajax({
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        xhrFields: {
            responseType: 'blob'
        },
        success: function (response) {
            handleSuccess(response, responseFilename, contentType);
        },
        error: function (xhr, textStatus, errorThrown) {
            handleError(xhr, textStatus, errorThrown, formImageId);
        }
    }).done(function () {
        reset_form(formImageId);
    });
});

$(formArchiveIdSelector).submit(function (e) {
    e.preventDefault();
    spinnerBox.fadeIn(500);
    const formData = getFormData(formStyleArchive, 'form_type_archive', 'Upload');
    const responseFilename = 'result.zip';
    const contentType = 'application/zip';

    $.ajax({
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        xhrFields: {
            responseType: 'blob'
        },
        success: function (response) {
            handleSuccess(response, responseFilename, contentType);
        },
        error: function (xhr, textStatus, errorThrown) {
            handleError(xhr, textStatus, errorThrown, formArchiveId);
        }
    }).done(function () {
        reset_form(formArchiveId);
    });
});
