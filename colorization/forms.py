from django import forms
from django.core.validators import FileExtensionValidator


class UploadImageField(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'image-input',
                                                                  'multiple': True,
                                                                  'accept': 'image/jpeg, image/jpg,'
                                                                            'image/png, image/webp, image/gif,'
                                                                            'image/jfif, image/tiff, image/bmp',
                                                                  'hidden': True}),
                           validators=[FileExtensionValidator(allowed_extensions=
                                                              ['jpeg', 'jpg', 'png', 'webp', 'gif', 'jfif', 'tiff',
                                                               'bmp'])])


class UploadArchiveField(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'archive-input',
                                                                  'multiple': False,
                                                                  'accept': 'application/zip,'
                                                                            '.rar',
                                                                  'hidden': True}),
                           validators=[FileExtensionValidator(allowed_extensions=['zip', 'rar'])])
