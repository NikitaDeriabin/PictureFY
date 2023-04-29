from django.shortcuts import render
from .forms import *
from django.http import HttpResponse, HttpResponseServerError
from .utils import stylization
from utils.file_handler import FileHandler

FH = FileHandler()


def upload_file(request):
    if request.method == "POST":
        if 'form_type_image' in request.POST:
            form = UploadImageField(request.POST, request.FILES)

            if form.is_valid():
                try:
                    main_file = request.FILES.getlist('main_file')[0]
                    style_file = request.FILES.getlist('style_file')[0]

                    main_prepared, style_prepared = stylization.prepare_images(main_file, style_file)
                    result_file = stylization.run_process(main_prepared, style_prepared)

                    jpg_image = FH.to_jpeg(result_file)

                    response = HttpResponse(jpg_image, content_type='image/jpeg')
                    response['Content-Disposition'] = 'attachment; filename="result.jpg"'

                    return response
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
                main_archive = request.FILES.getlist('main_file')[0]
                style_archive = request.FILES.getlist('style_file')[0]

                if not FH.check_archives_file_amount(main_archive, style_archive):
                    raise Exception("Different number of files in archives.")

                main_archive_generator = FH.get_files_from_archive(main_archive)
                style_archive_generator = FH.get_files_from_archive(style_archive)
                res_images = []

                for main_img, style_img in zip(main_archive_generator, style_archive_generator):
                    main_prepared, style_prepared = stylization.prepare_images(main_img, style_img)
                    res_images.append((FH.to_jpeg_filename(main_img.name),
                                       stylization.run_process(main_prepared, style_prepared)))

            except Exception as e:
                response = HttpResponseServerError()
                response['X-Error-Message'] = str(e)
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

    form = UploadImageField()
    archive_form = UploadArchiveField()
    return render(request, 'stylization/upload.html', {'form': form, 'archive_form': archive_form})
