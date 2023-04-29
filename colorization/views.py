from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from .forms import *
from utils.file_handler import FileHandler

from .utils import colorization

FH = FileHandler()


def upload_file(request):
    if request.method == "POST":
        res_images = []

        if 'form_type_files' in request.POST:
            form = UploadImageField(request.POST, request.FILES)
            if form.is_valid():
                try:
                    files = request.FILES.getlist('file')
                    for file in files:
                        res_images.append((FH.to_jpeg_filename(file.name), colorization.colorize(file)))

                except Exception as e:
                    response = HttpResponseServerError()
                    response['X-Error-Message'] = 'Check the file extensions.'
                    return response
            else:
                response = HttpResponseServerError()
                response['X-Error-Message'] = 'There is validation error. Check your files extensions.'
                return response

        if 'form_type_archive' in request.POST:
            form = UploadArchiveField(request.POST, request.FILES)
            if form.is_valid():
                try:
                    archive = request.FILES.getlist('file')[0]

                    files_generator = FH.get_files_from_archive(archive)
                    for file in files_generator:
                        res_images.append((FH.to_jpeg_filename(file.name), colorization.colorize(file)))

                except Exception as e:
                    response = HttpResponseServerError()
                    response['X-Error-Message'] = 'Check the file extensions in the archive.'
                    return response
            else:
                response = HttpResponseServerError()
                response['X-Error-Message'] = 'There is validation error. Check your files extensions.'
                return response

        try:
            response_data = FH.to_zip_buffer(res_images)

            response = HttpResponse(response_data, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="result.zip"'

            return response

        except Exception as e:
            response = HttpResponseServerError()
            response['X-Error-Message'] = str(e)
            return response

    image_form = UploadImageField()
    archive_form = UploadArchiveField()

    return render(request, 'colorization/upload.html', {'image_form': image_form, 'archive_form': archive_form})
