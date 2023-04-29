from django import forms
from django.core.validators import FileExtensionValidator
import copy


def _change_widget_attr(widget, attr, value):
    widget_copy = copy.deepcopy(widget)
    widget_copy.attrs[attr] = value
    return widget_copy


class UploadImageField(forms.Form):

    _widget = forms.ClearableFileInput(attrs={'class': 'image-input',
                                              'multiple': False,
                                              'accept': 'image/jpeg, image/jpg,'
                                                        'image/png, image/webp, image/gif,'
                                                        'image/jfif, image/tiff, image/bmp',
                                              'hidden': True
                                              })
    _allowed_ext = [FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png', 'webp', 'gif', 'jfif', 'tiff',
                                                               'bmp'])]

    main_file = forms.FileField(widget=_change_widget_attr(_widget, 'class', 'image-input-main'),
                                validators=_allowed_ext)
    style_file = forms.FileField(widget=_change_widget_attr(_widget, 'class', 'image-input-style'),
                                 validators=_allowed_ext)


class UploadArchiveField(forms.Form):
    _widget = forms.ClearableFileInput(attrs={'class': 'archive-input',
                                              'multiple': False,
                                              'accept': 'application/zip, .rar',
                                              'hidden': True
                                              })
    _allowed_ext = [FileExtensionValidator(allowed_extensions=['zip', 'rar'])]

    main_file = forms.FileField(widget=_change_widget_attr(_widget, 'class', 'archive-input-main'),
                                validators=_allowed_ext)
    style_file = forms.FileField(widget=_change_widget_attr(_widget, 'class', 'archive-input-style'),
                                 validators=_allowed_ext)
