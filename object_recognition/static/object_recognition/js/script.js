// IMAGE UPLOAD VARIABLES
const formImage = document.querySelector("#form-image-recognition"),
    formImageIdSelector = '#form-image-recognition',
    formImageId = 'form-image-recognition',
    imageInput = document.querySelector(".image-input"),
    uploadedAreaImage = document.querySelector("#image-uploaded-area"),
    formImageSubmitBtn = document.querySelector('#image-submit-btn');


// ARCHIVE UPLOAD VARIABLES
const formArchive = document.querySelector("#form-archive-recognition"),
    formArchiveIdSelector = '#form-archive-recognition',
    formArchiveId = 'form-archive-recognition',
    archiveInput = document.querySelector(".archive-input"),
    uploadedAreaArchive = document.querySelector("#archive-uploaded-area"),
    formArchiveSubmitBtn = document.querySelector('#archive-submit-btn');


// IMAGE AJAX REQUEST
$(formImageIdSelector).submit(function (e) {
    e.preventDefault();
    spinnerBox.fadeIn(500);
    const formData = getFormData(formImage, 'form_type_files', 'Upload');
    const responseFilename = 'picture_classes.csv';
    const contentType = 'text/csv';

    $.ajax({
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
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

// ARCHIVE AJAX REQUEST
$(formArchiveIdSelector).submit(function (e) {
    e.preventDefault();
    spinnerBox.fadeIn(500);
    const formData = getFormData(formArchive, 'form_type_archive', 'Upload');
    const responseFilename = 'picture_classes.csv';
    const contentType = 'text/csv';

    $.ajax({
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
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