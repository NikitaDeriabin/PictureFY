from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import *
from utils.file_handler import FileHandler
from .utils.classification import model

import os

FH = FileHandler()


def upload_file(request):
    if request.method == "POST":
        filenames = []
        predicts = []

        if 'form_type_files' in request.POST:
            form = UploadImageField(request.POST, request.FILES)
            if form.is_valid():
                files = request.FILES.getlist('file')

                # storing filenames and predictions for each of them
                for file in files:
                    filenames.append(str(file))
                    predicts.append(model.get_prediction(file))
            else:
                return JsonResponse({'error': 'There is validation error. Check your files extensions.'}, status=500)

        if 'form_type_archive' in request.POST:
            form = UploadArchiveField(request.POST, request.FILES)
            if form.is_valid():
                try:
                    files = request.FILES.getlist('file')
                    archive = files[0]

                    # using a generator to iterate over all files in the archive
                    for file in FH.get_files_from_archive(archive):
                        filenames.append(os.path.basename(str(file.name)))
                        predicts.append(model.get_prediction(file))

                except Exception as e:
                    return JsonResponse({'error': 'Check the file extensions in the archive.'}, status=500)
            else:
                return JsonResponse({'error': 'There is validation error. Check your files extensions.'}, status=500)

        try:
            # getting buffer
            csv_data_buffer = FH.to_csv({"filenames": filenames, "classes": predicts})

            # creating response
            response = HttpResponse(csv_data_buffer.getvalue(), content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename="picture_classes.csv"'

            # clearing buffer
            FH.clear_buffer(buffer=csv_data_buffer)

            return response
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    image_form = UploadImageField()
    archive_form = UploadArchiveField()

    return render(request, 'object_recognition/upload.html', {'image_form': image_form, 'archive_form': archive_form})
