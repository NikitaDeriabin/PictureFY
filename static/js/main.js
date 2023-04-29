// SPINNER
const spinnerBox = $('#bg-spinner');

//DROPDOWN MENU
const toggleBtn = document.querySelector('.toggle_btn');
const toggleBtnIcon = document.querySelector('.toggle_btn i');
const dropDownMenu = document.querySelector('.dropdown_menu');

toggleBtn.addEventListener('click', () => {
    dropDownMenu.classList.toggle('open');

    const isOpen = dropDownMenu.classList.contains('open');
    toggleBtnIcon.classList = isOpen
        ? 'fa-solid fa-xmark'
        : 'fa-solid fa-bars'
});

// AJAX HANDLERS
function showModalError(errorMessage) {
    Swal.fire({
        title: 'Oops! Something went wrong.',
        text: errorMessage,
        icon: 'warning',
        color: 'white',
        background: 'rgb(53,53,53)',
        position: 'center',
        confirmButtonText: 'Close',
        confirmButtonColor: '#FDA500'
    })
}

function handleError(xhr, textStatus, errorThrown, element_name) {
    spinnerBox.fadeOut(500);
    reset_form(element_name);

    try {
        const errorMessage = xhr.getResponseHeader('X-Error-Message');
        if (errorMessage) {
            showModalError(errorMessage);
        } else {
            let jsonResponse = JSON.parse(xhr.responseText);
            if (jsonResponse.error) {
                showModalError(jsonResponse.error);
            }
        }
    } catch (e) {
        showModalError("Unexpected error");
    }
}

function handleSuccess(response, response_filename, content_type) {
    spinnerBox.fadeOut(500);
    download_response_file(response, response_filename, content_type);

    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        background: 'rgb(53,53,53)',
        color: 'white',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didOpen: (toast) => {
            toast.addEventListener('mouseenter', Swal.stopTimer)
            toast.addEventListener('mouseleave', Swal.resumeTimer)
        }
    });

    Toast.fire({
        icon: 'success',
        title: 'Files processed successfully'
    });
}

function getFormData(form, formData_name, formData_value) {
    let formData = new FormData(form);
    formData.append(formData_name, formData_value);
    return formData;
}

function download_response_file(response, filename, content_type) {
    let blob = new Blob([response], {type: content_type});
    let url = window.URL.createObjectURL(blob);
    let link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function reset_form(form_id) {
    $('#' + form_id)[0].reset();
}


// UPLOAD WINDOW HANDLERS
function uploadFile(name, uploadedArea) {
    let uploadedHTML = `<li class="row">
                            <div class="content upload">
                              <i class="fas fa-file-alt"></i>
                              <div class="details">
                                <span class="name">${name}</span>
                              </div>
                            </div>
                            <i class="fas fa-check"></i>
                          </li>`;
    uploadedArea.insertAdjacentHTML("afterbegin", uploadedHTML);
}

function input_onchange(uploadedArea, target, max_text_length) {
    uploadedArea.innerHTML = '';
    let files = target.files;
    for (let i = 0; i < files.length; i++) {
        if (files[i]) {
            let fileName = files[i].name;
            let splitName = fileName.split('.');
            if (splitName[0].length > max_text_length + 2) {
                fileName = splitName[0].substring(0, max_text_length) + "...." + splitName[1];
            }
            uploadFile(fileName, uploadedArea);
        }
    }
}

function submit_btn_on_click(inputField, formIdSelector, uploadedArea) {
    if (inputField.value) {
        $(formIdSelector).submit();
        uploadedArea.innerHTML = '';
    }
}

function submit_btn_on_click_extended(mainInputField, styleInputField, formIdSelector, mainUploadedArea, styleUploadedArea) {
    if (mainInputField.value && styleInputField.value) {
        $(formIdSelector).submit();
        mainUploadedArea.innerHTML = '';
        styleUploadedArea.innerHTML = '';
    }
}

// IMAGE LISTENERS
formImage.addEventListener("click", () => {
    imageInput.click();
});

imageInput.onchange = ({target}) => {
    input_onchange(uploadedAreaImage, target, 12);
}

formImageSubmitBtn.addEventListener('click', () => {
    submit_btn_on_click(imageInput, formImageIdSelector, uploadedAreaImage);
});

// ARCHIVE LISTENERS
formArchive.addEventListener("click", () => {
    archiveInput.click();
})

archiveInput.onchange = ({target}) => {
    input_onchange(uploadedAreaArchive, target);
}

formArchiveSubmitBtn.addEventListener('click', () => {
    submit_btn_on_click(archiveInput, formArchiveIdSelector, uploadedAreaArchive);
});

